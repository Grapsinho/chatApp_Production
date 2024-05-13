from django.urls import path, include
from .views import *

urlpatterns = [
    path('get_chats_betweenUsers/', get_chats_betweenUsers, name='get_chats_betweenUsers'),
]