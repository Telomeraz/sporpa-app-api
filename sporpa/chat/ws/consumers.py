import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.api.v1.serializers import ActivityMessageListSerializer
from chat.models import ActivityMessage
from events.models import Activity


class ActivityMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        self.user = self.scope.get("user")
        if not self.user or not self.user.pk:
            await self.close()

        activity_pk = self.scope["url_route"]["kwargs"]["activity_pk"]
        try:
            self.activity = await Activity.objects.aget(
                pk=activity_pk,
                players=self.user.player,
            )
            self.activity_chat_group_name = f"activity_chat_{self.activity.pk}"

            await self.channel_layer.group_add(
                self.activity_chat_group_name,
                self.channel_name,
            )
            await self.accept()
        except Activity.DoesNotExist:
            await self.close()

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(
            self.activity_chat_group_name,
            self.channel_name,
        )

    async def receive(self, text_data: str) -> None:
        data = json.loads(text_data)
        message = data["message"]

        activity_message = await ActivityMessage.objects.acreate(
            sender=self.user,
            activity=self.activity,
            content=message,
        )
        serializer = ActivityMessageListSerializer(instance=activity_message)

        await self.channel_layer.group_send(
            self.activity_chat_group_name,
            {"type": "chat_message", "activity_message": serializer.data},
        )

    async def chat_message(self, event: dict) -> None:
        await self.send(text_data=json.dumps(event["activity_message"]))
