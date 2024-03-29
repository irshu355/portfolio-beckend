from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from ticker.models import UserProfile
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.template import loader
# Create your views here.


def index(request):
    # x = datetime(2018, 9, 15)
    # print(x.strftime("%b %d %Y %H:%M:%S"))
    template = loader.get_template('frontend/index.html')
    context = {
        'latest_question_list': 'Hi',
    }
    return HttpResponse(template.render({}, request))


def room(request, room_name):
    return render(request, 'frontend/room.html', {
        'room_name': room_name
    })


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        profile = UserProfile.objects.get(user=user.pk)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'tier': profile.tier
        })
