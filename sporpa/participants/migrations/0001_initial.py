# Generated by Django 4.1.2 on 2022-11-13 18:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def generate_sports(apps, schema_editor):
    Sport = apps.get_model("participants", "Sport")
    sports = (Sport(name=choice[0]) for choice in Sport.name.field.choices)
    Sport.objects.bulk_create(sports)


def generate_sport_levels(apps, schema_editor):
    SportLevel = apps.get_model("participants", "SportLevel")
    sport_levels = (SportLevel(level=choice[0]) for choice in SportLevel.level.field.choices)
    SportLevel.objects.bulk_create(sport_levels)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        limit_choices_to=models.Q(("is_active", True)),
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="player",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "player",
                "verbose_name_plural": "players",
                "db_table": "player",
            },
        ),
        migrations.CreateModel(
            name="Sport",
            fields=[
                (
                    "name",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Football"),
                            (2, "Basketball"),
                            (3, "Volleyball"),
                            (4, "Tennis"),
                            (5, "Table Tennis"),
                        ],
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
            ],
            options={
                "verbose_name": "sport",
                "verbose_name_plural": "sports",
                "db_table": "sport",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="SportLevel",
            fields=[
                (
                    "level",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Beginner"),
                            (2, "Lower Intermediate"),
                            (3, "Intermediate"),
                            (4, "Upper Intermediate"),
                            (5, "Expert"),
                        ],
                        primary_key=True,
                        serialize=False,
                        verbose_name="level",
                    ),
                ),
            ],
            options={
                "verbose_name": "sport level",
                "verbose_name_plural": "sport levels",
                "db_table": "sport_level",
                "ordering": ("level",),
            },
        ),
        migrations.CreateModel(
            name="PlayerSport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="player_sports",
                        to="participants.sportlevel",
                        verbose_name="level",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sports",
                        to="participants.player",
                        verbose_name="player",
                    ),
                ),
                (
                    "sport",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="player_sports",
                        to="participants.sport",
                        verbose_name="sport",
                    ),
                ),
            ],
            options={
                "verbose_name": "player sport",
                "verbose_name_plural": "player sports",
                "db_table": "player_sport",
            },
        ),
        migrations.AddConstraint(
            model_name="playersport",
            constraint=models.UniqueConstraint(fields=("player", "sport"), name="player_sport_unique"),
        ),
        migrations.RunPython(
            generate_sports,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            generate_sport_levels,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
