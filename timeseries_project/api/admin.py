from django.contrib import admin
from .models import Simulator, Dataset, SeasonalityComponent

# Register your models here.
admin.site.register(Simulator)
admin.site.register(Dataset)
admin.site.register(SeasonalityComponent)
