import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.db.models import Q

class LiveSearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.current_search_query = ""

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        search_query = text_data.strip()

        if search_query:
            search_results = await self.perform_product_search(search_query)  # Use await here

            result_data = []

            for i in search_results:
                result_data.append(i)

            await self.send(text_data=json.dumps({
                'search_results': result_data
            }))
        else:
            await self.send(text_data=json.dumps({
                'search_results': 'search query is empty'
            }))
        

    @sync_to_async
    def perform_product_search(self, search_query):
        from users.models import User
        # Use the sync_to_async decorator for the synchronous database query
        return list(User.objects.filter(full_name__icontains=search_query).values("full_name", "avatar", 'pk', 'email')[:6])