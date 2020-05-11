from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
import ticker.routing
application = ProtocolTypeRouter({
    # empty for now, django.views  ia added by default
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                ticker.routing.websocket_urlpatterns
            )
        )
    )
})
