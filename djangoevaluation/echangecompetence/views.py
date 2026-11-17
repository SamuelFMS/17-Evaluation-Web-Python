from django.http import HttpResponse
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
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


class DetailActivityView(generic.DetailView):
    model = plannedActivity
    template_name = "echangecompetence/detailActivity.html"


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
