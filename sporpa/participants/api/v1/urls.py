from django.urls import path

from .views import SportLevelListView, SportListView

urlpatterns = [
    path(
        "sport-list/",
        SportListView.as_view(),
        name="sport_list",
    ),
    path(
        "sport-level-list/",
        SportLevelListView.as_view(),
        name="sport_level_list",
    ),
]
