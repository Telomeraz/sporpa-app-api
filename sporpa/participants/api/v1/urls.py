from django.urls import path

from .views import SportListView

urlpatterns = [
    path(
        "sport-list/",
        SportListView.as_view(),
        name="sport_list",
    ),
]
