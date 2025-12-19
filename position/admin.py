from django.contrib import admin
from .models import Section, Subsection, Class, Subclass, Group, Position, JobTitle


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'section')
    search_fields = ('code', 'name')
    autocomplete_fields = ('section',)
    ordering = ('code',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'subsection', 'section')
    search_fields = ('code', 'name')
    autocomplete_fields = ('subsection', 'section')
    list_filter = ('section',)
    ordering = ('code',)


@admin.register(Subclass)
class SubclassAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'class_obj')
    search_fields = ('code', 'name')
    autocomplete_fields = ('class_obj',)
    ordering = ('code',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'class_obj')
    search_fields = ('code', 'name')
    autocomplete_fields = ('class_obj',)
    ordering = ('code',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'group')
    search_fields = ('code', 'name')
    autocomplete_fields = ('group',)
    list_filter = ('group',)
    ordering = ('code',)


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'position', 'group')
    search_fields = ('code', 'name')
    autocomplete_fields = ('position', 'group', 'subclass')
    list_filter = ('position', 'group')
    ordering = ('code',)
