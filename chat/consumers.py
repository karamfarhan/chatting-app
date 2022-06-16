from channels.generic.websocket import AsyncWebsocketConsumer
import json
import datetime
from .models import ChatRoom, Message,Contact
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat-{self.room_name}"
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send( 
            self.room_group_name,
            {
                'type':'send_notification',
                'msg_type':'notify',
                'username':self.user.username,
                'message': f'{self.user.username} joined the chat',
                'date': datetime.datetime.now().strftime("%I:%M %p | %d %b %Y")
            }
        )
        await self.accept()


    

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
 

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        image_url = text_data_json['image_url']
        date_now = datetime.datetime.now().strftime("%I:%M %p | %d %b %Y")
        await self.save_message(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_messages',
                'msg_type':'con',
                'message': message,
                'username': username,
                'image_url':image_url,
                'date': date_now,
            }
        )
    async def send_messages(self,event):
        message = event['message']
        msg_type = event['msg_type']
        username = event['username']
        image_url = event['image_url']
        date = event['date']
        await self.send(text_data=json.dumps({
            'msg_type':msg_type,
            'message': message,
            'username': username,
            'image_url':image_url,
            'date': date,
        }))

    async def send_notification(self,event):
        message = event['message']
        msg_type = event['msg_type']
        username = event['username']
        date = event['date']
        await self.send(text_data=json.dumps({
            'msg_type': msg_type,
            'username': username,
            'message': message,
            'date': date,
        }))
    @database_sync_to_async
    def save_message(self,data):
        contact = Contact.objects.get(user__username=data['username'])
        room = ChatRoom.objects.get(id=data['room'])
        new_message = Message.objects.create(
            contact=contact,
            room=room,
            text=data['message'],

        )
        new_message.save()