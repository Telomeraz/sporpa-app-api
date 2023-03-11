from django.urls import path

from .views import ActivityMessageListView

app_name = "chat"
urlpatterns = [
    path(
        "activity-messages/<int:activity_pk>/",
        ActivityMessageListView.as_view(),
        name="activity_messages",
    ),
]
