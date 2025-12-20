from django.contrib import admin
from .models import Region, District, Community, Settlement, CityDistrict

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category')
    search_fields = ('name', 'code')
    list_filter = ('category',)
    ordering = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'code')
    search_fields = ('name', 'code')
    list_filter = ('region',)
    autocomplete_fields = ('region',)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'code')
    search_fields = ('name', 'code')
    autocomplete_fields = ('district',)

@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'community', 'code')
    search_fields = ('name', 'code', 'community__name', 'community__district__name', 'community__district__region__name')
    list_filter = ('category',)
    autocomplete_fields = ('community',)

@admin.register(CityDistrict)
class CityDistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'settlement', 'code')
    search_fields = ('name', 'code')
    autocomplete_fields = ('settlement',)
