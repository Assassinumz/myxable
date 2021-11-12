from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("convert/<str:convert_type>", views.convert, name="convert")
]