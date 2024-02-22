from django.urls import path
import chat.views as chat

app_name = 'chat'

urlpatterns = [
    path('', chat.index, name='index'),
    path('like_sample/', chat.like_sample, name='like_sample'),
    path('delete_sample/', chat.delete_sample, name='delete_sample'),
    path('unlike_sample/', chat.unlike_sample, name='unlike_sample'),
    path('create_sample/', chat.create_sample, name='create_sample'),
    path('handle_request/', chat.handle_request, name='handle_request'),
    path('get_messages/', chat.get_messages, name='get_messages'),
    path('delete_message/', chat.delete_message, name='delete_message'),
    path('delete_chat/', chat.delete_chat, name='delete_chat'),
    path('return_chat/', chat.return_chat, name='return_chat'),
    path('return_message/', chat.return_message, name='return_message'),
    path('select_ai/', chat.select_ai, name='select_ai'),
    path('get_sample/', chat.get_sample, name='get_sample'),
    path('set_context/', chat.set_context, name='set_context'),
]