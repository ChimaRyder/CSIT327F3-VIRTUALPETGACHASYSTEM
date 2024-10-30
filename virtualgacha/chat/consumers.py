import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatRoom, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.room_group_name = 'global_chat'

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        if self.user.is_authenticated:
            room, _ = ChatRoom.objects.get_or_create(type='global', name='Global Chat')
            msg = Message.objects.create(room=room, sender=self.user, content=message)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username,
                    'timestamp': msg.timestamp.isoformat()
                }
            )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))
