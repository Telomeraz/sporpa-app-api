from django.urls import path

from .views import PlayerSportCreateView, SportLevelListView, SportListView

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
    path(
        "player-sport/create/",
        PlayerSportCreateView.as_view(),
        name="player_sport_create",
    ),
]
