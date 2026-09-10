from django.contrib import admin
from django import forms
from datetime import time
from .models import Bird, Flora, Butterfly, Story, NatureTrailSchedule, NatureTrailMedia

# CSV IMPORT
from import_export import resources
from import_export.admin import ImportExportModelAdmin


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
# NATURE TRAIL ADMIN
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


# =========================
# MEDIA ADMIN
# =========================
@admin.register(NatureTrailMedia)
class NatureTrailMediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'is_active', 'order')
    list_editable = ('is_active', 'order')


# =========================
# CSV IMPORT CONFIG
# =========================

class BirdResource(resources.ModelResource):
    class Meta:
        model = Bird
        import_id_fields = ['Bird_Name']


class FloraResource(resources.ModelResource):
    class Meta:
        model = Flora
        import_id_fields = ['Flora_Name']


class ButterflyResource(resources.ModelResource):
    class Meta:
        model = Butterfly
        import_id_fields = ['Butterfly_Name']

    # The source spreadsheet's file/image columns don't line up 1:1 with the
    # model, so fix them up before import-export maps columns to fields.
    def before_import_row(self, row, **kwargs):
        # Column is named "Butterfly_Maps" in the sheet; the model field is
        # "Butterfly_Map_Image". Without this, import-export can't match the
        # column to a field and silently drops it, leaving every butterfly's
        # map blank.
        if 'Butterfly_Maps' in row and not row.get('Butterfly_Map_Image'):
            row['Butterfly_Map_Image'] = row.pop('Butterfly_Maps')

        # The sheet uses Windows-style backslash paths (e.g.
        # "Images\Butterflies\Baronet01.webp"). Django storage/URLs need
        # forward slashes, or the resulting file URL breaks.
        path_fields = [
            'Butterfly_Animation',
            'Butterfly_Image1',
            'Butterfly_Image2',
            'Butterfly_Button_Media',
            'Butterfly_Map_Image',
        ]
        for field in path_fields:
            value = row.get(field)
            if value:
                row[field] = value.replace('\\', '/')


# =========================
# BIRD ADMIN (CSV ENABLED)
# =========================
@admin.register(Bird)
class BirdAdmin(ImportExportModelAdmin):
    resource_class = BirdResource


# =========================
# FLORA ADMIN (CSV ENABLED)
# =========================
@admin.register(Flora)
class FloraAdmin(ImportExportModelAdmin):
    resource_class = FloraResource


# =========================
# BUTTERFLY ADMIN (CSV ENABLED)
# =========================
@admin.register(Butterfly)
class ButterflyAdmin(ImportExportModelAdmin):
    resource_class = ButterflyResource


# =========================
# STORY
# =========================
admin.site.register(Story)