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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     l_date=cleaned_data.get("last_date")
    #     exp=cleaned_data.get("experience")


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "username",
                  "email",
                  "role",
                  "phone",
                  "password1",
                  'password2',
                  ]
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control form-control-lg', }),
            "last_name": forms.TextInput(attrs={'class': 'form-control form-control-lg', }),
            "username": forms.TextInput(attrs={'class': 'form-control form-control-lg', }),
            "email": forms.EmailInput(attrs={'class': 'form-control form-control-lg', }),
            "phone": forms.TextInput(attrs={'class': 'form-control form-control-lg', }),

        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control form-control-lg py-1 rounded', 'id': 'password', 'name': 'password',
             'minlength': '6'})

        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control form-control-lg py-1 rounded', 'id': 'confirm_password',
             'name': 'confirm_password'})

        self.fields['role'].widget.attrs.update(
            {'class': 'form-control form-control-lg py-1 rounded', 'id': 'role_id', 'name': 'role_name'})


class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                              'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg',
                                                                 'placeholder': 'Password'}))


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ("user",)
