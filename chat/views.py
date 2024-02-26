import base64
import calendar
import io
import json
import os
import re
import time
import decimal
import hashlib
from datetime import timedelta, datetime
from urllib import parse
from urllib.parse import urlparse
from uuid import uuid4

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import requests
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from translate import Translator
import config
from authentication.forms import UserLoginForm, UserRegisterForm
from authentication.models import User, BusinessSubscription
from tochkagpt import settings
from tochkagpt.settings import BASE_DIR, STATIC_URL, MEDIA_URL
from .models import Message, Chat, Tariff, Sample, SampleCategory, UserSamplesLikes, UserSample, Attachment, \
    NewChatInstruction, NewChatCategory, NewChatSample, PaymentOperation, Subscription


def index(request):

    context = {
        'title': 'Чат',
        'new_chat_samples_1': NewChatSample.objects.filter(category__isnull=True, section='1').order_by('pk'),
        'new_chat_samples_2': NewChatSample.objects.filter(category__isnull=True, section='2').order_by('pk'),
    }

    if request.user.is_authenticated:
        context['chats'] = Chat.objects.filter(user__pk=request.user.pk, is_deleted=False).order_by('pk')
        context['current_chat'] = request.user.get_current_chat
        context['tariffs'] = Tariff.objects.all().order_by('price')
        context['samples'] = Sample.objects.filter(usersample__isnull=True)
        context['sample_categories'] = SampleCategory.objects.all()
        context['categories_js'] = {cat.pk: cat.name for cat in context['sample_categories']}
        context['samples_js'] = serializers.serialize('json', context['samples'])
        context['user_samples_js'] = serializers.serialize('json', request.user.get_samples)
        context['liked_samples_js'] = serializers.serialize('json', request.user.get_liked_samples)
        context['liked_samples_pks'] = [sample.pk for sample in request.user.get_liked_samples]
        context['STATIC_URL'] = STATIC_URL
        context['MEDIA_URL'] = MEDIA_URL
        context['request_price'] = config.REQUEST_PRICE
        context['new_chat_categories_1'] = NewChatCategory.objects.filter(section='1')
        context['new_chat_categories_2'] = NewChatCategory.objects.filter(section='2')
        context['new_chat_categories_3'] = NewChatCategory.objects.filter(section='3')
        context['instructions'] = NewChatInstruction.objects.all()
    else:
        context['login_form'] = UserLoginForm()
        context['register_form'] = UserRegisterForm()
        context['action'] = 'none'

    return render(request, 'chat/chat.html', context=context)


@login_required
def like_sample(request):

    if request.user.check_samples:
        return JsonResponse({'result': 'failed'})

    pk = int(request.POST.get('pk'))
    sample = Sample.objects.filter(pk=pk)

    if UserSamplesLikes.objects.filter(user__pk=request.user.pk, sample__pk=pk).exists() or \
       not sample.exists():
        return JsonResponse({'result': 'failed'})

    sample = sample.first()
    UserSamplesLikes.objects.create(sample=sample, user=request.user)

    return JsonResponse({'result': 'ok', 'sample': {
        'pk': sample.pk, 'fields': {'name': sample.name, 'description': sample.description,
                                    'categories': [cat.pk for cat in sample.get_categories]}
    }})


@login_required
def delete_sample(request):

    if request.user.check_samples:
        return JsonResponse({'result': 'failed'})

    pk = int(request.POST.get('pk'))
    sample = UserSample.objects.filter(pk=pk)

    if not sample.exists():
        return JsonResponse({'result': 'failed'})

    sample.delete()

    return JsonResponse({'result': 'ok'})


@login_required
def create_sample(request):

    if request.user.check_samples:
        return JsonResponse({'result': 'failed'})

    name = request.POST.get('name')
    description = request.POST.get('name')
    text = request.POST.get('name')
    variables = json.loads(request.POST['variables'])
    categories = json.loads(request.POST['categories'])

    for var in variables.keys():
        if var not in ['[TEXT]', '[TEXT2]', '[TEXT3]']:
            del variables[var]

    var_names = variables.keys()
    if not name or not text or ('[TEXT]' not in var_names and ('[TEXT2]' in var_names or '[TEXT3]' in var_names)):
        return JsonResponse({'result': 'failed'})

    variables = json.dumps(variables)

    for cat in categories:
        try:
            if not SampleCategory.objects.filter(pk=int(cat)).exists():
                categories.remove(cat)
        except ValueError:
            categories.remove(cat)

    categories = [int(cat) for cat in categories]

    sample = UserSample.objects.create(user=request.user, name=name, text=text, variables=variables)

    if description:
        sample.description = description

    sample.categories.add(*categories)
    sample.save()

    return JsonResponse({'result': 'ok', 'sample': {
        'pk': sample.pk, 'fields': {'name': sample.name, 'description': sample.description,
                                    'categories': categories}}})


@login_required
def unlike_sample(request):

    if request.user.check_samples:
        return JsonResponse({'result': 'failed'})

    pk = int(request.POST.get('pk'))
    like = UserSamplesLikes.objects.filter(user__pk=request.user.pk, sample__pk=pk)

    if not like.exists():
        return JsonResponse({'result': 'failed'})

    like.delete()

    return JsonResponse({'result': 'ok'})


def get_gpt35_response(message, user, chat, from_subscription):
    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {
              "content": "You are a personal helpful assistant.",
              "role": "system"
            }
        ],
        "frequency_penalty": 1.5,
        "temperature": 0.8
    }

    if user.use_context:
        messages_query = Message.objects.filter(Q(chat__pk=chat.pk, is_deleted=False) & ~Q(pk=message.pk))
        if user.get_subscription is None and user.business_subscription is None:
            messages = []
            length = 0
            for m in messages_query.order_by('-pk'):
                length += len(m.text)
                if length <= config.CONTEXT_SIZE:
                    messages.append(m)
                else:
                    break
            messages.reverse()
        else:
            messages = messages_query

        for m in messages:
            data['messages'].append({
                "content": m.text,
                "role": "user" if m.is_sender else "assistant"
            })

    data['messages'].append({
      "content": message.text,
      "role": "user"
    })

    headers = {
        'x-api-key': config.GPT_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.post(url=f'{config.GPT_URL}/v1/openai/completion/',
                             json=data, headers=headers)
    response_json = response.json()
    received_message = Message.objects.create(user=user, chat=chat, is_sender=False, used_ai='GPT35',
                                              from_subscription=from_subscription,
                                              text=response_json['result'])
    return {'text': received_message.text, 'message_pk': received_message.pk}


def get_gpt4_response(message, user, chat, from_subscription):
    received_message = Message.objects.create(user=user, chat=chat, is_sender=False, used_ai='GPT4',
                                              from_subscription=from_subscription,
                                              text='4 Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.')
    return {'text': received_message.text, 'message_pk': received_message.pk}


def get_stable_response(message, user, chat, from_subscription):
    text = message.text
    if re.search(r'[а-яёА-ЯЁ]', text):
        translator = Translator(to_lang='en', from_lang='ru')
        text = translator.translate(text)
    payload = {
        "prompt": text,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 2,
        "steps": 20,
        "cfg_scale": 7,
        "width": 1024,
        "height": 1024
    }

    response = requests.post(url=f'{config.SD_URL}/sdapi/v1/txt2img', auth=(config.SD_USERNAME, config.SD_PASSWORD),
                             json=payload)

    response_json = response.json()
    image = Image.open(io.BytesIO(base64.b64decode(response_json['images'][0])))

    current_gmt = time.gmtime()
    time_stamp = calendar.timegm(current_gmt)
    file_name = f'{time_stamp}-{uuid4().hex}.{image.format.lower()}'
    new_file_path = os.path.join(BASE_DIR, 'media', 'attachments', file_name)
    image.save(new_file_path, quality=90, optimize=True)
    received_message = Message.objects.create(user=user, chat=chat, is_sender=False, used_ai='SD',
                                              from_subscription=from_subscription)
    attachment = Attachment.objects.create(message=received_message, file='attachments/' + file_name)
    return {'file': attachment.file.url, 'message_pk': received_message.pk}


def get_midjourney_response(message, user, chat, from_subscription):
    data = {
        "prompt": message.text,
        "api_token": config.MJ_TOKEN,
    }

    prompt_response = requests.post(url=f'{config.MJ_URL}/api/v1/midjourney/imagine',
                                    data=data)
    prompt_response_json = prompt_response.json()
    img_response_json = {'result': {'status': 'waiting_to_start'}}
    while img_response_json['result']['status'] in ['waiting_to_start', 'process']:
        time.sleep(20)
        img_response = requests.get(url=f'{config.MJ_URL}/api/v1/midjourney/task/'
                                        f'{prompt_response_json["result"]["task_id"]}')
        img_response_json = img_response.json()

    img_data = requests.get(url=img_response_json['result']['image_url']).content
    current_gmt = time.gmtime()
    time_stamp = calendar.timegm(current_gmt)
    file_name = f'{time_stamp}-{uuid4().hex}.jpg'
    file_path = str(BASE_DIR) + '/media/attachments/' + file_name
    with open(file_path, 'wb') as handler:
        handler.write(img_data)

    received_message = Message.objects.create(user=user, chat=chat, is_sender=False, used_ai='MJ',
                                              from_subscription=from_subscription)
    attachment = Attachment.objects.create(message=received_message, file='attachments/' + file_name)
    return {'file': attachment.file.url, 'message_pk': received_message.pk}


def get_vision_response(message, user, chat, from_subscription):
    client = OpenAI(api_key=config.VISION_TOKEN)
    with open(str(BASE_DIR) + message.get_attachment[0], "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": message.text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "auto"
                        },
                    },
                ],
            }
        ],
        max_tokens=1000
    )
    received_message = Message.objects.create(user=user, chat=chat, is_sender=False,
                                              from_subscription=from_subscription, used_ai='VS',
                                              text=response.choices[0].message.content)
    return {'text': received_message.text, 'message_pk': received_message.pk}


@login_required
def handle_request(request):

    try:
        text = request.POST.get('text')
        is_new = request.POST.get('is_new')
        sample_pk = request.POST.get('sample')
        subscription = request.user.get_subscription
        business_subscription = request.user.business_subscription
        if sample_pk:
            sample = Sample.objects.filter(pk=int(sample_pk))
            if sample.exists() and request.user.check_samples:
                sample = sample.first()
                variables = json.loads(request.POST['variables'])
                text = sample.text
                for key, value in variables.items():
                    text = text.replace(key, value)
            else:
                sample_pk = None

        if is_new == 'true':
            chat = Chat.objects.create(user=request.user)
            chat.set_current()
        else:
            chat = request.user.get_current_chat

        if subscription is None and business_subscription is None and \
                request.user.get_day_requests >= config.FREE_REQUESTS_PER_DAY:
            return JsonResponse({'result': 'day limit'})

        from_subscription = True
        message = Message.objects.create(text=text, user=request.user, chat=chat)
        if sample_pk:
            message.sample = sample
            message.save()
        if text.lower().startswith('нарисуй'):
            data = {
                'Stable Diffusion': [get_stable_response, 'SD'],
                'Midjourney': [get_midjourney_response, 'MJ']
            }
            user_data = data[request.user.selected_img_ai]

            if business_subscription is not None and business_subscription.balance >= config.REQUEST_PRICE[user_data[1]]:
                business_subscription.balance -= config.REQUEST_PRICE[user_data[1]]
                business_subscription.save()
                from_subscription = False
            elif subscription is not None and \
                    getattr(subscription.tariff, f'requests_{user_data[1]}') > request.user.get_month_requests(user_data[1]):
                pass
            elif getattr(request.user, f'requests_{user_data[1]}') > 0:
                setattr(request.user, f'requests_{user_data[1]}', getattr(request.user, f'requests_{user_data[1]}') - 1)
                request.user.save()
                from_subscription = False
            else:
                message.delete()
                return JsonResponse({'result': 'month limit', 'ai': request.user.selected_img_ai})
            response = user_data[0](message, request.user, chat, from_subscription)
            ai = user_data[1]
        else:
            if request.FILES:
                if business_subscription is not None and business_subscription.balance >= config.REQUEST_PRICE['VS']:
                    business_subscription.balance -= config.REQUEST_PRICE['VS']
                    business_subscription.save()
                    from_subscription = False
                elif subscription is not None and subscription.tariff.requests_VS > request.user.get_month_requests('VS'):
                    pass
                elif request.user.requests_VS > 0:
                    request.user.requests_VS -= 1
                    request.user.save()
                    from_subscription = False
                else:
                    message.delete()
                    return JsonResponse({'result': 'month limit', 'ai': 'Vision'})
                file = request.FILES.get('file')
                current_gmt = time.gmtime()
                time_stamp = calendar.timegm(current_gmt)
                file_name = f'{time_stamp}-{uuid4().hex}.{file.name.split(".")[-1]}'
                file.name = file_name
                Attachment.objects.create(message=message, file=file)
                response = get_vision_response(message, request.user, chat, from_subscription)
                ai = 'VS'
            else:
                data = {
                    'GPT-3.5': [get_gpt35_response, 'GPT35'],
                    'GPT-4': [get_gpt4_response, 'GPT4']
                }
                selected_ai = data[request.user.selected_ai]
                if business_subscription is not None and business_subscription.balance >= config.REQUEST_PRICE[selected_ai[1]]:
                    business_subscription.balance -= config.REQUEST_PRICE[selected_ai[1]]
                    business_subscription.save()
                    from_subscription = False
                elif subscription is None or \
                        (subscription is not None and
                         (getattr(subscription.tariff, f'requests_{selected_ai[1]}')
                          + (0 if selected_ai[1] == 'GPT4' else subscription.tariff.requests_GPT4))
                         > (request.user.get_month_requests(selected_ai[1])
                            + (0 if selected_ai[1] == 'GPT35' else request.user.get_month_requests('GPT35')))):
                    pass
                elif getattr(request.user, f'requests_{selected_ai[1]}') > 0:
                    setattr(request.user, f'requests_{selected_ai[1]}',
                            getattr(request.user, f'requests_{selected_ai[1]}') - 1)
                    request.user.save()
                    from_subscription = False
                else:
                    message.delete()
                    return JsonResponse({'result': 'month limit', 'ai': request.user.selected_ai})
                response = selected_ai[0](message, request.user, chat, from_subscription)
                ai = 'GPT4' if subscription is not None and from_subscription and selected_ai[1] == 'GPT35' and subscription.tariff.requests_GPT35 == 0 else selected_ai[1]

        data = {'result': 'ok', 'response': response, 'avatar': request.user.username[0],
                'message_pk': message.pk, 'text': message.text, 'rest_requests':
                    {'key': f'request-{"sub" if from_subscription else "acc"}-{ai}',
                     'value': eval(f'request.user.get_month_{ai.lower()}')}}

        if is_new:
            data['chat_name'] = chat.get_name
            data['chat_pk'] = chat.pk

        attachment = message.get_attachment
        if message.get_attachment:
            data['attachment'] = attachment

        if sample_pk:
            data['sample'] = sample.name

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'result': 'failed'})


@login_required
def get_messages(request):
    chat_pk = int(request.GET.get('pk'))
    chat = Chat.objects.get(pk=chat_pk)
    chat.set_current()
    messages = [{'pk': m.pk, 'is_sender': m.is_sender, 'text': m.text, 'file': m.get_attachment,
                 'sample': m.sample.name if m.sample else None} for m in chat.get_messages()]
    return JsonResponse({'avatar': request.user.username[0], 'messages': messages})


@login_required
def delete_message(request):
    pk = int(request.POST.get('pk'))
    message = Message.objects.get(pk=pk)
    message.is_deleted = True
    message.save()
    return JsonResponse({'result': 'ok', 'is_sender': message.is_sender})


@login_required
def delete_chat(request):
    pk = int(request.POST.get('pk'))
    chat = Chat.objects.get(pk=pk)
    chat.is_deleted = True
    chat.is_current = False
    chat.save()
    return JsonResponse({'result': 'ok'})


@login_required
def return_message(request):
    pk = int(request.POST.get('pk'))
    message = Message.objects.get(pk=pk)
    message.is_deleted = False
    message.save()
    return JsonResponse({'result': 'ok'})


@login_required
def return_chat(request):
    pk = int(request.POST.get('pk'))
    chat = Chat.objects.get(pk=pk)
    chat.is_deleted = False
    chat.save()
    return JsonResponse({'result': 'ok', 'chat_name': chat.get_name})


@login_required
def select_ai(request):
    ai = request.POST.get('ai')
    is_img = request.POST.get('is_img')

    if is_img == 'true':
        request.user.selected_img_ai = ai
        request.user.save()
    else:
        request.user.selected_ai = ai
        request.user.save()

    return JsonResponse({'result': 'ok'})


@login_required
def get_sample(request):
    if request.check_samples:
        return JsonResponse({'result': 'failed'})

    pk = int(request.GET.get('pk'))
    sample = Sample.objects.get(pk=pk)
    return JsonResponse({'result': 'ok', 'name': sample.name, 'variables': sample.variables})


@login_required
def set_context(request):

    value = request.POST.get('value')
    user = User.objects.get(pk=request.user.pk)
    user.use_context = True if value == 'yes' else False
    user.save()
    return JsonResponse({'result': 'ok'})


@login_required
def enter_promo_code(request):
    promo_code = request.POST.get('promo_code')
    subscription = BusinessSubscription.objects.filter(promo_code=promo_code)
    if subscription.exists():
        user = request.user
        user.business_subscription = subscription.first()
        user.save()
        return JsonResponse({'result': 'ok'})
    return JsonResponse({'result': 'wrong'})


def calculate_signature(*args) -> str:
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def parse_response(request: str) -> dict:
    params = {}

    for item in urlparse(request).query.split('&'):
        key, value = item.split('=')
        params[key] = value
    return params


def check_signature_result(
    order_number: int,  # invoice number
    received_sum: decimal,  # cost of goods, RU
    received_signature: hex,  # SignatureValue
    password: str  # Merchant password
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)
    if signature.lower() == received_signature.lower():
        return True
    return False


# Формирование URL переадресации пользователя на оплату.

def generate_payment_link(request):

    subject = request.POST.get('subject')
    if subject in ['tariff', 'business', 'requests']:
        total_cost = 0
        details = {'subject': subject}
        if subject == 'tariff':
            try:
                tariff_pk = int(request.POST.get('tariff_pk'))
                details['tariff_pk'] = tariff_pk
                tariff = Tariff.objects.get(pk=tariff_pk)
                count = int(request.POST.get('count'))
                details['count'] = count
                total_cost += tariff.price * count
                description = f'Оплата тарифа "{tariff.name}" на сайте tochkagpt.ru'
            except (ValueError, ObjectDoesNotExist):
                return JsonResponse({'result': 'failed'})
        elif subject == 'business':
            try:
                cost = int(request.POST.get('cost'))
                details['cost'] = cost
                total_cost += cost
                description = 'Пополнение баланса по тарифу "Бизнес" на сайте tochkagpt.ru'
            except ValueError:
                return JsonResponse({'result': 'failed'})
        else:
            result = {}
            for r in json.loads(request.POST['requests']):
                ai = r['ai']
                quantity = r['quantity']
                if ai in config.REQUEST_PRICE.keys():
                    cost = round(quantity * config.REQUEST_PRICE[ai], 2)
                    total_cost += cost
                    result[ai] = {'quantity': quantity, 'cost': cost}
            details['requests'] = result
            description = 'Оплата дополнительных запросов на сайте tochkagpt.ru'

        if total_cost <= 0:
            return JsonResponse({'result': 'failed'})

        payment_operation = PaymentOperation.objects.create(user=request.user, cost=total_cost, details=details)

        signature = calculate_signature(
            config.ROBOKASSA_LOGIN,
            total_cost,
            payment_operation.pk,
            config.ROBOKASSA_PASSWORD_1
        )

        data = {
            'MerchantLogin': config.ROBOKASSA_LOGIN,
            'OutSum': total_cost,
            'InvId': payment_operation.pk,
            'Description': description,
            'SignatureValue': signature,
            'IsTest': 0
        }
        return JsonResponse({'result': 'ok', 'link': f'https://auth.robokassa.ru/Merchant/Index.aspx?{parse.urlencode(data)}'})
    else:
        return JsonResponse({'result': 'failed'})


# Получение уведомления об исполнении операции (ResultURL).
@csrf_exempt
def result_payment(request, merchant_password_2=config.ROBOKASSA_PASSWORD_2):
    param_request = request.POST
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']
    operation = PaymentOperation.objects.get(pk=number)
    print(param_request)
    print(cost)
    print(number)
    print(signature)
    print(operation)
    print(check_signature_result(number, cost, signature, merchant_password_2))
    print(not operation.status == 'S')
    if check_signature_result(number, cost, signature, merchant_password_2) and not operation.status == 'S':
        print(1)
        operation.status = 'S'
        operation.save()
        subject = operation.details['subject']
        user = User.objects.get(pk=operation.user.pk)
        if subject == 'tariff':
            subscription = user.get_subscription
            if subscription is not None and subscription.tariff.pk == operation.details['tariff_pk']:
                subscription.end_date += timedelta(days=30*operation.details['count'])
                subscription.save()
            else:
                if subscription is not None:
                    subscription.end_date = datetime.now(pytz.timezone(settings.TIME_ZONE))
                    subscription.save()
                Subscription.objects.create(user=user, tariff=Tariff.objects.get(pk=operation.details['tariff_pk']),
                                            end_date=datetime.now(pytz.timezone(settings.TIME_ZONE)) + timedelta(days=30*operation.details['count']))
        elif subject == 'business':
            business_subscription = user.business_subscription
            business_subscription.balance += operation.details['cost']
            business_subscription.save()
        else:
            for ai, value in operation.details['requests'].items():
                setattr(user, f'requests_{ai}',
                        getattr(user, f'requests_{ai}') + value['quantity'])
            user.save()

        return f'OK{param_request["InvId"]}'
    operation.status = 'F'
    operation.save()
    return "bad sign"


# Проверка параметров в скрипте завершения операции (SuccessURL).
@csrf_exempt
def check_success_payment(request, merchant_password_1=config.ROBOKASSA_PASSWORD_1):
    param_request = request.POST
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    if check_signature_result(number, cost, signature, merchant_password_1):
        return render(request, 'authentication/notification.html',
                      context={'notification': 'Оплата прошла успешно!'})
    return render(request, 'authentication/notification.html',
                  context={'notification': 'Что-то пошло не так :с'})


def fail_payment(request):
    return render(request, 'authentication/notification.html',
                  context={'notification': 'Оплата была отменена.'})