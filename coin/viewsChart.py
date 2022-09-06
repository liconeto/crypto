from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self, spark):
        """Return 3 datasets to plot."""

        return [spark]


line_chart = TemplateView.as_view(template_name="geraChart.html")
line_chart_json = LineChartJSONView.as_view()
