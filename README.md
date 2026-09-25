<div align="center">

# ⚡ JobSpark — Full-Stack Django Job Portal

<p align="center">
  <strong>A modern, responsive recruitment and job-hunting web application built with Python, Django 5, Bootstrap 5, and SQLite.</strong>
</p>

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://jobspark-ot7t.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.style=for-the-badge)](LICENSE)

<br />

<p align="center">
  <a href="https://jobspark-ot7t.onrender.com/"><strong>Explore Live Demo »</strong></a>
  <br />
  <a href="#-about-jobspark">About</a> •
  <a href="#-live-demo">Live Demo</a> •
  <a href="#-key-features">Key Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-local-setup--installation">Local Setup</a> •
  <a href="#-deployment">Deployment</a>
</p>

</div>

---

## 📖 About JobSpark

**JobSpark** is a full-featured job board web application engineered to bridge the gap between job seekers and hiring managers. Originally designed as a vanilla static HTML/CSS/JavaScript layout, it has been transformed into a dynamic, production-ready Django application backed by a relational database, custom role-based authentication, and a responsive frontend with dark mode support.

Whether you are a job seeker aiming to discover opportunities and track applications or a recruiter looking to post vacancies and review talent, JobSpark offers a frictionless, intuitive experience.

---

## 🌐 Live Demo

👉 [https://jobspark-ot7t.onrender.com/](https://jobspark-ot7t.onrender.com/)

> 🚀 **Try it out live:** Experience real-time job searching, application tracking, dark mode toggle, and recruiter job posting on the live deployment. *(Note: Render free tier services may take a few seconds to spin up on initial load).*

---

## 🚀 Key Features

### 🔍 For Job Seekers
* **Smart Search & Filters:** Search jobs by keywords (title/company), location, employment type (Full-time, Part-time, Contract, Internship), and industry category (Engineering, Design, Data, Management, Marketing, Sales).
* **Detailed Job Overviews:** View complete job descriptions, requirements lists, company logos/badges, and salary ranges.
* **Streamlined Applications:** Apply directly to jobs with a tailored cover letter in one click.
* **Applicant Dashboard:** Monitor the live review status of every application (`Under Review`, `Reviewed`, `Accepted`, `Rejected`).
* **Saved Jobs / Bookmarks:** Save listings to revisit later with instant UI state toggling.

### 💼 For Recruiters & Employers
* **Role-Based Access Control (RBAC):** Dedicated recruiter accounts empowered with posting and candidate management capabilities.
* **Recruiter Dashboard:** Comprehensive overview of posted jobs, applicant counters, and candidate submissions.
* **Listing Management:** Full CRUD capability — create new job postings, edit existing vacancies, or archive/delete listings.
* **Applicant Review Portal:** View applicant profiles, inspect submitted cover letters, and track hiring decisions per job.

### 🎨 UI, UX & System Highlights
* **🌙 Dark / Light Mode Toggle:** Seamless theme switching with state persistence stored via `localStorage`.
* **🔔 Dynamic Toast Notifications:** Native Django messages (`messages.success`, `messages.info`, `messages.warning`, `messages.error`) bridge directly into animated Bootstrap 5 toasts.
* **📱 Fully Responsive Design:** Clean layout optimized for mobile screens, tablets, and desktops.
* **🔐 Robust Security:** Form validation, CSRF protection, secure password hashing, and login-restricted endpoints.
* **🛠️ Django Admin Suite:** Powerful built-in admin dashboard for complete management of users, jobs, applications, and bookmarks.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend Framework** | [Python 3](https://www.python.org/) & [Django 5](https://www.djangoproject.com/) |
| **Frontend UI** | HTML5, CSS3, JavaScript (ES6+), [Bootstrap 5](https://getbootstrap.com/), Bootstrap Icons |
| **Database** | SQLite3 (development & default; fully swappable with PostgreSQL / MySQL) |
| **WSGI / Web Server** | [Gunicorn](https://gunicorn.org/) |
| **Static Asset Serving** | [WhiteNoise](http://whitenoise.evans.io/) (compressed manifest caching) |
| **Hosting & Cloud** | [Render](https://render.com/) |

---

## 📂 Project Structure

```text
jobspark/
│
├── build.sh                  # Deployment build script (migrations & collectstatic)
├── db.sqlite3                # SQLite database (local development)
├── manage.py                 # Django command-line runner
├── requirements.txt          # Python package dependencies
│
├── jobspark/                 # Core Project Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Installed apps, middleware, database & WhiteNoise config
│   ├── urls.py               # Root URL dispatcher
│   └── wsgi.py               # WSGI entrypoint for Gunicorn
│
└── jobs/                     # Main Application
    ├── admin.py              # Model registrations for Django Admin
    ├── apps.py               # App configuration
    ├── forms.py              # Search, Job Creation, Application & Registration forms
    ├── models.py             # Job, Application, and SavedJob database models
    ├── urls.py               # Application-level routing endpoints
    ├── views.py              # View controllers (search, auth, dashboards, CRUD)
    │
    ├── static/               # Static assets
    │   ├── bot-logo.png
    │   └── jobs/
    │       ├── css/style.css # Custom themes, dark mode variables & styling
    │       └── js/app.js     # Dark mode handler, toasts & interactive UI logic
    │
    └── templates/jobs/       # Modular Django HTML Templates
        ├── base.html         # Base skeleton (navbar, toast bridge, footer)
        ├── home.html         # Job search, filters & card listings
        ├── job_detail.html   # Job specification & application modal/form
        ├── dashboard.html    # Unified seeker / recruiter dashboard
        ├── applicants.html   # Recruiter applicant review list
        ├── post_job.html     # Create and edit job form
        ├── login.html        # Authentication login page
        └── register.html     # Registration with Seeker/Recruiter role selection
