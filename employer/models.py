from django.db import models


class Jobs(models.Model):
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.PositiveIntegerField(null=True)
    experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.job_title

'''class SigninView(FormView):
    form_class = LoginForm
    template_name = "login.html"


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
                return  render(request,"login.html",{"form":form})



def signout_view(request,args,*kwargs):
    logout(request)
    return redirect("signin") '''