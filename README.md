# Django Blog

## Installation

This project was made with the https://owasp.org/Top10/2025/ list.

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

# Testing the vulnerabilities

First when you open the site you should see a homepage like this.

<img width="1418" height="445" alt="image" src="https://github.com/user-attachments/assets/16074dc1-b863-447e-bd78-5cbb5818c75a" />

Click register and create an account with a simple username like 1234.
Afterwards you should be logged in. Now you can create your first post.

<img width="1418" height="445" alt="image" src="https://github.com/user-attachments/assets/a429dfac-b64b-46b3-be19-14502c40ce48" />

After creating your first post, you can logout and create another account.

<img width="1418" height="445" alt="image" src="https://github.com/user-attachments/assets/93e6245c-e819-4046-a172-003dc2e9afef" />

Now we can apply the first vulnerability in the app. Delete the first post you made with the first account.

<img width="1418" height="445" alt="image" src="https://github.com/user-attachments/assets/9643fd36-6a67-4eb1-bace-d24831c6e677" />'

We have now completed the first exploit A01:2025 - BROKEN ACCESS CONTROL.
Next lets type gibberish into the search bar and force a 404 error.

<img width="1459" height="487" alt="image" src="https://github.com/user-attachments/assets/930cb4ae-d1f4-4096-bfd5-4e95d7ab0f3f" />

We should see that the debug panel has not been turned off A02:2025 - SECURITY MISCONFIGURATION.
The exposed debug panel makes exploiting the site easier for an attacker, as they might be able to see vulnerabilities easily.
Fixing this doesn't inherently increase security, but adds security by obscurity which is not perfect.
It still is better to keep the debug page hidden.
Now lets return to the home page.
Open your code editor and open the bruteforce.py file. 
Enter the name of the first account you made.
open a new terminal and setup the venv environment and run bruteforce py.

<img width="946" height="86" alt="image" src="https://github.com/user-attachments/assets/9f4b40e2-7442-4026-b02e-3611e967bb95" />

You should be able to see the guessed password.
This is the A09:2025 Security Logging & Alerting Failures vulnerability. The app doesn't log or prevent failed attempts in any way.
This bruteforce didn't use a large list but you could for example enumarate huge amounts of passwords without problem.
In the search bar type this: 
### ' UNION SELECT id, username, password, null, null FROM app_unsafeuser -- 
<img width="1850" height="972" alt="image" src="https://github.com/user-attachments/assets/2ddefc7e-b3e1-4eb8-aebc-824d313c2f71" />

We should get all accounts and their plaintext passwords as search results.
This fulfills two vulnerabilities. # A05:2025 - INJECTION and # A07:2025 - AUTHENTICATION FAILURES.
We were able to inject our sql command into the search bar and expose non hashed plaintext passwords from the database. 
We also could drop tables, edit information and do many other malicious actions with this injection vulnerability.

<img width="877" height="518" alt="image" src="https://github.com/user-attachments/assets/b47aeaf6-5a1a-46a8-ac60-4af4ab51d9c8" />


Now you can apply the fixes that appear commented in the code and attempt these vulnerabilities again.
Changes to apply exist in the following files.

views.py

urls.py (both of them)

settings.py

models.py

forms.py

backends.py

admin.py

post_detail.html

After applying changes remember to.

python manage.py makemigrations

python manage.py migrate


