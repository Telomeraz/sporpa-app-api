from typing import Any

import factory
import factory.django
import factory.fuzzy

from participants.models import ParticipationRequest, Player, PlayerSport, Sport, SportLevel


class SportLevelFactory(factory.django.DjangoModelFactory):
    level = factory.fuzzy.FuzzyChoice(SportLevel.Level.choices, getter=lambda c: c[0])

    class Meta:
        model = SportLevel
        django_get_or_create = ("level",)


class PlayerFactory(factory.django.DjangoModelFactory):
    sports = factory.RelatedFactoryList(
        "tests.participants.factories.PlayerSportFactory",
        factory_related_name="player",
    )

    class Meta:
        model = Player
        django_get_or_create = ("user",)

    @classmethod
    def _create(cls, model_class: Player, *args: Any, **kwargs: Any) -> Player:
        cls.sports.size = kwargs.pop("sports_size", 2)
        return super()._create(model_class, *args, **kwargs)


class PlayerSportFactory(factory.django.DjangoModelFactory):
    sport = factory.Iterator(Sport.objects.all())
    level = factory.SubFactory(
        "tests.participants.factories.SportLevelFactory",
    )

    class Meta:
        model = PlayerSport


class ParticipationRequestFactory(factory.django.DjangoModelFactory):
    message = factory.Faker("text", max_nb_chars=ParticipationRequest.message.field.max_length)

    class Meta:
        model = ParticipationRequest
