from channels.routing import ProtocolTypeRouter , URLRouter
import submission.routing

application = ProtocolTypeRouter({
    'websocket': (
        URLRouter(
            submission.routing.websocket_urlpatterns
        )
    ),
})