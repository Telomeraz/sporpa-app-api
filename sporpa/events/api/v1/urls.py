from django.urls import path

from .views import ActivityCreateView, ActivityUpdateView, ParticipationRequestListView

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
        "participation-requests/<int:activity_pk>/",
        ParticipationRequestListView.as_view(),
        name="participation_requests",
    ),
]
