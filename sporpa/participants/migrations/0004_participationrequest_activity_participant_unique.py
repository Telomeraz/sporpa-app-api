# Generated by Django 4.1.5 on 2023-01-24 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0003_participationrequest"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="participationrequest",
            constraint=models.UniqueConstraint(
                fields=("activity", "participant"),
                name="activity_participant_unique",
                violation_error_message="You already sent a participation request.",
            ),
        ),
    ]