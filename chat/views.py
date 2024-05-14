from django.shortcuts import render
from django.http import JsonResponse
from .models import Chat, Message
from django.shortcuts import get_object_or_404

# Create your views here.

def get_chats_betweenUsers(request):
    """
    View to get chat messages.
    """

    # Get chat_id from the request
    chat_id = request.GET.get('id')
    # Get chat instance, using get_object_or_404 for safety
    chat = get_object_or_404(Chat, pk=chat_id)

    # Initialize context and chat_messages dictionary
    context = {}
    chat_messages = {'my': [], 'friend': []}

    # Determine which user's information to include in the context
    if chat.sender != request.user:
        context = {
            'user_full_name': chat.sender.full_name,
            'img_url': chat.sender.avatar.url,
            'email': chat.sender.email
        }
    else:
        context = {
            'user_full_name': chat.receiver.full_name,
            'img_url': chat.receiver.avatar.url,
            'email': chat.receiver.email
        }

    # Process messages
    try:
        messages = chat.messages.all()
        for message in messages:
            message_info = [message.content, message.timestamp.strftime('%m-%d %H:%M'), message.timestamp, message.sender.avatar.url, message.pk]
            if message.sender == request.user:
                chat_messages['my'].append(message_info)
            else:
                chat_messages['friend'].append(message_info)

        # Include chat_messages in the response
        return JsonResponse({
            'top_info': context,
            'chat_messages': chat_messages,
            'success': True
        })
    except Exception as e:
        # Log unexpected exceptions and return generic error response
        print(f"An unexpected error occurred: {e}")
        return JsonResponse({'success': False, 'message': 'An unexpected error occurred'}, status=500)
    
