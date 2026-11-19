from django import forms

from .models import Activity


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class InscriptionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Prénom")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class PlannedActivityForm(forms.Form):
    activity = forms.ModelChoiceField(queryset=Activity.objects.all(), label="Activité")
    date = forms.DateField(label="Date", widget=forms.SelectDateWidget)
    description = forms.CharField(label="Description", widget=forms.Textarea)
