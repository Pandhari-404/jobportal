# JobSpark

A full-stack job portal web application built with **Django**, **Bootstrap 5**, and **SQLite**.

Originally created as a static frontend prototype, JobSpark was rebuilt from the ground up as a complete Django application with authentication, role-based workflows, live search and filtering, applicant tracking, and dark mode support.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://jobspark-ot7t.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

---

## 🌐 Live Demo

👉 **[https://jobspark-ot7t.onrender.com/](https://jobspark-ot7t.onrender.com/)**

> **Note:** Hosted on Render's free tier. If the instance has been sleeping, the first request may take ~30–50 seconds to boot up.

---

## Overview

JobSpark provides two distinct experiences depending on the user's role:

* **Job Seekers** can search listings, filter by job type and category, submit applications with a cover letter, save jobs for later, and track their application review status in real time.
* **Recruiters** have access to a dedicated management dashboard where they can create new job postings, edit or remove listings, and review candidate applications.

The frontend is fully responsive across mobile, tablet, and desktop screens, and includes a dark/light mode toggle that persists across page refreshes via `localStorage`.

---

## Features

### For Job Seekers
* **Search & Filters:** Search by title or company keywords, filter by location, job type (*Full-time, Part-time, Contract, Internship*), and department category (*Engineering, Design, Data, Sales, Marketing, Management*).
* **Job Detail View:** Detailed job descriptions, bulleted requirements, salary ranges, and company badges.
* **Application System:** One-click application with an optional custom cover letter (prevents duplicate applications per job).
* **Saved Jobs:** Bookmark jobs with instant visual feedback to review later.
* **Seeker Dashboard:** Track all submitted applications with live status badges (`Under Review`, `Reviewed`, `Accepted`, `Rejected`).

### For Recruiters
* **Role-Based Access:** Recruiters are assigned elevated permissions (`is_staff = True`) upon registration.
* **Listing Management:** Full CRUD operations — post new vacancies, update descriptions/requirements, and delete inactive listings.
* **Applicant Review:** View all submissions per job posting, inspect candidate names, timestamps, and cover letters.

### Platform & UI/UX
* **Dark / Light Theme:** Persistent theme toggle stored in the browser's `localStorage`.
* **Toast Feedback:** Native Django messages (`messages.success`, `messages.error`, etc.) are mapped to Bootstrap 5 toasts via a custom JavaScript bridge.
* **Secure Authentication:** Standard session-based authentication (login, registration, logout) with CSRF protection and Django password hashing.
* **Django Admin:** Preconfigured admin interface for managing users, listings, and applications.

---

## Tech Stack

* **Backend:** Python 3.10+, Django 5.2
* **Frontend:** HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, Bootstrap Icons
* **Database:** SQLite (default for development; easily swappable with PostgreSQL)
* **WSGI Server:** Gunicorn
* **Static Assets:** WhiteNoise (configured for compressed caching in production)
* **Deployment:** Render

---

## Data Models

The project is structured around three core relational models in `jobs/models.py`:
