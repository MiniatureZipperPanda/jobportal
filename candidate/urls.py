from django.urls import path
from candidate import views

urlpatterns = [
    path('home', views.CandidateHomeView.as_view(), name="cand-home"),
    path('profile/add', views.CandidateProfileView.as_view(), name="cand-add-profile"),
    path('profile/edit', views.CandidateProfileEditView.as_view(), name="cand-edit-profile"),
    path('profile/detail', views.CandidateProfileDetailView.as_view(), name="cand-detail-profile"),
    path('job/all', views.CandidateJobListView.as_view(), name="cand-job-list"),
    path('job/detail/<int:id>', views.CandidateJobDetailView.as_view(), name="cand-job-detail"),
    path('job/apply-now/<int:id>', views.apply_now, name="apply-now"),
    path('job/my-applications', views.MyApplicationsView.as_view(), name="cand-applications"),
    path('cand/account/sign-out', views.cand_sign_out_view, name="cand-log-out"),
    path('application/remove/<int:id>', views.cancel_application, name="cand-cancel-application")
]
