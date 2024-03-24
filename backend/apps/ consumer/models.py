import json

from Scripts.activate_this import path
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

from models import consumers


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None

    async def connect(self):
        self.room_name = 'chat'
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

        application = ProtocolTypeRouter({
            'websocket': URLRouter([
                path('ws/chat/', consumers.ChatConsumer.as_asgi()),
            ]),
        })
