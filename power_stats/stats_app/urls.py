from django.urls import path

from power_stats.stats_app import views as stats_views

app_name = "stats_app"
urlpatterns = [
    path("genarate_data/", stats_views.genarate_data, name="genarate_data"),
    path("get_kafka_data/", stats_views.store_data, name="save_data"),
    path("plot_graph/", stats_views.plot_graph, name="plot_graph"),
]
