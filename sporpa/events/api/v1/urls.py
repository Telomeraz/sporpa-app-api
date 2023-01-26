from django.urls import path

from .views import ActivityCreateView, ActivityUpdateView

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
]
