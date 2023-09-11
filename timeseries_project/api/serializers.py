from rest_framework import serializers
from .models import UseCase, Dataset, SeasonalityComponent


class SeasonalityComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalityComponent
        fields = ["frequency", "multiplier", "phase_shift", "amplitude"]


class DatasetSerializer(serializers.ModelSerializer):
    seasonality_components = SeasonalityComponentSerializer(
        many=True
    )  # Dataset has many seasonality components

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
            "seasonality_components",
        ]

    def create(self, validated_data):
        """Creates a dataset and its seasonality components."""
        seasonality_components_data = validated_data.pop(
            "seasonality_components"
        )  # Remove the seasonality components data from the validated data

        dataset = Dataset.objects.create(**validated_data)  # Create the dataset
        # Create the seasonality components
        for seasonality_component_data in seasonality_components_data:
            SeasonalityComponent.objects.create(
                dataset=dataset, **seasonality_component_data
            )
        return dataset


class UseCaseSerializer(serializers.ModelSerializer):
    datasets = DatasetSerializer(many=True)  # UseCase has many datasets

    class Meta:
        model = UseCase
        fields = ["name", "start_date", "end_date", "type", "datasets"]

    def validate(self, attrs):
        """Checks that either the end date or the data size is provided, but not both."""
        if not (bool(attrs["end_date"]) ^ bool(attrs["data_size"])):
            raise serializers.ValidationError(
                "Either the end date or the data size must be provided, but not both."
            )
        return attrs

    def create(self, validated_data):
        """Creates a user context and its datasets."""
        datasets_data = validated_data.pop(
            "datasets"
        )  # Remove the datasets data from the validated data

        use_case = UseCase.objects.create(**validated_data)  # Create the use case

        # Create the datasets
        for dataset_data in datasets_data:
            Dataset.objects.create(use_case=use_case, **dataset_data)
        return use_case
