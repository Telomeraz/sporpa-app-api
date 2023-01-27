from django.urls import path, re_path

from .views import (
    ActivityCreateView,
    ActivityUpdateView,
    ParticipationRequestApprovalView,
    ParticipationRequestListView,
)

app_name = "events"
urlpatterns = [
    path(
        "activities/",
        ActivityCreateView.as_view(),
        name="activities",
    ),
    path(
        "activities/<int:pk>/",
        ActivityUpdateView.as_view(),
        name="activities_update",
    ),
    path(
        "activities/<int:activity_pk>/participation-requests/",
        ParticipationRequestListView.as_view(),
        name="participation_requests",
    ),
    re_path(
        r"^participation-requests/(?P<pk>\d+)/(?P<result>accept|reject)/$",
        ParticipationRequestApprovalView.as_view(),
        name="participation_requests_approval",
    ),
]
