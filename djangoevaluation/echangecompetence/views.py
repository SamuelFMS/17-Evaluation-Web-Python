from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import redirect
from django.utils import timezone
from django.views import generic

from echangecompetence.forms import LoginForm, PlannedActivityForm
from echangecompetence.models import (
    BelongSkill,
    HelpRequest,
    PlannedActivity,
    Skill,
)


class IndexView(generic.ListView):
    template_name = "echangecompetence/index.html"
    context_object_name = "index_tuple"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            has_skill = BelongSkill.objects.filter(
                user=self.request.user, skill=OuterRef("activity__skill__pk")
            )
            return (
                PlannedActivity.objects.filter(
                    Exists(has_skill),
                    date__gte=timezone.now().date(),
                ).order_by("-date"),
                Skill.objects.all(),
            )

        return (
            PlannedActivity.objects.filter(date__gte=timezone.now().date()).order_by(
                "-date"
            ),
            Skill.objects.all(),
        )


class PlanActivityView(generic.FormView):
    template_name = "echangecompetence/plan_activity.html"
    form_class = PlannedActivityForm
    success_url = "/"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            planned_activity = PlannedActivity(
                user=self.request.user,
                activity=form.cleaned_data["activity"],
                description=form.cleaned_data["description"],
                date=form.cleaned_data["date"],
            )
            planned_activity.save()
            return super().form_valid(form)
        else:
            form.add_error(None, "Vous devez être connecté pour proposer une activité.")
            return self.form_invalid(form)


class MyActivitiesView(generic.ListView):
    template_name = "echangecompetence/my_activities.html"
    context_object_name = "my_activities"

    def get_queryset(self):
        return (
            PlannedActivity.objects.filter(user=self.request.user),
            PlannedActivity.objects.filter(reserved_by=self.request.user),
        )


class LoginView(generic.FormView):
    template_name = "echangecompetence/login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
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
        return redirect("/")


class ReservedView(generic.View):
    def post(self, request):
        planned_activity_id = request.POST.get("planned_activity_id")
        planned_activity = PlannedActivity.objects.get(pk=planned_activity_id)
        if (
            planned_activity
            and planned_activity.reserved_by is None
            and planned_activity.user != request.user
            and request.user.is_authenticated()
        ):
            planned_activity.reserved_by = request.user
            planned_activity.save()
        return redirect(request.POST.get("next", "/"))


class HelpView(generic.View):
    success_url = "/"

    def post(self, request):
        print("test")
        planned_activity_id = request.POST.get("planned_activity_id")
        planned_activity = PlannedActivity.objects.filter(
            pk=planned_activity_id
        ).first()
        if not planned_activity:
            return redirect(
                f"{request.POST.get('next', '/')}?error_message=aucun-planned-activity"
            )
        if planned_activity.user == request.user:
            selector_email = request.POST.get("select-helplist", "")
            input_email = request.POST.get("email", "")
            final_email = selector_email or input_email
            if not final_email:
                return redirect(
                    f"{request.POST.get('next', '/')}?error_message=final-email-none"
                )
            find_user = User.objects.filter(email=final_email).first()
            if not find_user:
                return redirect(
                    f"{request.POST.get('next', '/')}?error_message=not-final-email"
                )
            if find_user == request.user:
                return redirect(
                    f"{request.POST.get('next', '/')}?error_message=self-email"
                )
            if HelpRequest.objects.filter(
                user=find_user, planned_activity=planned_activity
            ).first():
                return redirect(
                    f"{request.POST.get('next', '/')}?error_message=already-ask"
                )
            HelpRequest.objects.create(
                user=find_user,
                planned_activity=planned_activity,
                date=timezone.now().date(),
            )
        return redirect(f"{request.POST.get('next', '/')}")


class DetailActivityView(generic.DetailView):
    model = PlannedActivity
    template_name = "echangecompetence/detail_activity.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (
            self.request.user.is_authenticated
            and self.request.user == context["plannedactivity"].user
        ):
            list_user_got_help = (
                PlannedActivity.objects.filter(user=self.request.user)
                .values("reserved_by")
                .distinct()
            )
            list_user_helped = (
                PlannedActivity.objects.filter(reserved_by=self.request.user)
                .values("user")
                .distinct()
            )
            context["user_helplist"] = User.objects.filter(
                Q(pk__in=list_user_got_help) | Q(pk__in=list_user_helped)
            ).distinct()
        return context


class ManageSkillView(generic.ListView):
    template_name = "echangecompetence/manage_skill.html"
    context_object_name = "skills"

    def post(self, request):
        selected_skills = request.POST.getlist("skills")
        print(selected_skills)
        BelongSkill.objects.filter(user=request.user).delete()
        for skill_id in selected_skills:
            skill_instance = Skill.objects.get(id=skill_id)
            BelongSkill.objects.create(user=request.user, skill=skill_instance)
        return redirect(request.path)

    def get_queryset(self):
        return Skill.objects.annotate(
            user_has_skill=Exists(
                BelongSkill.objects.filter(user=self.request.user, skill=OuterRef("pk"))
            )
        )
