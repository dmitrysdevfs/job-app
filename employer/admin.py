from django.contrib import admin
from .models import Employer


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'employer_type', 'tax_id', 'is_verified', 'created_at')
    list_filter = ('employer_type', 'is_verified', 'created_at')
    search_fields = ('name', 'brand_name', 'tax_id')
    autocomplete_fields = ('owner', 'kved', 'location', 'staff')
    
    def get_name(self, obj):
        if obj.brand_name:
            return f"{obj.brand_name} ({obj.name})"
        return obj.name
    get_name.short_description = "Назва"
