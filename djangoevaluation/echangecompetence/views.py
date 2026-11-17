from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic

from echangecompetence.forms import LoginForm
from echangecompetence.models import plannedActivity, skill


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


class DetailActivityView(generic.DetailView):
    model = plannedActivity
    template_name = "echangecompetence/detailActivity.html"


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
