from rest_framework import serializers

from .models import CancerStatistic, Location, ProtectionRule, UVReading


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "city", "state", "latitude", "longitude"]


class UVReadingSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = UVReading
        fields = [
            "id",
            "uv_index",
            "risk_level",
            "observation_time",
            "burn_time_minutes",
            "location",
        ]


class CancerStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancerStatistic
        fields = ["id", "year", "incidence_rate", "age_group"]


class ProtectionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectionRule
        fields = ["id", "min_uv", "max_uv", "label", "recommendation"]
