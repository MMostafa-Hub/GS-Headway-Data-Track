from django.db import models
from django.utils import timezone


class Simulator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateTimeField(name="start_date")

    # At least one of the following two fields must be filled
    # If the two are filled, then the end_date is used
    end_date = models.DateTimeField(name="end_date", null=True, blank=True)
    data_size = models.IntegerField(name="data_size", null=True, blank=True)

    producer_types = [
        ("additive", "additive"),
        ("multiplicative", "multiplicative"),
    ]
    type = models.CharField(max_length=15, choices=producer_types, name="type")

    status_choices = [
        ("Submitted", "Submitted"),
        ("Running", "Running"),
        ("Succeeded", "Succeeded"),
        ("Failed", "Failed"),
    ]
    status = models.CharField(
        max_length=100, choices=status_choices, default="Submitted"
    )

    sink_name = models.CharField(max_length=100, name="sink_name", default="sink_topic")

    interval = models.CharField(
        name="interval", null=True, blank=True, max_length=100, default=None
    )

    start_date = models.DateTimeField(
        name="start_date", null=True, blank=True, default=timezone.now
    )


class Dataset(models.Model):
    # This is the frequency of the time index used in pandas
    frequency = models.CharField(max_length=5, name="frequency")

    noise_level = models.FloatField(name="noise_level")
    trend_coefficients = models.JSONField(name="trend_coefficients", default=list)
    missing_percentage = models.FloatField(default=0, name="missing_percentage")
    outlier_percentage = models.FloatField(default=0, name="outlier_percentage")

    cycle_component_freq = models.IntegerField(name="cycle_frequency")
    cycle_component_amplitude = models.FloatField(name="cycle_amplitude")

    # Creating a one-to-many relationship between UseCase and Configuration
    # as a use case can have many configurations
    simulator = models.ForeignKey(
        Simulator,
        related_name="datasets",
        on_delete=models.CASCADE,
    )

    # The generator name is for example the name of the sensor that generates the data
    generator_name = models.CharField(max_length=100, name="generator_name")

    # The attribute name is for example the physical quantity that the sensor measures
    attribute_name = models.CharField(max_length=100, name="attribute_name")

    sink_data = models.JSONField(name="sink_data", default=list)


class SeasonalityComponent(models.Model):
    amplitude = models.FloatField(default=0, name="amplitude")
    phase_shift = models.FloatField(default=0, name="phase_shift")
    frequency_types = [
        ("Daily", "daily"),
        ("Weekly", "weekly"),
        ("Monthly", "monthly"),
    ]
    frequency_type = models.CharField(
        max_length=10, choices=frequency_types, name="frequency"
    )
    frequency_multiplier = models.FloatField(default=0, name="multiplier")

    # Creating a one-to-many relationship between Dataset and SeasonalityComponent
    # as a dataset can have many seasonal components
    dataset = models.ForeignKey(
        Dataset,
        related_name="seasonality_components",
        on_delete=models.CASCADE,
    )
