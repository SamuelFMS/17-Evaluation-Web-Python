from django import forms

from .models import activity


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class PlannedActivityForm(forms.Form):
    activity = forms.ModelChoiceField(queryset=activity.objects.all(), label="Activité")
    date = forms.DateField(label="Date", widget=forms.SelectDateWidget)
    description = forms.CharField(label="Description", widget=forms.Textarea)
