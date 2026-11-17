from django.contrib.auth import authenticate, login, logout
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic

from echangecompetence.forms import LoginForm
from echangecompetence.models import belongSkill, plannedActivity, skill


class IndexView(generic.ListView):
    template_name = "echangecompetence/index.html"
    context_object_name = "index_tuple"

    def get_queryset(self):
        """Return the last five published questions."""
        return (
            plannedActivity.objects.order_by("-date")[:5],
            skill.objects.all(),
        )


class LoginView(generic.FormView):
    template_name = "echangecompetence/login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        # Here you can add your authentication logic
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        # Add your authentication logic here
        # For example, you might check the username and password against a database
        user = authenticate(username=username, password=password)

        if user is not None:
            # Authentication successful
            login(self.request, user)
            return super().form_valid(form)
        else:
            # Authentication failed
            form.add_error(None, "Identifiants incorrects.")
            return self.form_invalid(form)


class LogoutView(generic.View):
    def post(self, request):
        logout(request)
        return redirect(request.POST.get("next", "/"))


class DetailActivityView(generic.DetailView):
    model = plannedActivity
    template_name = "echangecompetence/detailActivity.html"


class ManageSkillView(generic.ListView):
    template_name = "echangecompetence/manage-skill.html"
    context_object_name = "skills"

    def get_queryset(self):
        return skill.objects.annotate(
            user_has_skill=Exists(
                belongSkill.objects.filter(user=self.request.user, skill=OuterRef("pk"))
            )
        )


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
