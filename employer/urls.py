from django.urls import path
from employer import views

urlpatterns = [
    path('home', views.EmployerHomeView.as_view(), name="emp-home"),
    path('jobs/add', views.AddJobView.as_view(), name="emp-add-job"),
    path('jobs/all', views.ListJobView.as_view(), name="emp-all-jobs"),
    path('jobs/details/<int:id>', views.JobDetailView.as_view(), name="emp-job-detail"),
    path('jobs/change/<int:id>', views.JobEditView.as_view(), name="emp-job-edit"),
    path('jobs/delete/<int:id>', views.JobDeleteView.as_view(), name="emp-job-delete"),
    path('users/account/signup', views.SignUpView.as_view(), name="signup"),
    path('users/account/signin', views.SignInView.as_view(), name="signin"),
    path('users/account/sign-out', views.sign_out_view, name="sign-out"),
    path('users/account/change-password', views.ChangePasswordView.as_view(), name="chane-password"),
    path('users/account/password-reset', views.PasswordResetView.as_view(), name="password-reset"),
    path('profile/add',views.CompanyProfileView.as_view(),name="emp-add-profile")


]
