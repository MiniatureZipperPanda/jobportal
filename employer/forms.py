from django import forms
from employer.models import Jobs, CompanyProfile
# from django.contrib.auth.models import User
from employer.models import User

from django.contrib.auth.forms import UserCreationForm


class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        exclude = ("company", "created_date", "active_status")
        widgets = {
            "last_date": forms.DateInput(attrs={"class": "form-control", "type": "date"})
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2", "role", "phone"]


class LoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ("user",)
