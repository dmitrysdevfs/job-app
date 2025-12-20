from django.contrib import admin
from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'employer', 
        'position', 
        'location', 
        'salary_min', 
        'salary_max', 
        'is_active', 
        'published_at'
    )
    list_filter = (
        'is_active', 
        'employment_type', 
        'education_level', 
        'published_at'
    )
    search_fields = (
        'title', 
        'description', 
        'employer__name', 
        'employer__brand_name'
    )
    autocomplete_fields = (
        'employer', 
        'position', 
        'speciality', 
        'location', 
        'kved'
    )
    
    # Можна додати inline або фільтри по тегах пізніше
    filter_horizontal = ('tags',)
