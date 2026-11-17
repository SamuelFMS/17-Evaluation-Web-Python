from django.urls import path

from . import views

app_name = "echangecompetence"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "detailActivity/<int:pk>/",
        views.DetailActivityView.as_view(),
        name="detailActivity",
    ),
]
