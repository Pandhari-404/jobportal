"""
jobs/management/commands/seed_data.py
======================================
Management command to populate the database with sample jobs
and two demo user accounts (seeker + recruiter).

Usage:
    python manage.py seed_data
    python manage.py seed_data --clear   # wipe existing data first
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Job, Application, SavedJob


DEMO_JOBS = [
    {
        "title": "Frontend Developer",
        "company": "TechNova Inc.",
        "logo": "TN",
        "location": "Bangalore, IN",
        "job_type": Job.FULL_TIME,
        "salary": "₹8–12 LPA",
        "category": Job.ENGINEERING,
        "description": (
            "We are looking for a skilled Frontend Developer proficient in React, "
            "HTML5, CSS3, and JavaScript. You will collaborate with our design team "
            "to build responsive, performant UIs that delight our users."
        ),
        "requirements": (
            "2+ years experience with React\n"
            "Strong CSS & Bootstrap skills\n"
            "Git workflow familiarity\n"
            "Good communication skills"
        ),
    },
    {
        "title": "UI/UX Designer",
        "company": "Pixel Studios",
        "logo": "PS",
        "location": "Remote",
        "job_type": Job.CONTRACT,
        "salary": "₹6–9 LPA",
        "category": Job.DESIGN,
        "description": (
            "Pixel Studios seeks a creative UI/UX Designer to craft intuitive digital "
            "experiences. You will conduct user research, build wireframes, and work "
            "closely with our engineering team to bring designs to life."
        ),
        "requirements": (
            "Proficiency in Figma & Adobe XD\n"
            "Portfolio of shipped products\n"
            "Understanding of usability principles\n"
            "1+ year professional experience"
        ),
    },
    {
        "title": "Data Analyst",
        "company": "Insight Analytics",
        "logo": "IA",
        "location": "Mumbai, IN",
        "job_type": Job.FULL_TIME,
        "salary": "₹7–10 LPA",
        "category": Job.DATA,
        "description": (
            "Join our growing data team to translate raw numbers into actionable "
            "business intelligence. You will work with Python, SQL, and BI dashboards "
            "to drive product and marketing strategy."
        ),
        "requirements": (
            "SQL proficiency\n"
            "Python / Pandas experience\n"
            "Tableau or Power BI knowledge\n"
            "Statistical reasoning skills"
        ),
    },
    {
        "title": "Backend Engineer",
        "company": "CloudBase",
        "logo": "CB",
        "location": "Hyderabad, IN",
        "job_type": Job.FULL_TIME,
        "salary": "₹10–16 LPA",
        "category": Job.ENGINEERING,
        "description": (
            "CloudBase is hiring a Backend Engineer to design and build scalable "
            "microservices. Experience with Node.js or Python FastAPI is required. "
            "You will own services end-to-end from design to deployment."
        ),
        "requirements": (
            "Node.js or Python FastAPI\n"
            "REST API design patterns\n"
            "Postgres / MongoDB\n"
            "Docker & Kubernetes basics"
        ),
    },
    {
        "title": "Product Manager",
        "company": "LaunchPad",
        "logo": "LP",
        "location": "Delhi, IN",
        "job_type": Job.FULL_TIME,
        "salary": "₹12–18 LPA",
        "category": Job.MANAGEMENT,
        "description": (
            "Drive the product roadmap and strategy for LaunchPad's flagship SaaS "
            "product. You'll work cross-functionally with engineering, design, and "
            "sales teams to deliver value to thousands of customers."
        ),
        "requirements": (
            "3+ years product management experience\n"
            "Agile / Scrum methodology\n"
            "Strong analytical mindset\n"
            "Excellent stakeholder management"
        ),
    },
    {
        "title": "DevOps Engineer",
        "company": "InfraHub",
        "logo": "IH",
        "location": "Pune, IN",
        "job_type": Job.FULL_TIME,
        "salary": "₹9–14 LPA",
        "category": Job.ENGINEERING,
        "description": (
            "InfraHub is looking for a DevOps Engineer to own CI/CD pipelines, "
            "cloud infrastructure (AWS/GCP), and platform reliability. You will "
            "automate everything and keep our 99.9% uptime SLA."
        ),
        "requirements": (
            "AWS / GCP experience\n"
            "Terraform & Ansible\n"
            "Kubernetes administration\n"
            "Monitoring with Prometheus/Grafana"
        ),
    },
    {
        "title": "Content Writer",
        "company": "Wordsmith Co.",
        "logo": "WC",
        "location": "Remote",
        "job_type": Job.PART_TIME,
        "salary": "₹3–5 LPA",
        "category": Job.MARKETING,
        "description": (
            "Create compelling blog posts, case studies, and social media copy for "
            "B2B tech clients. You will research topics, interview SMEs, and deliver "
            "SEO-optimised content that drives organic traffic."
        ),
        "requirements": (
            "Excellent written English\n"
            "SEO fundamentals\n"
            "Strong research skills\n"
            "Ability to meet deadlines"
        ),
    },
    {
        "title": "Mobile App Developer",
        "company": "AppForge",
        "logo": "AF",
        "location": "Chennai, IN",
        "job_type": Job.FULL_TIME,
        "salary": "₹8–13 LPA",
        "category": Job.ENGINEERING,
        "description": (
            "AppForge is hiring a React Native developer to build cross-platform "
            "mobile applications for enterprise clients. You will own the full "
            "development lifecycle from design to App Store release."
        ),
        "requirements": (
            "React Native proficiency\n"
            "iOS & Android deployment experience\n"
            "REST API integration\n"
            "Redux state management"
        ),
    },
]


class Command(BaseCommand):
    help = 'Seed the database with demo users and sample job listings.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing jobs, applications, and saved jobs first.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data…')
            SavedJob.objects.all().delete()
            Application.objects.all().delete()
            Job.objects.all().delete()
            User.objects.filter(username__in=[
                'seeker@demo.com', 'recruiter@demo.com'
            ]).delete()
            self.stdout.write(self.style.WARNING('Existing data cleared.'))

        # ── Create demo recruiter ─────────────────────────────
        recruiter, created = User.objects.get_or_create(
            username='recruiter@demo.com',
            defaults={
                'email':      'recruiter@demo.com',
                'first_name': 'Demo Recruiter',
                'is_staff':   True,   # Marks them as recruiter
            }
        )
        if created:
            recruiter.set_password('password123')
            recruiter.save()
            self.stdout.write(self.style.SUCCESS(
                '✓ Recruiter created  →  recruiter@demo.com / password123'
            ))
        else:
            self.stdout.write('  Recruiter already exists, skipping.')

        # ── Create demo seeker ────────────────────────────────
        seeker, created = User.objects.get_or_create(
            username='seeker@demo.com',
            defaults={
                'email':      'seeker@demo.com',
                'first_name': 'Demo Seeker',
                'is_staff':   False,
            }
        )
        if created:
            seeker.set_password('password123')
            seeker.save()
            self.stdout.write(self.style.SUCCESS(
                '✓ Seeker created     →  seeker@demo.com / password123'
            ))
        else:
            self.stdout.write('  Seeker already exists, skipping.')

        # ── Seed job listings ─────────────────────────────────
        jobs_created = 0
        for data in DEMO_JOBS:
            _, created = Job.objects.get_or_create(
                title=data['title'],
                company=data['company'],
                defaults={**data, 'recruiter': recruiter},
            )
            if created:
                jobs_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'✓ {jobs_created} job(s) seeded  '
            f'({Job.objects.count()} total in DB)'
        ))
        self.stdout.write(self.style.SUCCESS(
            '\n🚀  Seed complete! Run: python manage.py runserver'
        ))
