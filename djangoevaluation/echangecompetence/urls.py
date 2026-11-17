from django.urls import path

from . import views

app_name = "echangecompetence"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("plan-activity/", views.PlanActivityView.as_view(), name="plan-activity"),
    path(
        "<int:pk>/detailActivity/",
        views.DetailActivityView.as_view(),
        name="detailActivity",
    ),
    path("manage-skill/", views.ManageSkillView.as_view(), name="manage-skill"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
