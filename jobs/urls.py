"""
jobs/urls.py
============
URL patterns for the JobSpark 'jobs' application.

Pattern       View              Name
-----------   ---------------   ---------------
/             home              home
/jobs/<pk>/   job_detail        job_detail
/jobs/<pk>/save/  toggle_save   toggle_save
/dashboard/   dashboard         dashboard
/dashboard/applicants/<pk>/  view_applicants  view_applicants
/post-job/    post_job          post_job
/edit-job/<pk>/  edit_job       edit_job
/delete-job/<pk>/  delete_job   delete_job
/login/       login_view        login
/register/    register_view     register
/logout/      logout_view       logout
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Public pages ──────────────────────────────────────────
    path('',               views.home,        name='home'),
    path('jobs/<int:pk>/', views.job_detail,  name='job_detail'),

    # ── Auth ──────────────────────────────────────────────────
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),

    # ── Authenticated user actions ────────────────────────────
    path('jobs/<int:pk>/save/',   views.toggle_save,     name='toggle_save'),
    path('dashboard/',            views.dashboard,        name='dashboard'),
    path('dashboard/applicants/<int:pk>/', views.view_applicants, name='view_applicants'),

    # ── Recruiter job management ──────────────────────────────
    path('post-job/',              views.post_job,   name='post_job'),
    path('edit-job/<int:pk>/',     views.edit_job,   name='edit_job'),
    path('delete-job/<int:pk>/',   views.delete_job, name='delete_job'),
]
