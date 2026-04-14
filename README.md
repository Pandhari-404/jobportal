<<<<<<< HEAD
# jobportal
=======
# JobSpark – Django Job Portal

A fully functional job portal built with **Django 4+**, **Bootstrap 5**, and **SQLite**.
Converted from a vanilla HTML/CSS/JS frontend — same UI, full backend power.

---

## Quick Start

```bash
# 1. (Optional) create & activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install Django
pip install django

# 3. Apply database migrations
python manage.py migrate

# 4. Seed demo data (8 jobs + 2 demo users)
python manage.py seed_data

# 5. (Optional) create a superuser for the admin panel
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## Demo Accounts

| Role       | Email                  | Password      |
|------------|------------------------|---------------|
| Job Seeker | seeker@demo.com        | password123   |
| Recruiter  | recruiter@demo.com     | password123   |

---

## Project Structure

```
jobspark/
├── manage.py
├── db.sqlite3                   ← auto-created after migrate
├── README.md
│
├── jobspark/                    ← Django project package
│   ├── settings.py              ← All project settings
│   ├── urls.py                  ← Root URL dispatcher
│   ├── wsgi.py
│   └── asgi.py
│
└── jobs/                        ← Main application
    ├── models.py                ← Job, Application, SavedJob
    ├── views.py                 ← 12 function-based views
    ├── forms.py                 ← 4 Django forms
    ├── urls.py                  ← App URL patterns
    ├── admin.py                 ← Admin panel registration
    │
    ├── templatetags/
    │   └── job_tags.py          ← Custom template filters
    │
    ├── management/commands/
    │   └── seed_data.py         ← `python manage.py seed_data`
    │
    ├── migrations/
    │   └── 0001_initial.py
    │
    ├── templates/jobs/
    │   ├── base.html            ← Navbar, footer, dark mode, toasts
    │   ├── home.html            ← Job listings + search + filters
    │   ├── job_detail.html      ← Job detail + apply modal
    │   ├── dashboard.html       ← Seeker & recruiter dashboards
    │   ├── post_job.html        ← Create/edit job form
    │   ├── applicants.html      ← Recruiter applicant management
    │   ├── login.html           ← Login page
    │   └── register.html        ← Registration (seeker/recruiter)
    │
    └── static/jobs/
        ├── css/style.css        ← Full custom CSS + dark mode
        └── js/app.js            ← Dark mode, AJAX save, toasts
```

---

## URL Routes

| URL                              | View                 | Name                |
|----------------------------------|----------------------|---------------------|
| `/`                              | home                 | `home`              |
| `/jobs/<pk>/`                    | job_detail           | `job_detail`        |
| `/jobs/<pk>/save/`               | toggle_save          | `toggle_save`       |
| `/dashboard/`                    | dashboard            | `dashboard`         |
| `/dashboard/applicants/<pk>/`    | view_applicants      | `view_applicants`   |
| `/post-job/`                     | post_job             | `post_job`          |
| `/edit-job/<pk>/`                | edit_job             | `edit_job`          |
| `/delete-job/<pk>/`              | delete_job           | `delete_job`        |
| `/login/`                        | login_view           | `login`             |
| `/register/`                     | register_view        | `register`          |
| `/logout/`                       | logout_view          | `logout`            |
| `/admin/`                        | Django Admin         | —                   |

---

## Features

### Job Seeker
- Browse all active job listings with cards
- Search by title/company and location (server-side)
- Filter by job type and category (server-side)
- View full job details page
- Apply with optional cover letter
- Bookmark/save jobs (AJAX, no page reload)
- Dashboard: view all applications and saved jobs

### Recruiter
- Post new job listings
- Edit existing listings
- Delete listings
- View all applicants per job
- Update application status (Under Review → Accepted/Rejected)
- Dashboard: stats and job table

### General
- Dark mode toggle (persisted in localStorage)
- Bootstrap toast notifications for all actions
- Django admin panel for full data management
- Responsive design (mobile-friendly)
- Django messages → toast notification bridge

---

## Admin Panel

Visit **http://127.0.0.1:8000/admin/** and log in with your superuser.

Models registered:
- **Jobs** – full CRUD, filter by type/category/status
- **Applications** – bulk status updates
- **Saved Jobs** – view all bookmarks

---

## Models

### Job
| Field        | Type         | Description                        |
|--------------|--------------|------------------------------------|
| title        | CharField    | Job title                          |
| company      | CharField    | Company name                       |
| location     | CharField    | City/Remote                        |
| job_type     | CharField    | Full-time / Part-time / Contract   |
| salary       | CharField    | Salary range string                |
| category     | CharField    | Engineering / Design / Data / ...  |
| description  | TextField    | Full job description               |
| requirements | TextField    | One requirement per line           |
| logo         | CharField    | 2-letter abbreviation (e.g. TN)    |
| recruiter    | FK(User)     | Posting user                       |
| posted_at    | DateTimeField| Auto-set on creation               |
| is_active    | BooleanField | Visibility toggle                  |

### Application
| Field        | Type         | Description                        |
|--------------|--------------|------------------------------------|
| job          | FK(Job)      | Applied job                        |
| applicant    | FK(User)     | Applying user                      |
| cover_letter | TextField    | Optional cover letter              |
| status       | CharField    | pending/reviewed/rejected/accepted |
| applied_at   | DateTimeField| Auto-set on creation               |

### SavedJob
| Field    | Type      | Description     |
|----------|-----------|-----------------|
| user     | FK(User)  | Bookmarking user|
| job      | FK(Job)   | Saved job       |
| saved_at | DateTimeField | Auto-set   |

---

## How Recruiter Detection Works

Rather than adding a separate `Profile` model, we use Django's built-in
`User.is_staff` flag:

- `is_staff = True`  → Recruiter (can post/edit/delete jobs, view applicants)
- `is_staff = False` → Job Seeker (can apply, save jobs)

This keeps the codebase simple for an internship-level project.
For production, replace with a `UserProfile` model with a proper `role` field.
>>>>>>> 22dda36 (Initial commit - JobSpark Django project)
