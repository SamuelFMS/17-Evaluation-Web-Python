from django.http import HttpResponse
from django.views import generic

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


class DetailActivityView(generic.DetailView):
    model = plannedActivity
    template_name = "echangecompetence/detailActivity.html"


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
