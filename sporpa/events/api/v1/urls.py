from django.urls import path

from .views import ActivityView

app_name = "events"
urlpatterns = [
    path(
        "activities/",
        ActivityView.as_view(),
        name="activities",
    ),
]
