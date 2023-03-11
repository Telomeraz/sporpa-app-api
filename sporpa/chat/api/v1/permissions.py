from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from events.models import Activity


class ActivityMessagePermission(permissions.BasePermission):
    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        return Activity.objects.filter(
            pk=view.kwargs[view.lookup_field],
            players=request.user.player,
        ).exists()
