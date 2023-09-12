from django.urls import path
from .views import views

urlpatterns = [
    path("seasonality", views.add_seasonality_component),
    path("dataset", views.add_dataset),
    path("use_case", views.add_use_case),
]
