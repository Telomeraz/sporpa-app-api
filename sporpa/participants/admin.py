from django.contrib import admin

from participants.models import Player, PlayerSport, Sport, SportLevel


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(PlayerSport)
class PlayerSportAdmin(admin.ModelAdmin):
    pass


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    pass


@admin.register(SportLevel)
class SportLevelAdmin(admin.ModelAdmin):
    pass
