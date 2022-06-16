from django.urls import path
from .consumers import ChatConsumer
from django.urls import re_path


ws_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$',ChatConsumer.as_asgi()),
]