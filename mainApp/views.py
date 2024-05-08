from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import FriendRequest, User, Friendship

# Create your views here.

@login_required(login_url='login')
def home(request):
    """
    View function for home page of site.
    """

    user = User.objects.get(email=request.user)

    requests_for_user = FriendRequest.objects.filter(receiver=user, rejected=False, accepted=False).values('rejected', 'accepted', 'sender__full_name', "sender__avatar", 'sender__pk', 'sender__email')

    declined_requests = FriendRequest.objects.filter(sender=user, rejected=True).values('receiver__full_name', 'pk')
    accepted_requests = FriendRequest.objects.filter(sender=user, accepted=True).values('receiver__full_name', 'pk')

    message_len = len(requests_for_user) + len(declined_requests) + len(accepted_requests)

    context = {
        'friend_requests': requests_for_user,
        'friend_requests_count': message_len,
        'accepted_requests': accepted_requests,
        "declined_requests": declined_requests
    }

    return render(request, 'mainApp/home.html', context)

@login_required(login_url='login')
def profile(request, email):
    """
    View function for profile page.
    """

    user = User.objects.get(email=email)

    # this is for user who received friend request
    requests_for_user = FriendRequest.objects.filter(receiver=request.user, rejected=False, accepted=False).values('sender__email')
    
    bool_friend = False
    bool_friend2 = False

    # this is user sent requests
    sent_requests = FriendRequest.objects.filter(sender=request.user, rejected=False, accepted=False).values('receiver__email')

    # if request that user sent is equal to user whos page we are now then bool will be True
    for j in sent_requests:
        if j['receiver__email'] == email:
            bool_friend2 = True

    # if user received request bool friend will be True
    for i in requests_for_user:
        if email == i['sender__email']:
            bool_friend = True

    friends = user.friends.all()

    context = {
        'user': user,
        'friends': friends,
        "bool_friend": bool_friend,
        "bool_friend2": bool_friend2,
    }

    return render(request, 'mainApp/profile.html', context)