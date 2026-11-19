from django.urls import path

from . import views

app_name = "echangecompetence"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("plan-activity/", views.PlanActivityView.as_view(), name="plan-activity"),
    path("my-activities/", views.MyActivitiesView.as_view(), name="my-activities"),
    path(
        "<int:pk>/detail-activity/",
        views.DetailActivityView.as_view(),
        name="detail-activity",
    ),
    path("manage-skill/", views.ManageSkillView.as_view(), name="manage-skill"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("reserved/", views.ReservedView.as_view(), name="reserved"),
    path("ask-help/", views.HelpView.as_view(), name="ask-help"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
