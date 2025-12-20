from django.contrib import admin
from .models import  Speciality, KnowledgeField


@admin.register(KnowledgeField)
class KnowledgeFieldAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'order')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'knowledge_field', 'parent', 'level')
    list_filter = ('knowledge_field', 'level')
    search_fields = ('code', 'name')
    autocomplete_fields = ('knowledge_field', 'parent')
    ordering = ('code',)