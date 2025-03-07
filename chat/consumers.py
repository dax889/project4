import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = data['user']
        room = data['room']

        # Save message in DB
        await self.save_message(user, room, message)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "user": user}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"], "user": event["user"]}))

    @staticmethod
    async def save_message(user, room, message):
        Message.objects.create(user=user, room=room, content=message)
