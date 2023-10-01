from django.urls import path
from .views import (
    add_use_case,
    list_simulators,
    restart_simulator,
    stop_simulator,
    check_status,
)

urlpatterns = [
    path("use_case", add_use_case),
    path("list_simulators", list_simulators),
    path("restart_simulator", restart_simulator),
    path("stop_simulator", stop_simulator),
    path("check_status", check_status),
]
