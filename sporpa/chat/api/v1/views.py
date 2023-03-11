from rest_framework import generics
from rest_framework.settings import api_settings

from django.db.models import QuerySet

from chat.models import ActivityMessage

from .paginations import MessageCursorPagination
from .permissions import ActivityMessagePermission
from .serializers import ActivityMessageListSerializer


class ActivityMessageListView(generics.ListAPIView):
    pagination_class = MessageCursorPagination
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ActivityMessagePermission]
    serializer_class = ActivityMessageListSerializer
    lookup_field = "activity_pk"

    def get_queryset(self) -> QuerySet[ActivityMessage]:
        activity_pk = self.kwargs[self.lookup_field]
        return ActivityMessage.objects.filter(activity=activity_pk)
