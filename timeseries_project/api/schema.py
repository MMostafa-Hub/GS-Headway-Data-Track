import graphene
from graphene_django.types import DjangoObjectType

from .models import SeasonalityComponent, Dataset, Simulator


class SeasonalityComponentType(DjangoObjectType):
    class Meta:
        model = SeasonalityComponent
        fields = (
            "frequency",
            "multiplier",
            "phase_shift",
            "amplitude",
        )


class DatasetType(DjangoObjectType):
    class Meta:
        model = Dataset
        fields = (
            "frequency",
            "trend_coefficients",
            "missing_percentage",
            "outlier_percentage",
            "noise_level",
            "cycle_amplitude",
            "cycle_frequency",
            "generator_name",
            "attribute_name",
            "seasonality_components",
        )


class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator
        fields = (
            "name",
            "start_date",
            "end_date",
            "data_size",
            "type",
            "datasets",
            "sink_name",
            "interval",
            "datasets",
        )


class Query(graphene.ObjectType):
    # Query to get all simulators
    all_simulators = graphene.List(SimulatorType)

    # Query to get the simulators by name, sink name, start data, end date, data size, type
    get_simulators_by = graphene.List(
        SimulatorType,
        name=graphene.String(),
        sink_name=graphene.String(),
        type=graphene.String(),
        start_date=graphene.DateTime(),
        end_date=graphene.DateTime(),
        data_size=graphene.Int(),
        interval=graphene.String(),
    )

    def resolve_all_simulators(self, info):
        return Simulator.objects.all()

    def resolve_get_simulators_by(
        self,
        info,
        name=None,
        sink_name=None,
        type=None,
        start_date=None,
        end_date=None,
        data_size=None,
        interval=None,
    ):
        """
        Query to get the simulators by name, sink name, start data, end date, data size, type
        """
        simulators = Simulator.objects.all()

        if name:
            simulators = simulators.filter(name=name)

        if sink_name:
            simulators = simulators.filter(sink_name=sink_name)

        if type:
            simulators = simulators.filter(type=type)

        if start_date:
            simulators = simulators.filter(start_date=start_date)

        if end_date:
            simulators = simulators.filter(end_date=end_date)

        if data_size:
            simulators = simulators.filter(data_size=data_size)

        if interval:
            simulators = simulators.filter(interval=interval)

        return simulators


schema = graphene.Schema(query=Query)
