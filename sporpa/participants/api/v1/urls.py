from django.urls import path

from .views import PlayerSportCreateView, PlayerSportUpdateView, SportLevelListView, SportListView

app_name = "participants"
urlpatterns = [
    path(
        "sports/",
        SportListView.as_view(),
        name="sports",
    ),
    path(
        "sport-levels/",
        SportLevelListView.as_view(),
        name="sport_levels",
    ),
    path(
        "player-sports/",
        PlayerSportCreateView.as_view(),
        name="player_sports",
    ),
    path(
        "player-sports/<int:sport_pk>/level/",
        PlayerSportUpdateView.as_view(),
        name="player_sports_update_level",
    ),
]
