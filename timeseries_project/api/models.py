from django.db import models


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
