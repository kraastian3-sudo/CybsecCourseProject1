# Django Blog

A simple blog application built with Django. This is the first version, no vulnerabilities yet. Next work on adding log in and the ability for logged in users to create posts.

## Installation

Clone the repository:

    git clone <repository-url>
    cd CybsecCourseProject1

Create a virtual environment:

    python3 -m venv .venv

Activate it:

    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate

Create an admin user:

    python manage.py createsuperuser

Start the server:

    python manage.py runserver

Blog:
http://127.0.0.1:8000/

Admin:
http://127.0.0.1:8000/admin/
