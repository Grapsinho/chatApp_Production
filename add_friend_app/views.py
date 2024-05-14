from django.shortcuts import render
from django.http import JsonResponse
from users.models import FriendRequest, User, Friendship
from chat.models import Chat, Message
# Create your views here.

def sendFriendRequest(request):
    """
    View to send friend request.
    """

    receiver_user_id = request.POST.get('user_id')
    receiver_user = User.objects.get(pk=receiver_user_id)

    try:
        FriendRequest.objects.create(
            sender=request.user,
            receiver=receiver_user
        )
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False}, status=404)
    
def approve_friend_request(request):
    """
    View to accept friend request.
    """

    sender_user_id = request.POST.get('user_id')
    sender_user = User.objects.get(pk=sender_user_id)
    receiver = request.user

    try:
        Friendship.objects.create(user=sender_user, friend=receiver)
        Friendship.objects.create(user=receiver, friend=sender_user)

        curChat = Chat.objects.get_or_create(
            sender=sender_user,
            receiver=receiver,
        )

        Message.objects.create(
            content=f"Greetings from {sender_user.full_name}",
            chat=curChat[0],
            sender=sender_user,
        )

        friendrequest_model = FriendRequest.objects.get(sender=sender_user, receiver=receiver)
        friendrequest_model.accepted = True
        friendrequest_model.save()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False}, status=404)
    
def decline_friend_request(request):
    """
    View to decline friend request.
    """

    sender_user_id = request.POST.get('user_id')
    sender_user = User.objects.get(pk=sender_user_id)
    receiver = request.user

    try:
        friendrequest_model = FriendRequest.objects.get(sender=sender_user, receiver=receiver)
        friendrequest_model.rejected = True
        friendrequest_model.save()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False}, status=404)
    
def delete_friend_request(request):
    """
    View to delete friend request.
    """

    req_id = request.POST.get('id')

    try:
        friendrequest_model = FriendRequest.objects.get(pk=req_id)
        friendrequest_model.delete()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False}, status=404)
    
def remove_from_friend(request):
    """
    View to delete friend.
    """

    user_we_want_to_unfriend = request.POST.get('user_id')
    user_we_want_to_unfriend_user = User.objects.get(pk=user_we_want_to_unfriend)

    try:
        Friendship.objects.get(user=request.user, friend=user_we_want_to_unfriend_user).delete()
        Friendship.objects.get(user=user_we_want_to_unfriend_user, friend=request.user).delete()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False}, status=404)