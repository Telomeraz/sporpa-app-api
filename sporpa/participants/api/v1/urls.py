from django.urls import path

from .views import PlayerSportUpdateLevelView, PlayerSportView, SportLevelView, SportView

app_name = "participants"
urlpatterns = [
    path(
        "sports/",
        SportView.as_view(),
        name="sports",
    ),
    path(
        "sport-levels/",
        SportLevelView.as_view(),
        name="sport_levels",
    ),
    path(
        "player-sports/",
        PlayerSportView.as_view(),
        name="player_sports",
    ),
    path(
        "player-sports/<int:sport_id>/level/",
        PlayerSportUpdateLevelView.as_view(),
        name="player_sports_update_level",
    ),
]
