from channels.routing import ProtocolTypeRouter , URLRouter
from channels.auth import AuthMiddlewareStack
import submission.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            submission.routing.websocket_urlpatterns
        )
    ),
})