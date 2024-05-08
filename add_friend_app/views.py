from django.shortcuts import render
from django.http import JsonResponse
from users.models import FriendRequest, User, Friendship

# Create your views here.

def sendFriendRequest(request):
    """
    View to send friend request.
    """

    # Get the product ID from the POST data
    receiver_user_id = request.POST.get('user_id')
    receiver_user = User.objects.get(pk=receiver_user_id)

    # Find the cart item associated with the product and the user's cart
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

    # Get the product ID from the POST data
    sender_user_id = request.POST.get('user_id')
    sender_user = User.objects.get(pk=sender_user_id)
    receiver = request.user

    # Find the cart item associated with the product and the user's cart
    try:
        Friendship.objects.create(user=sender_user, friend=receiver)
        Friendship.objects.create(user=receiver, friend=sender_user)

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

    # Get the product ID from the POST data
    sender_user_id = request.POST.get('user_id')
    sender_user = User.objects.get(pk=sender_user_id)
    receiver = request.user

    # Find the cart item associated with the product and the user's cart
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

    # Get the product ID from the POST data
    req_id = request.POST.get('id')

    # Find the cart item associated with the product and the user's cart
    try:
        friendrequest_model = FriendRequest.objects.get(pk=req_id)
        friendrequest_model.delete()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False}, status=404)