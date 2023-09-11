from rest_framework import serializers
from .models import UseCase, Dataset, SeasonalityComponent


class SeasonalComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalityComponent
        fields = [
            "frequency",
            "multiplier",
            "phase_shift",
            "amplitude",
        ]


class ConfigurationSerializer(serializers.ModelSerializer):
    seasonal_components = SeasonalComponentSerializer(many=True)

    class Meta:
        model = Dataset
        fields = [
            "frequency",
            "trend_coefficients",
            "missing_percentage",
            "outlier_percentage",
            "noise_level",
            "cycle_amplitude",
            "cycle_frequency",
            "seasonal_components",
        ]


class UseCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseCase
        fields = [
            "name",
            "start_date",
            "end_date",
            "data_size",
            "type",
            "datasets",
        ]
