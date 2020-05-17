import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from ticker.models import Ticker, WatchList, Option, Symbol, UserProfile
from rest_framework.authtoken.models import Token


class QuoteConsumer(WebsocketConsumer):
    def connect(self):
        self.token = self.scope['url_route']['kwargs']['username']
        user = Token.objects.get(key=self.token).user
        watchList = WatchList.objects.filter(owner__user=user)
        self.room_group_name = "BA"
        for rec in watchList:
            async_to_sync(self.channel_layer.group_add)(
                rec.ticker.symbol,
                self.channel_name
            )

        # self.room_group_name = 'chat_%s' % self.room_name

        # # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group

        user = Token.objects.get(key=self.token).user
        watchList = WatchList.objects.filter(owner__user=user)
        for rec in watchList:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'quote_message',
                'message': message
            }
        )

    # Receive message from room group
    def quote_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'stock-quote',
            'ticker': message
        }))
