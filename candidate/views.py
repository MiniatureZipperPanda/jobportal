from candidate.forms import CandidateProfileForm, CandidateProfileEditForm
from django.views.generic import TemplateView, CreateView, FormView, DetailView, ListView
from candidate.models import CandidateProfile
from django.urls import reverse_lazy
from employer.models import User, Jobs, Application
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout


class CandidateHomeView(TemplateView):
    template_name = "candidate/can-home.html"


def cand_sign_out_view(request, *args, **kwargs):
    logout(request)
    return redirect("signin")


class CandidateProfileView(CreateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = "candidate/can-profile.html"
    success_url = reverse_lazy("cand-home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your profile has been Added")
        return super().form_valid(form)


class CandidateProfileDetailView(TemplateView):
    template_name = "candidate/cand-profile-detail.html"


class CandidateProfileEditView(FormView):
    model = CandidateProfile
    template_name = "candidate/cand-profile-edit.html"
    form_class = CandidateProfileEditForm

    def get(self, request, *args, **kwargs):
        profile = CandidateProfile.objects.get(user=request.user)
        form = CandidateProfileEditForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone,
            'email': request.user.email,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        profile = CandidateProfile.objects.get(user=request.user)
        form = self.form_class(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data.pop('first_name')
            last_name = form.cleaned_data.pop('last_name')
            phone = form.cleaned_data.pop('phone')
            email = form.cleaned_data.pop('email')
            form.save()
            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name_name = last_name
            user.phone = phone
            user.email = email
            user.save()
            messages.success(request, "your profile has been updated")
            return redirect('cand-home')
        else:
            messages.error(request, "Error Occurred")
            return render(request, "candidate/cand-profile-edit.html", {"form": form})


class CandidateJobListView(ListView):
    model = Jobs
    context_object_name = "jobs"
    template_name = "candidate/cand-joblist.html"

    def get_queryset(self):
        return self.model.objects.all().order_by("-created_date")


class CandidateJobDetailView(DetailView):
    model = Jobs
    context_object_name = "job"
    template_name = "candidate/cand-job-detail.html"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_applied = Application.objects.filter(applicant=self.request.user, job=self.object)
        context["is_applied"] = is_applied
        return context


def apply_now(request, *args, **kwargs):
    user = request.user
    job_id = kwargs.get("id")
    job = Jobs.objects.get(id=job_id)
    Application.objects.create(applicant=user,
                               job=job)
    messages.success(request, "your application has been posted successfully")
    return redirect("cand-home")


class MyApplicationsView(ListView):
    model = Application
    template_name = "candidate/cand-applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)


def cancel_application(request, *args, **kwargs):
    app_id = kwargs.get("id")
    application = Application.objects.get(id=app_id)
    application.status = "cancelled"
    application.save()
    messages.success(request, "Your Application Cancelled Successfully")
    return redirect("cand-home")
