import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from ticker.models import Ticker, WatchList, Option, Symbol, UserProfile
from rest_framework.authtoken.models import Token
from django.http import Http404


class QuoteConsumer(WebsocketConsumer):
    def connect(self):
        self.token = self.scope['url_route']['kwargs']['username']
        user = Token.objects.get(key=self.token).user
        watchList = WatchList.objects.filter(owner__user=user)
        for rec in watchList:
            async_to_sync(self.channel_layer.group_add)(
                rec.ticker.symbol,
                self.channel_name
            )

        self.markUserOnline(user, 1)

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
                rec.ticker.symbol,
                self.channel_name
            )

        self.markUserOnline(user, 0)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("message received {}".format(message))
        # # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'quote_message',
        #         'message': message
        #     }
        # )

    # transmit quotes refresh
    def quote_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'stock-quote',
            'ticker': message
        }))

    # transmit options refresh

    def options_refresh_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'options-refresh',
            'options_refresh': message
        }))

    def historical_loaded_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'historical-loaded',
            'historical_loaded': message
        }))

    def markUserOnline(self, user, status):
        try:
            profile = UserProfile.objects.get(user=user.id)
            profile.is_online = status
            profile.save()
        except UserProfile.DoesNotExist:
            return Http404
