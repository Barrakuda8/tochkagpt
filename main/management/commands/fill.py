import json
import os.path

from django.core.management.base import BaseCommand
from tochkagpt import settings
from tochkagpt.settings import BASE_DIR
from chat.models import Tariff, NewChatSample, NewChatInstruction, NewChatCategory
from main.models import FAQ, FAQCategory


def load_from_json(file_name):
    with open(f'{settings.BASE_DIR}/json/{file_name}.json', 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):

        # if not Tariff.objects.all():
        #     for tariff in load_from_json('tariffs'):
        #         Tariff.objects.create(**tariff)
        #
        # if not NewChatCategory.objects.all():
        #     for cat in load_from_json('new_chat_categories'):
        #         NewChatCategory.objects.create(**cat)
        #
        # if not NewChatSample.objects.all():
        #     for sample in load_from_json('new_chat_samples'):
        #         if 'category' in sample.keys():
        #             sample['category'] = NewChatCategory.objects.get(name=sample['category'])
        #         if 'icon' in sample.keys():
        #             sample['icon'] = os.path.join('new_chat_icons', sample['icon'] + '.svg')
        #         NewChatSample.objects.create(**sample)
        #
        # if not NewChatInstruction.objects.all():
        #     for instruction in load_from_json('new_chat_instructions'):
        #         NewChatInstruction.objects.create(**instruction)

        if not FAQ.objects.all():
            for faq in load_from_json('faq'):
                FAQ.objects.create(**faq)
