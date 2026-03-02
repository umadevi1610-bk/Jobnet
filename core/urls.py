from django.contrib import admin
from django.urls import path
from core import views
from core.admin import jobnet_admin  # Custom admin import
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

# Root redirect → login page
def root_redirect(request):
    return redirect("login")

urlpatterns = [
    # ===== Custom Admin Site =====
    path("admin/", jobnet_admin.urls),

    # ===== Auth / User Management =====
    path("", root_redirect, name="root_redirect"),  # Root → Login
    path(
    "login/",
    auth_views.LoginView.as_view(
        template_name="core/auth.html",
        redirect_authenticated_user=True,
        next_page="home"  # ← Add this
    ),
    name="login"
),

    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", views.signup, name="signup"),

    # ===== Job Flow URLs =====
    path("home/", views.home, name="home"),  # Login success → Home
    path("jobbot/", views.jobbot, name="jobbot"),
    path("upload/", views.upload_resume, name="upload_resume"),
    path("match/", views.jobs_match, name="jobs_match"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_to_job"),
    path("cover/<str:job_title>/", views.cover_letter, name="cover_letter"),
    path("success/", views.application_success, name="application_success"),

    # ===== Internship Flow URLs =====
    path("intern/upload/", views.intern_upload, name="intern_upload"),
    path("intern/match/", views.intern_match, name="intern_match"),
    path("intern/apply/<int:intern_id>/", views.intern_apply, name="internship_apply"),
    path("intern/success/", views.intern_success, name="intern_success"),
]
