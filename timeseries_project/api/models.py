from django.db import models
from django_mysql.models import ListTextField


class UseCase(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()

    # At least one of the following two fields must be filled
    # If the two are filled, then the end_date is used
    end_date = models.DateTimeField()
    data_size = models.IntegerField()

    producer_types = [
        ("Additive", "additive"),
        ("Multiplicative", "multiplicative"),
    ]
    producer_type = models.CharField(choices=producer_types)


class Configuration(models.Model):
    # This is the frequency of the time index used in pandas
    cycle_component_freq = models.CharField(max_length=5)
    cycle_component_amplitude = models.FloatField()

    trend_coefficients = ListTextField(
        base_field=models.FloatField(), size=10, default=[0]
    )
    noise_level = models.FloatField()
    outlier_percentage = models.FloatField(default=0)
    missing_percentage = models.FloatField(default=0)

    status_choices = [
        ("Submitted", "Submitted"),
        ("Running", "Running"),
        ("Succeeded", "Succeeded"),
        ("Failed", "Failed"),
    ]
    status = models.CharField(max_length=100, choices=status_choices)

    # Creating a one-to-many relationship between UseCase and Configuration
    # as a use case can have many configurations
    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE)
