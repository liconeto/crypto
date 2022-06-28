from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("whale", views.whale, name="whale"),
    path("lore", views.lore, name="lore"),
]
