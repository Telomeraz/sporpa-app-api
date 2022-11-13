from django.contrib import admin

from events.models import Activity, ActivityLevel, ActivityPlayer


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityLevel)
class ActivityLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityPlayer)
class ActivityPlayerAdmin(admin.ModelAdmin):
    pass
