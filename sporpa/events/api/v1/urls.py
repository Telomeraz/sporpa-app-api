from django.urls import path

from .views import ActivityUpdateView, ActivityView

app_name = "events"
urlpatterns = [
    path(
        "activities/",
        ActivityView.as_view(),
        name="activities",
    ),
    path(
        "activities/<int:pk>/",
        ActivityUpdateView.as_view(),
        name="activities_update",
    ),
]
