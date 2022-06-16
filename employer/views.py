from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from employer.forms import JobForm, CompanyProfileForm
from employer.models import Jobs, CompanyProfile
# from django.contrib.auth.models import User
from employer.models import User, Application
from django.contrib.auth import authenticate, login, logout
from employer.forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class EmployerHomeView(TemplateView):
    template_name = "emp-home.html"


class AddJobView(CreateView):
    model = Jobs
    form_class = JobForm
    template_name = "emp-add-job.html"
    success_url = reverse_lazy("emp-all-jobs")

    def form_valid(self, form):
        form.instance.company = self.request.user
        messages.success(self.request, "Your Job has been Added")
        return super().form_valid(form)

    # def get(self, request):
    #     form = JobForm
    #     return render(request, "emp-add-job.html", {"form": form})
    #
    # def post(self, request):
    #     form = JobForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #
    #         return render(request, "emp-home.html")
    #     else:
    #         return render(request, "emp-add-job.html", {"form": form})


class ListJobView(ListView):
    model = Jobs
    context_object_name = "jobs"
    template_name = "emp-list-job.html"

    def get_queryset(self):
        return Jobs.objects.filter(company=self.request.user)


# def get(self, request):
#     qs = Jobs.objects.filter(company=request.user)
#     return render(request, "emp-list-job.html", {"jobs": qs})


class JobDetailView(DetailView):
    model = Jobs
    context_object_name = "job"
    template_name = "emp-job-detail.html"
    pk_url_kwarg = "id"

    # def get(self, request, id):
    #     qs = Jobs.objects.get(id=id)
    #     return render(request, "emp-job-detail.html", {"job": qs})


class JobEditView(UpdateView, SuccessMessageMixin):
    model = Jobs
    form_class = JobForm
    template_name = "emp-job-edit.html"
    success_url = reverse_lazy("emp-all-jobs")
    success_message = "your update done"
    pk_url_kwarg = "id"

    # def get(self, request, id):
    #     qs = Jobs.objects.get(id=id)
    #     form = JobForm(instance=qs)
    #     return render(request, "emp-job-edit.html", {"form": form})

    # def post(self, request, id):
    #     qs = Jobs.objects.get(id=id)
    #     form = JobForm(request.POST, instance=qs)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("emp-all-jobs")
    #     else:
    #         return render(request, "emp-job-edit.html", {"form": form})


class JobDeleteView(DeleteView):
    model = Jobs
    template_name = "emp-job-delete.html"
    success_url = reverse_lazy("emp-all-jobs")
    pk_url_kwarg = "id"
    # def get(self, request, id):
    #     qs = Jobs.objects.get(id=id)
    #     qs.delete()
    #     return redirect("emp-all-jobs")


class SignUpView(CreateView):
    model = Jobs
    form_class = SignUpForm
    template_name = "user-signup.html"
    success_url = reverse_lazy("signin")


class SignInView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("user_name")
            pwd = form.cleaned_data.get("password")
            user = authenticate(request, username=uname, password=pwd)
            if user:
                login(request, user)
                if request.user.role == "employer":
                    return redirect("emp-all-jobs")
                elif request.user.role == "candidate":
                    return redirect("cand-home")
            else:
                return render(request, "cand-login.html", {"form": form})


def sign_out_view(request, *args, **kwargs):
    logout(request)
    return redirect("signin")


class ChangePasswordView(TemplateView):
    template_name = "change-password.html"

    def post(self, request, *args, **kwargs):
        pwd = request.POST.get("pwd")
        uname = request.user
        user = authenticate(request, username=uname, password=pwd)
        if user:
            return redirect("password-reset")
        else:
            return render(request, self.template_name)


class PasswordResetView(TemplateView):
    template_name = "password-reset.html"

    def post(self, request, *args, **kwargs):
        password1 = request.POST.get("pwd1")
        password2 = request.POST.get("pwd2")
        if password1 != password2:
            return render(request, self.template_name, {"msg": "Password missmatch"})
        else:
            u = User.objects.get(username=request.user)
            u.set_password(password1)
            u.save()
            return redirect("signin")


class CompanyProfileView(CreateView):
    model = CompanyProfile
    form_class = CompanyProfileForm
    template_name = "emp-add-profile.html"
    success_url = reverse_lazy("emp-home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your profile has been Added")
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = CompanyProfileForm(request.POST, files=request.FILES)
    #     if form.is_valid():
    #         form.instance.user = request.user
    #         form.save()
    #         return redirect("emp-home")
    #     else:
    #         return request, self.template_name, {"form": form}


class EmpProfileView(TemplateView):
    template_name = "emp-view-profile.html"


class EmpEditProfileView(UpdateView):
    model = CompanyProfile
    form_class = CompanyProfileForm
    template_name = "emp-edit-profile.html"
    success_url = reverse_lazy("emp-profile-view")
    pk_url_kwarg = "id"


class EmpListApplicationsView(ListView):
    model = Application
    context_object_name = "applications"
    template_name = "emp-app-list.html"

    def get_queryset(self):
        return Application.objects.filter(job=self.kwargs.get("id")).exclude(status="cancelled")


class EmApplicationDetailView(DetailView):
    model = Application
    context_object_name = "application"
    template_name = "emp-app-detail.html"
    pk_url_kwarg = "id"
