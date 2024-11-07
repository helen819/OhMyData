from django.urls import path
from . import views

app_name = "p4ds"

urlpatterns = [
    path("", views.index, name="index"),
]