import hashlib
from datetime import datetime
import pytz
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

import config
from chat.models import NewChatSample
from tochkagpt import settings
from .forms import UserLoginForm, UserRegisterForm, UserPasswordChangeForm
from tochkagpt.settings import BASE_URL
from .models import User


def login(request):
    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(reverse('admin:index'))
            else:
                return HttpResponseRedirect(reverse('chat:index'))

    context = {
        'title': 'Чат',
        'login_form': login_form,
        'register_form': UserRegisterForm(),
        'action': 'login',
        'new_chat_samples_1': NewChatSample.objects.filter(category__isnull=True, section='1').order_by('pk'),
        'new_chat_samples_2': NewChatSample.objects.filter(category__isnull=True, section='2').order_by('pk'),
    }

    return render(request, 'chat/chat.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('chat:index'))


def registration(request):
    if request.method == 'POST':
        registration_form = UserRegisterForm(request.POST, request.FILES)
        if registration_form.is_valid():
            user = registration_form.save()
            if not BASE_URL == 'http://127.0.0.1:8000':
                send_verify_email(user)
            user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password1'))
            if user:
                auth.login(request, user)
            return HttpResponseRedirect(reverse('chat:index'))
    else:
        registration_form = UserRegisterForm()

    context = {
        'title': 'Чат',
        'register_form': registration_form,
        'login_form': UserLoginForm(),
        'action': 'register',
        'new_chat_samples_1': NewChatSample.objects.filter(category__isnull=True, section='1').order_by('pk'),
        'new_chat_samples_2': NewChatSample.objects.filter(category__isnull=True, section='2').order_by('pk'),
    }
    return render(request, 'chat/chat.html', context)


def verify(request, email, key):
    user = get_object_or_404(User, email=email)
    if user:
        if key == user.verification_key and not user.is_verification_key_expired:
            user.email_verified = True
            user.verification_key = None
            user.verification_key_expires = None
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authentication/notification.html',
                          context={'notification': 'Почта успешно подтверждена!'})
    return render(request, 'authentication/notification.html',
                  context={'notification': 'Что-то пошло не так! Попробуйте отправить письмо повторно '
                                           'или обновить ключ подтверждения через личный кабинет.'})


def send_verify_email(user):
    verify_link = reverse('authentication:verify', args=[user.email, user.verification_key])
    full_link = f'{settings.BASE_URL}{verify_link}'
    try:
        message_beginning = config.EMAIL_VERIFICATION_MESSAGE_BEGINNING
    except ObjectDoesNotExist:
        message_beginning = 'Здравствуйте,\n\nПерейдите по ссылке, чтобы подтвердить свой адрес электронной почты:'
    try:
        message_ending = config.EMAIL_VERIFICATION_MESSAGE_ENDING
    except ObjectDoesNotExist:
        message_ending = '\n\nС уважением'

    message = f'{message_beginning} {full_link} {message_ending}'
    return send_mail(
        'Подтверждение почты',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )


@login_required
def renew_verification_key(request):
    user = request.user
    if user.is_verification_key_expired:
        user.verification_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
        user.verification_key_expires = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()
    send_verify_email(request.user)
    return render(request, 'authentication/notification.html',
                  context={'notification': 'Письмо со ссылкой для подтверждения адреса электронной почты '
                                           'было успешно отправлено!'})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('chat:index'))
    else:
        form = UserPasswordChangeForm(request.user)

    context = {
        'title': 'Смена пароля',
        'form': form,
    }

    return render(request, 'authentication/change_password.html', context=context)


@login_required
def delete_account(request):
    user = User.objects.get(pk=request.user.pk)
    user.delete()

    return HttpResponseRedirect(reverse('chat:index'))
