from django.urls import path
from . import views, viewsChart

urlpatterns = [
    path("", views.index, name="index"),
    path("whale", views.whale, name="whale"),
    path("gecko", views.gecko, name="gecko"),
    path("gcoin/<str:id>", views.gcoin, name="gcoin"),
    path("geraChart/<str:sparkline>", views.geraChart, name="geraChart"),
    path("chart", viewsChart.line_chart, name="line_chart"),
    path("chartJSON", viewsChart.line_chart_json, name="line_chart_json"),
]
