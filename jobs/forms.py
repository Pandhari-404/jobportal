"""
jobs/forms.py
=============
All Django forms used in the JobSpark portal.

Forms:
  - JobSearchForm    : Hero search bar + sidebar filters
  - JobForm          : Create / edit a job posting (recruiter)
  - ApplicationForm  : Apply to a job with optional cover letter
  - RegisterForm     : User registration (seeker or recruiter)
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Job, Application


# ── Search & Filter ────────────────────────────────────────────
class JobSearchForm(forms.Form):
    """Powers the hero search bar and sidebar filter panel."""

    q        = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'id':          'searchTitle',
            'placeholder': 'Job title or company…',
            'class':       'hero-search-input',
            'autocomplete': 'off',
        }),
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'id':          'searchLocation',
            'placeholder': 'Location or Remote…',
            'class':       'hero-search-input',
            'autocomplete': 'off',
        }),
    )
    job_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Job.JOB_TYPE_CHOICES,
        widget=forms.Select(attrs={'id': 'filterType', 'class': 'form-select form-select-sm'}),
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Job.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'id': 'filterCategory', 'class': 'form-select form-select-sm'}),
    )


# ── Job Form (create / edit) ───────────────────────────────────
class JobForm(forms.ModelForm):
    """Used by recruiters to post or edit a job."""

    class Meta:
        model  = Job
        fields = [
            'title', 'company', 'location', 'job_type',
            'salary', 'category', 'description', 'requirements',
        ]
        widgets = {
            'title':        forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Senior Frontend Developer',
            }),
            'company':      forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. TechNova Inc.',
            }),
            'location':     forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Bangalore, IN or Remote',
            }),
            'job_type':     forms.Select(attrs={'class': 'form-select'}),
            'salary':       forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. ₹8–12 LPA',
            }),
            'category':     forms.Select(attrs={'class': 'form-select'}),
            'description':  forms.Textarea(attrs={
                'class': 'form-control',
                'rows':  5,
                'placeholder': 'Describe the role, responsibilities, culture…',
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows':  4,
                'placeholder': 'One requirement per line…',
            }),
        }

    def save(self, commit=True, recruiter=None):
        """Attach the recruiter user before saving."""
        job = super().save(commit=False)
        # Auto-derive logo from company name if not provided
        if not job.logo:
            job.logo = job.company[:2].upper()
        if recruiter:
            job.recruiter = recruiter
        if commit:
            job.save()
        return job


# ── Application Form ───────────────────────────────────────────
class ApplicationForm(forms.ModelForm):
    """Cover letter form shown in the apply modal."""

    class Meta:
        model  = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class':       'form-control',
                'rows':        5,
                'id':          'coverLetter',
                'placeholder': 'Introduce yourself and explain why you\'re a great fit…',
            }),
        }
        labels = {
            'cover_letter': 'Cover Letter (optional)',
        }


# ── Registration Form ──────────────────────────────────────────
class RegisterForm(UserCreationForm):
    """Extended registration form with name + role selection."""

    ROLE_CHOICES = [
        ('seeker',    'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]

    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class':       'form-control border-start-0',
            'placeholder': 'Your full name',
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class':       'form-control border-start-0',
            'placeholder': 'you@example.com',
        }),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.HiddenInput(attrs={'id': 'regRole'}),
        initial='seeker',
    )

    class Meta:
        model  = User
        fields = ['first_name', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style the password fields
        self.fields['password1'].widget.attrs.update({
            'class':       'form-control border-start-0',
            'placeholder': 'Min. 6 characters',
            'id':          'regPassword',
        })
        self.fields['password2'].widget.attrs.update({
            'class':       'form-control border-start-0',
            'placeholder': 'Re-enter password',
            'id':          'regPassword2',
        })
        # Remove the default help texts (they are shown in tooltips on the frontend)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def save(self, commit=True):
        """
        Use the email as the username (unique identifier).
        Store role in the user's profile (we use a simple approach:
        staff flag for recruiters, ordinary user for seekers).
        """
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        # Username = email (ensures uniqueness)
        user.username   = email
        user.email      = email
        user.first_name = self.cleaned_data['first_name']
        # Recruiters are flagged so we can tell them apart without a Profile model
        user.is_staff   = (self.cleaned_data['role'] == 'recruiter')
        if commit:
            user.save()
        return user
