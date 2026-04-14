"""
jobs/views.py
=============
All function-based views for the JobSpark portal.

Views:
  home            – Job listing page with search & filter
  job_detail      – Single job detail + apply action
  dashboard       – User dashboard (seeker or recruiter)
  post_job        – Create a new job posting (recruiter only)
  edit_job        – Edit an existing job posting (recruiter only)
  delete_job      – Delete a job posting (recruiter only)
  toggle_save     – Bookmark / un-bookmark a job (AJAX-friendly)
  login_view      – Custom login page
  register_view   – Registration page
  logout_view     – Logout
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Job, Application, SavedJob
from .forms import JobSearchForm, JobForm, ApplicationForm, RegisterForm


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def is_recruiter(user):
    """Return True if the authenticated user is a recruiter (is_staff flag)."""
    return user.is_authenticated and user.is_staff


# ─────────────────────────────────────────────────────────────
# HOME — Job Listings
# ─────────────────────────────────────────────────────────────

def home(request):
    """
    Main landing page.
    Displays the hero section, search bar, filter sidebar, and job cards.
    Supports GET parameters: q, location, job_type, category
    """
    form = JobSearchForm(request.GET or None)
    jobs = Job.objects.filter(is_active=True).select_related('recruiter')

    # Apply search / filter from query parameters
    if form.is_valid():
        q        = form.cleaned_data.get('q', '').strip()
        location = form.cleaned_data.get('location', '').strip()
        job_type = form.cleaned_data.get('job_type', '')
        category = form.cleaned_data.get('category', '')

        if q:
            jobs = jobs.filter(
                Q(title__icontains=q) | Q(company__icontains=q)
            )
        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if category:
            jobs = jobs.filter(category=category)

    # Collect saved job IDs for the current user (to show filled bookmark icons)
    saved_ids = set()
    applied_ids = set()
    if request.user.is_authenticated:
        saved_ids   = set(SavedJob.objects.filter(
            user=request.user).values_list('job_id', flat=True))
        applied_ids = set(Application.objects.filter(
            applicant=request.user).values_list('job_id', flat=True))

    context = {
        'jobs':        jobs,
        'form':        form,
        'job_count':   jobs.count(),
        'saved_ids':   saved_ids,
        'applied_ids': applied_ids,
    }
    return render(request, 'jobs/home.html', context)


# ─────────────────────────────────────────────────────────────
# JOB DETAIL
# ─────────────────────────────────────────────────────────────

def job_detail(request, pk):
    """
    Full job detail page.
    Handles the apply form submission (POST).
    """
    job   = get_object_or_404(Job, pk=pk, is_active=True)
    form  = ApplicationForm()
    saved = False
    applied = False

    if request.user.is_authenticated:
        saved   = SavedJob.objects.filter(user=request.user, job=job).exists()
        applied = Application.objects.filter(applicant=request.user, job=job).exists()

    # ── Handle apply form submission ──────────────────────────
    if request.method == 'POST' and 'apply' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to apply.')
            return redirect('login')

        if applied:
            messages.warning(request, 'You have already applied for this job.')
        else:
            form = ApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.job       = job
                application.applicant = request.user
                application.save()
                messages.success(request, 'Application submitted successfully! 🎉')
                return redirect('job_detail', pk=pk)

    context = {
        'job':     job,
        'form':    form,
        'saved':   saved,
        'applied': applied,
    }
    return render(request, 'jobs/job_detail.html', context)


# ─────────────────────────────────────────────────────────────
# TOGGLE SAVE (Bookmark)
# ─────────────────────────────────────────────────────────────

@login_required
@require_POST
def toggle_save(request, pk):
    """
    Bookmark or un-bookmark a job.
    Accepts POST; returns JSON for AJAX calls or redirects for normal forms.
    """
    job   = get_object_or_404(Job, pk=pk)
    obj, created = SavedJob.objects.get_or_create(user=request.user, job=job)

    if not created:
        # Already saved → remove it
        obj.delete()
        now_saved = False
        msg = 'Job removed from saved.'
    else:
        now_saved = True
        msg = 'Job saved! ★'

    # AJAX request → return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': now_saved, 'message': msg})

    # Normal form POST → redirect back
    messages.success(request, msg)
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)


# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """
    User dashboard.
    - Job seekers  : see applications and saved jobs.
    - Recruiters   : see their posted jobs and applicant counts.
    """
    user = request.user

    if is_recruiter(user):
        # ── Recruiter dashboard ───────────────────────────────
        my_jobs    = Job.objects.filter(recruiter=user).prefetch_related('applications')
        total_apps = sum(j.applications.count() for j in my_jobs)

        context = {
            'is_recruiter': True,
            'my_jobs':      my_jobs,
            'total_apps':   total_apps,
        }
    else:
        # ── Seeker dashboard ──────────────────────────────────
        my_apps   = (Application.objects
                     .filter(applicant=user)
                     .select_related('job')
                     .order_by('-applied_at'))
        saved_jobs = (SavedJob.objects
                      .filter(user=user)
                      .select_related('job')
                      .order_by('-saved_at'))

        # For saved job cards we need saved/applied sets
        saved_ids   = {s.job_id for s in saved_jobs}
        applied_ids = {a.job_id for a in my_apps}

        context = {
            'is_recruiter': False,
            'my_apps':      my_apps,
            'saved_jobs':   [s.job for s in saved_jobs],
            'saved_ids':    saved_ids,
            'applied_ids':  applied_ids,
        }

    return render(request, 'jobs/dashboard.html', context)


# ─────────────────────────────────────────────────────────────
# VIEW APPLICANTS (Recruiter)
# ─────────────────────────────────────────────────────────────

@login_required
def view_applicants(request, pk):
    """Show all applicants for a specific job (recruiter only).
    Also handles POST requests to update application status."""
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)

    # Handle status update POST from the dropdown on the applicants page
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        status = request.POST.get('status')
        if app_id and status:
            Application.objects.filter(pk=app_id, job=job).update(status=status)
            messages.success(request, 'Application status updated.')
        return redirect('view_applicants', pk=pk)

    applicants = (Application.objects
                  .filter(job=job)
                  .select_related('applicant')
                  .order_by('-applied_at'))
    return render(request, 'jobs/applicants.html', {
        'job':        job,
        'applicants': applicants,
    })


# ─────────────────────────────────────────────────────────────
# POST JOB (Recruiter)
# ─────────────────────────────────────────────────────────────

@login_required
def post_job(request):
    """Create a new job posting. Restricted to recruiters."""
    if not is_recruiter(request.user):
        messages.error(request, 'Only recruiters can post jobs.')
        return redirect('home')

    form = JobForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(recruiter=request.user)
        messages.success(request, 'Job posted successfully! 🚀')
        return redirect('dashboard')

    return render(request, 'jobs/post_job.html', {
        'form':     form,
        'is_edit':  False,
        'heading':  'Post a New Job',
        'btn_text': 'Post Job',
    })


# ─────────────────────────────────────────────────────────────
# EDIT JOB (Recruiter)
# ─────────────────────────────────────────────────────────────

@login_required
def edit_job(request, pk):
    """Edit an existing job posting. Only the owner can edit."""
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    form = JobForm(request.POST or None, instance=job)

    if request.method == 'POST' and form.is_valid():
        form.save(recruiter=request.user)
        messages.success(request, 'Job updated successfully! ✅')
        return redirect('dashboard')

    return render(request, 'jobs/post_job.html', {
        'form':     form,
        'job':      job,
        'is_edit':  True,
        'heading':  'Edit Job',
        'btn_text': 'Update Job',
    })


# ─────────────────────────────────────────────────────────────
# DELETE JOB (Recruiter)
# ─────────────────────────────────────────────────────────────

@login_required
@require_POST
def delete_job(request, pk):
    """Delete a job posting. Only the owner can delete."""
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    job.delete()
    messages.success(request, 'Job deleted.')
    return redirect('dashboard')


# ─────────────────────────────────────────────────────────────
# AUTH — Login
# ─────────────────────────────────────────────────────────────

def login_view(request):
    """Custom login page."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        # We use email as username (set during registration)
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.email}! 👋')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'jobs/login.html')


# ─────────────────────────────────────────────────────────────
# AUTH — Register
# ─────────────────────────────────────────────────────────────

def register_view(request):
    """Registration page for both seekers and recruiters."""
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created! Welcome to JobSpark 🚀')
        return redirect('home')

    return render(request, 'jobs/register.html', {'form': form})


# ─────────────────────────────────────────────────────────────
# AUTH — Logout
# ─────────────────────────────────────────────────────────────

def logout_view(request):
    """Log the user out and redirect to home."""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

