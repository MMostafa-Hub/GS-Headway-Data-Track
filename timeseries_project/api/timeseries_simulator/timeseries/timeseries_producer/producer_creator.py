class ProducerCreator:
    """This class is responsible for writing the time series to any format."""

    def __init__(self, output_type: str):
        """
        Initialize a ProducerCreator instance.

        Args:
            output_type (str): The desired output format for writing time series data.
                Valid options include "csv" and "django".
        """
        self.output_type = output_type

    def create(self, **kwargs):
        """
        Create a time series producer based on the specified output format.

        Args:
            **kwargs: Additional keyword arguments to pass to the producer constructor.

        Returns:
            Producer: An instance of a time series producer for the specified output format.

        Raises:
            Exception: If an invalid output type is specified.
        """
        if self.output_type == "csv":
            from .producers.csv_producer import CsvProducer

            return CsvProducer(**kwargs)
        elif self.output_type == "django":
            from .producers.djangol_producer import DjangoModelProducer

            return DjangoModelProducer(**kwargs)
        else:
            raise Exception("Invalid output type.")
