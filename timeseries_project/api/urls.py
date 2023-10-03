from django.urls import path
from .views import (
    AddView,
    ListView,
    RestartView,
    StopView,
    StatusView,
    StartView,
)

urlpatterns = [
    path("add", AddView.as_view()),
    path("start", StartView.as_view()),
    path("list", ListView.as_view()),
    path("restart", RestartView.as_view()),
    path("stop", StopView.as_view()),
    path("status", StatusView.as_view()),
]
