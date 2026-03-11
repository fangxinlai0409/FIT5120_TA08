from django.contrib import admin

from .models import CancerStatistic, Location, ProtectionRule, UVReading


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "latitude", "longitude")


@admin.register(UVReading)
class UVReadingAdmin(admin.ModelAdmin):
    list_display = ("location", "uv_index", "risk_level", "observation_time")
    list_filter = ("risk_level", "location")


@admin.register(CancerStatistic)
class CancerStatisticAdmin(admin.ModelAdmin):
    list_display = ("year", "incidence_rate", "age_group")


@admin.register(ProtectionRule)
class ProtectionRuleAdmin(admin.ModelAdmin):
    list_display = ("label", "min_uv", "max_uv")
