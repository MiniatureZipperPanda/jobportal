from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    options = (
        ("employer", "employer"),
        ("candidate", "candidate")
    )
    role = models.CharField(max_length=120, choices=options, default="candidate")
    phone = models.CharField(max_length=12, null=True)


class Jobs(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company")
    location = models.CharField(max_length=100)
    salary = models.PositiveIntegerField(null=True)
    experience = models.PositiveIntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)
    last_date = models.DateField(null=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.job_title


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer")
    logo = models.ImageField(upload_to="companyprofile", null=True)
    location = models.CharField(max_length=100)
    services = models.CharField(max_length=150)
    description = models.CharField(max_length=250)


'''class SigninView(FormView):
    form_class = LoginForm
    template_name = "cand-login.html"


    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)

                return redirect("all-jobs")
            else:
                return  render(request,"cand-login.html",{"form":form})



def signout_view(request,args,*kwargs):
    logout(request)
    return redirect("signin") '''
