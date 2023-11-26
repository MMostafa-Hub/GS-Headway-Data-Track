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

    # Query to get a simulator by name
    simulator_by_name = graphene.Field(
        SimulatorType, name=graphene.String(required=True)
    )

    def resolve_all_simulators(self, info):
        return Simulator.objects.all()

    def resolve_simulator_by_name(self, info, name):
        try:
            return Simulator.objects.get(name=name)
        except Simulator.DoesNotExist:
            return None
    

schema = graphene.Schema(query=Query)
