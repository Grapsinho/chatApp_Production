from django.urls import path, include
from .views import *

urlpatterns = [
    path('friend_request/', sendFriendRequest, name='sendFriendRequest'),
    path('approve_friend_request/', approve_friend_request, name='approve_friend_request'),
    path('decline_friend_request/', decline_friend_request, name='decline_friend_request'),
    path('delete_friend_request/', delete_friend_request, name='delete_friend_request')
]