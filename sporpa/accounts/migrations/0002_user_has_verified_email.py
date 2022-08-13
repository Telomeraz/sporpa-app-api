# Generated by Django 4.1 on 2022-08-13 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_verified_email',
            field=models.BooleanField(default=False, help_text='Designates whether this user has verified email address.', verbose_name='verified email'),
        ),
    ]
