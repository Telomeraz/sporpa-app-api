import random

import pytest
from faker import Faker

from django.core.exceptions import ValidationError

from accounts.models import User
from events.models import Activity
from participants.models import ParticipationRequest, Player, PlayerSport, Sport, SportLevel

fake = Faker()
pytestmark = pytest.mark.django_db


class TestActivityManager:
    def test_create(self, user: User) -> None:
        player_sport: PlayerSport = user.player.sports.first()
        sport: Sport = player_sport.sport
        sport_levels: set[SportLevel] = set(
            random.sample(
                list(SportLevel.objects.all()),
                k=random.randint(0, SportLevel.objects.count()),
            ),
        )
        sport_levels.add(player_sport.level)
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = (
            fake.date_time_between(start_date="+1d", end_date="+15d"),
            fake.date_time_between(start_date="+16d", end_date="+30d"),
        )

        data = {
            "organizer": user.player,
            "name": name,
            "about": about,
            "sport": sport,
            "available_between_at": available_between_at,
        }
        activity = Activity.objects.create(**data)
        activity.levels.set(sport_levels)

        assert activity.pk
        assert activity.players.get(activity_players__is_organizer=True) == user.player
        assert activity.name == name
        assert activity.about == about
        assert activity.sport == sport
        assert list(activity.levels.all()) == list(sport_levels)
        assert activity.available_between_at == available_between_at
        assert Activity.objects.count() == 1

    def test_create_when_activity_does_not_have_organizer(self, user: User) -> None:
        player_sport: PlayerSport = user.player.sports.first()
        sport: Sport = player_sport.sport
        sport_levels: set[SportLevel] = set(
            random.sample(
                list(SportLevel.objects.all()),
                k=random.randint(0, SportLevel.objects.count()),
            ),
        )
        sport_levels.add(player_sport.level)
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = (
            fake.date_time_between(start_date="+1d", end_date="+15d"),
            fake.date_time_between(start_date="+16d", end_date="+30d"),
        )

        data = {
            "name": name,
            "about": about,
            "sport": sport,
            "available_between_at": available_between_at,
        }
        with pytest.raises(KeyError):
            Activity.objects.create(**data)


class TestActivityQueryset:
    @pytest.mark.parametrize(
        "activities_with_participants",
        [{"total_activities": 3, "total_participants": 3}],
        indirect=["activities_with_participants"],
    )
    def test_filter_organizer(self, user: User, activities_with_participants: list[Activity]) -> None:
        organizer = user.player
        activities = Activity.objects.filter_organizer(organizer)

        assert activities.count() == 3
        assert list(activities) == list(activities_with_participants)

    @pytest.mark.parametrize(
        "activities_with_participants",
        [{"total_activities": 7, "total_participants": 2}],
        indirect=["activities_with_participants"],
    )
    def test_filter_available(self, activities_with_participants: list[Activity]) -> None:
        participant = activities_with_participants[0].participants[0]
        activities = Activity.objects.filter_available(participant)

        assert activities.count() == 6
        assert list(activities) == list(activities_with_participants[1:])

    @pytest.mark.parametrize(
        "activities_with_participants",
        [{"total_activities": 4, "total_participants": 2}],
        indirect=["activities_with_participants"],
    )
    def test_filter_participant(self, activities_with_participants: list[Activity]) -> None:
        participant = activities_with_participants[0].participants[0]
        activities = Activity.objects.filter_participant(participant)

        assert activities.count() == 1
        assert list(activities) == list(activities_with_participants[:1])


class TestActivity:
    def test_str(self, activity_without_participants: Activity) -> None:
        assert str(activity_without_participants) == activity_without_participants.name

    def test_organizer(self, activity_without_participants: Activity) -> None:
        assert activity_without_participants.organizer == Player.objects.get(
            activity_players__is_organizer=True,
            activities=activity_without_participants,
        )

    def test_participants(self, activity_with_participants: Activity) -> None:
        assert list(activity_with_participants.participants) == list(
            Player.objects.filter(
                activity_players__is_organizer=False,
                activities=activity_with_participants,
            ),
        )

    @pytest.mark.parametrize(
        "activity_with_participants",
        [{"player_limit": 10}],
        indirect=["activity_with_participants"],
    )
    def test_check_player_limit(self, user2: User, activity_with_participants: Activity) -> None:
        activity_with_participants.check_player_limit(total_players=3)

    @pytest.mark.parametrize(
        "activity_with_participants",
        [{"player_limit": 2}],
        indirect=["activity_with_participants"],
    )
    def test_check_player_limit_when_player_limit_is_less(
        self,
        activity_with_participants: Activity,
    ) -> None:
        with pytest.raises(ValidationError, match="Player limit cannot be less than total players."):
            activity_with_participants.check_player_limit(total_players=3)

    @pytest.mark.parametrize(
        "user, user2",
        [
            (
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 5},
            ),
        ],
        indirect=["user", "user2"],
    )
    def test_check_participant(self, user2: User, activity_without_participants: Activity) -> None:
        activity_without_participants.check_participant(participant=user2.player)

    @pytest.mark.parametrize(
        "user, user2, activity_without_participants",
        [
            (
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"status": 2},
            ),
        ],
        indirect=["user", "user2", "activity_without_participants"],
    )
    def test_check_participant_when_activity_status_is_not_updatable(
        self,
        user2: User,
        activity_without_participants: Activity,
    ) -> None:
        with pytest.raises(ValidationError, match="The activity is already played."):
            activity_without_participants.check_participant(participant=user2.player)

    @pytest.mark.parametrize(
        "user, user2, activity_with_participants",
        [
            (
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"player_limit": 2},
            ),
        ],
        indirect=["user", "user2", "activity_with_participants"],
    )
    def test_check_participant_when_activity_is_fully_booked(
        self,
        user2: User,
        activity_with_participants: Activity,
    ) -> None:
        with pytest.raises(ValidationError, match="The activity is fully booked."):
            activity_with_participants.check_participant(participant=user2.player)

    @pytest.mark.parametrize(
        "user, activity_without_participants",
        [
            (
                {"player__sports__level_id": 5, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"player_limit": 2},
            ),
        ],
        indirect=["user", "activity_without_participants"],
    )
    def test_check_participant_when_organizer_is_participant(
        self,
        activity_without_participants: Activity,
    ) -> None:
        with pytest.raises(ValidationError, match="You cannot send a participation request to your own activity."):
            activity_without_participants.check_participant(participant=activity_without_participants.organizer)

    @pytest.mark.parametrize(
        "user, activity_without_participants",
        [
            (
                {"player__sports__level_id": 5, "player_sports_size": 1, "player__sports__sport_id": 2},
                {"player_limit": 2},
            ),
        ],
        indirect=["user", "activity_without_participants"],
    )
    def test_check_participant_when_participant_does_not_have_sport(
        self,
        user_without_sport: User,
        activity_without_participants: Activity,
    ) -> None:
        with pytest.raises(ValidationError, match="The player does not have Basketball record."):
            activity_without_participants.check_participant(participant=user_without_sport.player)

    @pytest.mark.parametrize(
        "user, user2, activity_without_participants",
        [
            (
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"player__sports__level_id": 1, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"levels": (4,)},
            ),
        ],
        indirect=["user", "user2", "activity_without_participants"],
    )
    def test_check_participant_when_participant_level_is_not_eligible(
        self,
        user2: User,
        activity_without_participants: Activity,
    ) -> None:
        with pytest.raises(ValidationError, match="Your level is not eligible for the activity."):
            activity_without_participants.check_participant(participant=user2.player)

    def test_accept_participation_request(self, participation_request: ParticipationRequest) -> None:
        activity = participation_request.activity
        participant = participation_request.participant

        activity.accept_participation_request(participation_request)

        assert activity.players.contains(participant)
        with pytest.raises(ParticipationRequest.DoesNotExist):
            participation_request.refresh_from_db()

    def test_reject_participation_request(self, participation_request: ParticipationRequest) -> None:
        activity = participation_request.activity
        participant = participation_request.participant

        activity.reject_participation_request(participation_request)

        assert not activity.players.contains(participant)
        with pytest.raises(ParticipationRequest.DoesNotExist):
            participation_request.refresh_from_db()


class TestActivityLevel:
    def test_str(self, activity_without_participants: Activity) -> None:
        activity_level = activity_without_participants.activity_levels.first()
        assert str(activity_level) == f"{activity_without_participants} - {activity_level.level.get_level_display()}"


class TestActivityPlayer:
    def test_str(self, user: User, activity_without_participants: Activity) -> None:
        activity_player = activity_without_participants.activity_players.first()
        assert str(activity_player) == f"{activity_without_participants} - {user.email}"
