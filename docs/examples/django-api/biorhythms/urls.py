from django.urls import path
from . import views

urlpatterns = [
    path("", views.api_home, name="api_home"),
    path("api/", views.BiorhythmCalculationView.as_view(), name="api_info"),
    path(
        "api/calculate/",
        views.BiorhythmCalculationView.as_view(),
        name="calculate_biorhythm",
    ),
    path("api/quick/", views.QuickBiorhythmView.as_view(), name="quick_biorhythm"),
]
