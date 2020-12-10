from django.urls import re_path
from django.conf.urls import url

from chat.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    url(r'ws/chat/(?P<room_name>\w+)', ChatConsumer.as_asgi()),
]