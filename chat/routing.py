from django.urls import path, re_path
from .consumers import ChatConsumer, DeleteMessageConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_pk>\d+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/delete_message/(?P<chat_pk>\d+)/$', DeleteMessageConsumer.as_asgi()),
]