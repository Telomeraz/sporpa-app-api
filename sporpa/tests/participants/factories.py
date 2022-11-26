import factory
import factory.django
import factory.fuzzy

from participants.models import Player, PlayerSport, Sport, SportLevel


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


class PlayerSportFactory(factory.django.DjangoModelFactory):
    sport = factory.Iterator(Sport.objects.all())
    level = factory.SubFactory(
        "tests.participants.factories.SportLevelFactory",
    )

    class Meta:
        model = PlayerSport
