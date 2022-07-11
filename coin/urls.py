from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("whale", views.whale, name="whale"),
    path("acoin/<str:id>", views.acoin, name="acoin"),
    path("gecko", views.gecko, name="gecko"),
    path("gcoin/<str:id>", views.gcoin, name="gcoin"),
]
