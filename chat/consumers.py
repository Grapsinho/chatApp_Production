import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        # Add the consumer to a group based on chat PK
        self.chat_pk = self.scope['url_route']['kwargs']['chat_pk']
        await self.channel_layer.group_add(
            f"chat_{self.chat_pk}",
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Disconnect from WebSocket
        await self.channel_layer.group_discard(
            f"chat_{self.chat_pk}",
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive a message from the WebSocket
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        sender_id = text_data_json['sender_id']

        # Create a new message
        message_id = await self.create_message(message_content, sender_id, self.chat_pk)

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            f"chat_{self.chat_pk}",
            {
                'type': 'chat_message',
                'message': message_content,
                'sender_id': sender_id,
                'message_id': message_id[0],
                'message_time': message_id[1],
                'sender_img': message_id[2],
            }
        )

    @sync_to_async
    def create_message(self, message_content, sender, chat):
        from .models import Message, Chat
        from users.models import User
        
        # Create a new message in the database
        chat = Chat.objects.get(pk=chat)
        sender = User.objects.get(pk=sender)

        if sender == chat.receiver:
            chat.sender_seen = False
            chat.save()
        else:
            chat.receiver_seen = False
            chat.save()

        message = Message.objects.create(
            content=message_content,
            chat=chat,
            sender=sender,
        )

        return [message.pk, message.timestamp.strftime('%m-%d %H:%M'), sender.avatar.url]

    async def chat_message(self, event):
        # Fetch additional information from the database
        message_id = event['message_id']
        sender_id = event['sender_id']
        message_time = event['message_time']
        sender_img = event['sender_img']
        
        # Prepare data to send back to the front end
        message_data = {
            'type': 'chat_message',
            'message_id': message_id,
            'message': event['message'],
            'sender_id': sender_id,
            'message_time': message_time,
            'sender_img': sender_img,
            'chat_id': self.chat_pk
        }
        
        # Send the message data to the WebSocket
        await self.send(text_data=json.dumps(message_data))

# delete message
class DeleteMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        # Add the consumer to a group based on chat PK
        self.chat_pk = self.scope['url_route']['kwargs']['chat_pk']
        await self.channel_layer.group_add(
            f"delete_message_chat_{self.chat_pk}",
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Disconnect from WebSocket
        await self.channel_layer.group_discard(
            f"delete_message_chat_{self.chat_pk}",
            self.channel_name
        )

    async def receive(self, text_data):
        load_data = json.loads(text_data)
        message_id = load_data['message_id']
        chat_pk = load_data['chat_pk']

        message_data = {
            'type': 'delete_message_info',
            "message_id": message_id,
            "chat_pk": chat_pk,
        }

        # Delete the message from the database
        await self.delete_message_from_db(message_data)

        # Broadcast the delete message event to the group
        await self.channel_layer.group_send(
            f"delete_message_chat_{message_data['chat_pk']}",
            {
                'type': 'delete_message_info',
                'message_id': message_data['message_id']
            }
        )

    @sync_to_async
    def delete_message_from_db(self, message_data):
        from .models import Message
        # Delete the message from the database
        Message.objects.get(id=message_data['message_id']).delete()
    
    async def delete_message_info(self, event):
        # Fetch additional information from the database
        from django.utils import timezone

        curr_time = timezone.now().strftime('%m-%d %H:%M')

        message_id = event['message_id']
        
        # Prepare data to send back to the front end
        message_data = {
            'type': 'delete_message_info',
            'del_time': curr_time,
            'new_text': 'User Deleted This Message',
            'message_id': message_id
        }
        
        # Send the message data to the WebSocket
        await self.send(text_data=json.dumps(message_data))

