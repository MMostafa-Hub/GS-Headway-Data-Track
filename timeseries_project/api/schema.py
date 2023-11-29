from .models import SeasonalityComponent, Dataset, Simulator
from .serializers import SimulatorSerializer
import graphene
from graphene_django.types import DjangoObjectType


class SeasonalityComponentType(DjangoObjectType):
    class Meta:
        model = SeasonalityComponent
        fields = [
            "frequency",
            "multiplier",
            "phase_shift",
            "amplitude",
        ]


class DatasetType(DjangoObjectType):
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


class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator
        fields = [
            "name",
            "start_date",
            "end_date",
            "data_size",
            "type",
            "datasets",
            "sink_name",
            "interval",
        ]


class SimulatorInput(graphene.InputObjectType):
    name = graphene.String()
    start_date = graphene.String()
    end_date = graphene.String()
    type = graphene.String()
    sink_name = graphene.String()
    datasets = graphene.List(lambda: DatasetInput)


class DatasetInput(graphene.InputObjectType):
    generator_name = graphene.String()
    attribute_name = graphene.String()
    frequency = graphene.String()
    trend_coefficients = graphene.List(graphene.Int)
    missing_percentage = graphene.Float()
    outlier_percentage = graphene.Float()
    noise_level = graphene.Float()
    cycle_amplitude = graphene.Float()
    cycle_frequency = graphene.Int()
    seasonality_components = graphene.List(lambda: SeasonalityComponentInput)


class SeasonalityComponentInput(graphene.InputObjectType):
    frequency = graphene.String()
    multiplier = graphene.Int()
    phase_shift = graphene.Int()
    amplitude = graphene.Float()


class CreateSimulator(graphene.Mutation):
    class Arguments:
        input = SimulatorInput(required=True)

    simulator = graphene.Field(lambda: SimulatorType)

    @classmethod
    def mutate(cls, root, info, input):
        simulator_serializer = SimulatorSerializer(data=input)
        simulator_serializer.is_valid(raise_exception=True)
        simulator = simulator_serializer.save()
        return CreateSimulator(simulator=simulator)


class Mutation(graphene.ObjectType):
    create_simulator = CreateSimulator.Field()


class Query(graphene.ObjectType):
    # Query to list all simulators
    list_all_simulators = graphene.List(SimulatorType)

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
        limit=graphene.Int(),
    )

    def resolve_list_all_simulators(self, info):
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
        limit=None,
    ):
        """
        Query to get the simulators by name, sink name, start data, end date, data size, type
        """
        simulators = Simulator.objects.all().first(limit)

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


schema = graphene.Schema(query=Query, mutation=Mutation)
