from django.contrib import admin

from .models import ActivityMessage, DirectMessage


@admin.register(ActivityMessage)
class ActivityMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    pass
