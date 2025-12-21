from django.contrib import admin
from django.utils.html import format_html
from .models import EmploymentType, EducationLevel, Degree, Tag, VacancySource


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('icon_preview', 'name', 'order')
    list_display_links = ('name',)
    search_fields = ('name',)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-height: 24px;"/>', obj.icon.url)
        return "-"
    icon_preview.short_description = "Іконка"


@admin.register(VacancySource)
class VacancySourceAdmin(admin.ModelAdmin):
    list_display = ('icon_preview', 'name', 'code', 'order')
    list_display_links = ('name',)
    search_fields = ('name', 'code')
    prepopulated_fields = {'code': ('name',)}

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-height: 24px;"/>', obj.icon.url)
        return "-"
    icon_preview.short_description = "Іконка"
