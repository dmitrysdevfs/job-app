from django.contrib import admin
from django.utils import timezone
from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'employer', 
        'source',
        'external_id',
        'status',
        'generation_label',
        'salary_min', 
        'is_active', 
        'relevance_status',
        'published_at'
    )
    list_display_links = ('title',)
    list_filter = (
        'status',
        'is_active', 
        'source',
        'report_3pn_date',
        'employment_type', 
        'education_level', 
        'published_at',
        'confirmed_at',
        'closed_at'
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
        'kved',
        'parent'
    )
    
    actions = ['confirm_relevance']

    @admin.action(description="Підтвердити актуальність обраних вакансій")
    def confirm_relevance(self, request, queryset):
        queryset.update(confirmed_at=timezone.now())
        self.message_user(request, "Актуальність обраних вакансій підтверджена.")

    def generation_label(self, obj):
        if obj.generation > 1:
            return f"{obj.generation}-ге"
        return "-"
    generation_label.short_description = "Покоління"

    def relevance_status(self, obj):
        # Логіка для візуальної підказки (можна розширити HTML кольорами)
        last_check = obj.confirmed_at or obj.published_at
        days_diff = (timezone.now() - last_check).days
        if days_diff > 15:
            return "⏳ Потребує перевірки"
        return "✅ Актуальна"
    relevance_status.short_description = "Статус"
