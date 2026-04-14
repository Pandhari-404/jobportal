"""
jobs/models.py
==============
Database models for the JobSpark portal.

Models:
  - Job          : A job posting (title, company, location, etc.)
  - Application  : A user's application to a job (linked to Django auth User)
  - SavedJob     : Bookmarked / saved job per user
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Job(models.Model):
    """Represents a single job posting."""

    # ── Job Type choices ──────────────────────────────────────
    FULL_TIME  = 'Full-time'
    PART_TIME  = 'Part-time'
    CONTRACT   = 'Contract'
    INTERNSHIP = 'Internship'

    JOB_TYPE_CHOICES = [
        (FULL_TIME,  'Full-time'),
        (PART_TIME,  'Part-time'),
        (CONTRACT,   'Contract'),
        (INTERNSHIP, 'Internship'),
    ]

    # ── Category choices ──────────────────────────────────────
    ENGINEERING = 'Engineering'
    DESIGN      = 'Design'
    DATA        = 'Data'
    MANAGEMENT  = 'Management'
    MARKETING   = 'Marketing'
    SALES       = 'Sales'
    OTHER       = 'Other'

    CATEGORY_CHOICES = [
        (ENGINEERING, 'Engineering'),
        (DESIGN,      'Design'),
        (DATA,        'Data'),
        (MANAGEMENT,  'Management'),
        (MARKETING,   'Marketing'),
        (SALES,       'Sales'),
        (OTHER,       'Other'),
    ]

    # ── Core Fields ───────────────────────────────────────────
    title        = models.CharField(max_length=200)
    company      = models.CharField(max_length=200)
    location     = models.CharField(max_length=200)
    job_type     = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default=FULL_TIME)
    salary       = models.CharField(max_length=100, blank=True, default='Negotiable')
    category     = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=ENGINEERING)
    description  = models.TextField()
    requirements = models.TextField(blank=True, help_text='One requirement per line')
    logo         = models.CharField(max_length=5, blank=True,
                                    help_text='2-letter abbreviation shown on card (e.g. TN)')

    # ── Recruiter (owner) ─────────────────────────────────────
    recruiter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='posted_jobs',
    )

    # ── Timestamps ────────────────────────────────────────────
    posted_at  = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # ── Active flag ───────────────────────────────────────────
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-posted_at']   # Newest first
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return f"{self.title} @ {self.company}"

    # ── Helpers ───────────────────────────────────────────────
    def get_logo(self):
        """Return logo abbreviation; fall back to first two letters of company."""
        return self.logo or self.company[:2].upper()

    def requirements_as_list(self):
        """Split multi-line requirements into a Python list."""
        return [r.strip() for r in self.requirements.splitlines() if r.strip()]

    def get_type_badge_class(self):
        """Return CSS class for the job-type badge."""
        mapping = {
            self.FULL_TIME:  'badge-fulltime',
            self.CONTRACT:   'badge-contract',
            self.PART_TIME:  'badge-parttime',
            self.INTERNSHIP: 'badge-parttime',
        }
        return mapping.get(self.job_type, 'badge-fulltime')


class Application(models.Model):
    """A job-seeker's application to a specific job."""

    STATUS_PENDING  = 'pending'
    STATUS_REVIEWED = 'reviewed'
    STATUS_REJECTED = 'rejected'
    STATUS_ACCEPTED = 'accepted'

    STATUS_CHOICES = [
        (STATUS_PENDING,  'Under Review'),
        (STATUS_REVIEWED, 'Reviewed'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_ACCEPTED, 'Accepted'),
    ]

    job          = models.ForeignKey(Job,  on_delete=models.CASCADE, related_name='applications')
    applicant    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    applied_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only apply once per job
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.get_full_name() or self.applicant.username} → {self.job.title}"

    def get_status_badge_class(self):
        mapping = {
            self.STATUS_PENDING:  'bg-warning text-dark',
            self.STATUS_REVIEWED: 'bg-info text-dark',
            self.STATUS_REJECTED: 'bg-danger',
            self.STATUS_ACCEPTED: 'bg-success',
        }
        return mapping.get(self.status, 'bg-secondary')


class SavedJob(models.Model):
    """A bookmarked / saved job for a user."""

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job        = models.ForeignKey(Job,  on_delete=models.CASCADE, related_name='saved_by')
    saved_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
