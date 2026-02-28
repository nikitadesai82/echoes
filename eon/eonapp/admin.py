from django.contrib import admin
from django import forms
from datetime import time
from .models import Bird, Flora, Story, NatureTrailSchedule, NatureTrailMedia


# =========================
# 12 HOUR TIME DROPDOWNS
# =========================
HOUR_CHOICES = [(i, f"{i:02d}") for i in range(1, 13)]
MINUTE_CHOICES = [(i, f"{i:02d}") for i in range(0, 60)]
AMPM_CHOICES = [('AM', 'AM'), ('PM', 'PM')]


# =========================
# CUSTOM FORM
# =========================
class NatureTrailScheduleForm(forms.ModelForm):

    start_hour = forms.ChoiceField(choices=HOUR_CHOICES, label="Start")
    start_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label="")
    start_ampm = forms.ChoiceField(choices=AMPM_CHOICES, label="")

    end_hour = forms.ChoiceField(choices=HOUR_CHOICES, label="End")
    end_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label="")
    end_ampm = forms.ChoiceField(choices=AMPM_CHOICES, label="")

    class Meta:
        model = NatureTrailSchedule
        exclude = ['start_time', 'end_time']

    def clean(self):
        cleaned = super().clean()

        def convert(h, m, ap):
            if not h or not m or not ap:
                return None

            h = int(h)
            m = int(m)

            if ap == 'PM' and h != 12:
                h += 12
            if ap == 'AM' and h == 12:
                h = 0

            return time(hour=h, minute=m)

        cleaned['start_time'] = convert(
            cleaned.get('start_hour'),
            cleaned.get('start_minute'),
            cleaned.get('start_ampm')
        )

        cleaned['end_time'] = convert(
            cleaned.get('end_hour'),
            cleaned.get('end_minute'),
            cleaned.get('end_ampm')
        )

        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.start_time = self.cleaned_data['start_time']
        obj.end_time = self.cleaned_data['end_time']
        if commit:
            obj.save()
        return obj

# =========================
# ADMIN CONFIG
# =========================
@admin.register(NatureTrailSchedule)
class NatureTrailScheduleAdmin(admin.ModelAdmin):
    form = NatureTrailScheduleForm
    readonly_fields = ('day',)

    list_display = ('day', 'date', 'start_time', 'end_time')
    list_filter = ('day', 'date')

    fieldsets = (
        (None, {
            'fields': ('day', 'date')
        }),
        ('Time Slot', {
            'fields': (
                ('start_hour', 'start_minute', 'start_ampm'),
                ('end_hour', 'end_minute', 'end_ampm'),
            )
        }),
    )

    class Media:
        js = ('admin/js/autoday.js',)


@admin.register(NatureTrailMedia)
class NatureTrailMediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'is_active', 'order')
    list_editable = ('is_active', 'order')


# =========================
# REGISTER OTHERS
# =========================
admin.site.register(Bird)
admin.site.register(Flora)
admin.site.register(Story)