from django.contrib import admin
from .models import Bird, Flora, Story, NatureTrailSchedule, NatureTrailMedia


@admin.register(NatureTrailSchedule)
class NatureTrailScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'date', 'start_time', 'end_time')
    list_filter = ('day', 'date')


@admin.register(NatureTrailMedia)
class NatureTrailMediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'is_active', 'order')
    list_editable = ('is_active', 'order')



admin.site.register(Bird)
admin.site.register(Flora)
admin.site.register(Story)
