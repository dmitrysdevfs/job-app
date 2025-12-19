from django.contrib import admin
from .models import Section, Division, Group, Class

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "section")
    search_fields = ("code", "name")
    list_filter = ("section",)
    autocomplete_fields = ("section",)
    ordering = ("code",)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "division")
    search_fields = ("code", "name")
    list_filter = ("division__section", "division")
    autocomplete_fields = ("division",)
    ordering = ("code",)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "group")
    search_fields = ("code", "name")
    list_filter = ("group__division__section", "group__division", "group")
    autocomplete_fields = ("group",)
    ordering = ("code",)
