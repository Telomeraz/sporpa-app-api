from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("chat/<int:activity_pk>/", consumers.ActivityMessageConsumer.as_asgi()),
]
