from typing import override
from rest_framework import serializers
from .models import Simulator, Dataset, SeasonalityComponent


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
            "generator_name",
            "attribute_name",
        ]


class SimulatorSerializer(serializers.ModelSerializer):
    datasets = DatasetSerializer(many=True)  # UseCase has many datasets

    class Meta:
        model = Simulator
        fields = ["name", "start_date", "end_date", "data_size", "type", "datasets", "sink_name"]

    @override
    def validate(self, attrs):
        """Checks that either the end date or the data size is provided, but not both."""
        super().validate(attrs)
        if not (
            bool(attrs.get("end_date", False)) ^ bool(attrs.get("data_size", False))
        ):
            raise serializers.ValidationError(
                "Either the end date or the data size must be provided, but not both."
            )
        return attrs

    @override
    def create(self, validated_data):
        """Creates a user case and its associated datasets and seasonality components."""
        datasets_data = validated_data.pop(
            "datasets"
        )  # Remove the datasets data from the validated data

        simulator = Simulator.objects.create(**validated_data)  # Create the use case

        # Create the datasets and associate them with the simulator
        for dataset_data in datasets_data:
            seasonality_components_data = dataset_data.pop(
                "seasonality_components"
            )  # Remove the seasonality components data from the dataset

            # Create the dataset and associate it with the simulator
            dataset = Dataset.objects.create(**dataset_data, simulator=simulator)

            # Create the seasonality components and associate them with the dataset
            for seasonality_component_data in seasonality_components_data:
                SeasonalityComponent.objects.create(
                    **seasonality_component_data,
                    dataset=dataset  # Associate the seasonality component with the dataset
                )

        return simulator
