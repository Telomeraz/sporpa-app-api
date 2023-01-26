import random
from typing import Any, Sequence

import factory
import factory.django

from events.models import Activity
from participants.models import Player, PlayerSport, SportLevel


class ActivityFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    about = factory.Faker("text", max_nb_chars=Activity.about.field.max_length)
    available_between_at = factory.List(
        params=(
            factory.Faker("date_time_between", start_date="+1d", end_date="+15d"),
            factory.Faker("date_time_between", start_date="+16d", end_date="+30d"),
        ),
    )

    class Meta:
        model = Activity

    @classmethod
    def _create(cls, model_class: Activity, *args: Any, **kwargs: Any) -> Activity:
        participants: Sequence[Player] = kwargs.pop("participants", ())
        organizer: Player = kwargs["organizer"]
        player_sport: PlayerSport = kwargs.pop(
            "player_sport",
            random.choice(organizer.sports.all()),
        )

        sport = player_sport.sport
        kwargs["sport"] = sport

        sport_levels = set(
            kwargs.pop(
                "levels",
                random.sample(
                    list(SportLevel.objects.all()),
                    k=random.randint(0, SportLevel.objects.count()),
                ),
            ),
        )
        sport_levels.add(player_sport.level)
        for participant in participants:
            sport_levels.add(participant.sports.get(sport=sport).level)

        if "player_limit" not in kwargs:
            min_value = max(Activity.player_limit.field.validators[0].limit_value, len(participants) + 1)
            max_value: int = Activity.player_limit.field.validators[1].limit_value
            kwargs["player_limit"] = random.randint(min_value, max_value)

        activity: Activity = super()._create(model_class, *args, **kwargs)
        activity.levels.set(sport_levels)
        activity.players.add(*participants)
        return activity
