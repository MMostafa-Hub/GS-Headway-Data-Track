class ProducerCreator:
    """This class is responsible for writing the time series to any format."""

    def __init__(self, output_type: str):
        self.output_type = output_type

    def create(self, **kwargs):
        """This method is responsible for writing the time series to any format."""
        if self.output_type == "csv":
            from .producers.csv_producer import CsvProducer

            return CsvProducer(**kwargs)
        elif self.output_type == "django":
            from .producers.djangol_producer import DjangoModelProducer

            return DjangoModelProducer(**kwargs)
        else:
            raise Exception("Invalid output type.")
