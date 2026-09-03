Django blog vulnerabilities.

https://github.com/kraastian3-sudo/CybsecCourseProject1


Installation

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

Apply all of the fixes at once before restarting the application. Some fixes remove models and add new ones. After applying all of the changes that are explained below and pointed out with comments in the code remember to make migrate the database before starting the app for it to work. Fixes to apply exist in the following files and exist as comments within them. Read my essay below before applying them.

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


Testing the vulnerabilities:

First when you open the site you should see a homepage. Click register and create an account with a simple username like 1234. Afterwards you should be logged in. Now you can create your first post. After creating your first post, you can logout and create another account.

Flaw 01 (Cross Site Request forgery, csrf):

On one page log in to any user. Open another terminal and navigate to the project directory. Open a local web server on another port “python3 -m http.server 9000”. Open the csrf attack page in your browser “http://127.0.0.1:9000/csfr_demo.html”. Now from the demo page press the “create post using csrf” button. You should see the post in the blog website now. 

To fix it we need to enable csrf protection and add a csrf token in the post form.

https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/cb52340e6e21db94bd3d946dff2f0308a660944b/app/views.py#L15
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/views.py#L123
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/templates/blog/post_form.html#L17


Flaw 02 (A01:2021 – Broken Access Control):

Log in to a user and create a post. Afterwards log into another user and delete the post. The deletion goes through as the deletion function only checks that the user is logged in, but does not check if the user is the owner of the post. This problem is easily fixed comparing the logged in user with the owner of the post. If they don’t match we can raise an error and stop the function, redirecting the user back without any changes.

https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/ca91d04390bee8e6a4cd22e15d6609297019d4b4/app/views.py#L158


Flaw 03 (A05:2021 – Security Misconfiguration ):
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/44c395ea02f42f0a3207aefcb9f4b4cf15235a59/myproject/settings.py#L31

Next lets type gibberish into the search bar and force a 404 error. We should see that the debug panel has not been turned off. The exposed debug panel makes exploiting the site easier for an attacker, as they might be able to see vulnerabilities easily. Fixing this doesn't inherently increase security, but adds security by obscurity which is not perfect. It still is better to keep the debug page hidden. To fix this change we only need to apply DEBUG = False in the settings.py file.

Flaw 04 (A09:2021 – Security Logging and Monitoring Failures):
 

Now lets return to the home page. Open your code editor and open the bruteforce.py file in a code editor. This is a password cracker that enumerates through a preset list of password. I kept the list brief for simplicity, but there are lots of repos with thousands of easy to guess passwords. Enter the name of the first account you made into the file. Open a new terminal and setup the venv environment and run bruteforce py. This should crack easy to guess passwords like 1234 and 0000. The fix is to use a library like axes to implement logging of password attempts. Enable axes in the settings.py file.

https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/ca91d04390bee8e6a4cd22e15d6609297019d4b4/myproject/settings.py#L38
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/b9219e65ce25eff0ffe10b652b6304c9ad40a666/myproject/settings.py#L54
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/b9219e65ce25eff0ffe10b652b6304c9ad40a666/myproject/settings.py#L56
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/ca91d04390bee8e6a4cd22e15d6609297019d4b4/myproject/settings.py#L77

Flaw 05 (A03:2021 – Injection ):
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/b9219e65ce25eff0ffe10b652b6304c9ad40a666/app/views.py#L175

If we navigate to the main page of the website and use this 

' UNION SELECT id, username, password, null, null FROM app_unsafeuser – 

as  a query, we will see a search page with all of the usernames and passwords visible. This means that sql queries are not sanitized and the database is able to be modified freely by an attacker by injecting malicous sql. The attacker is free to even drop tables. The fix is to treat the query safely

posts = Post.objects.filter(title__icontains=query) 

with the filter function. This way querying other tables or modifying them is not possible and the user is limited to only searching posts.

Flaw 06 (A07:2021 – Identification and Authentication Failures 
):

https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/b9219e65ce25eff0ffe10b652b6304c9ad40a666/app/views.py#L13

This flaw is apparent as a combination of all previous flaws. As we set the password at the start the app permits the use of simple passwords like 1234. Also bruteforce scripts can be used to crack passwords easily, as repeated attempts are not blocked. Moreover passwords were stored as plaintext information as it is apparent through our injection attack. The fixes for this problem are to use Djangos own user model that hashes passwords securely. The axes library can be configured freeze the login in repeated attempts fail.

This fix is implemented by disabling the custom user backend. Disabling all all unsafe models and forms. The difference between the safe and unsafe models and forms is the fact that the safe ones are configured to use the django user model. In views we can disable the login and logout functions as the django library includes these already. This also means that we have to remove them from the urls.py file. As for the axes library, we can apply the passwords limit by enabling them in the settings.

https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/views.py#L17
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/b9219e65ce25eff0ffe10b652b6304c9ad40a666/myproject/settings.py#L38
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/myproject/settings.py#L45
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/models.py#L3
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/models.py#L69
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/forms.py#L1
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/forms.py#L34
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/backends.py#L1
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/admin.py#L1
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/templates/blog/post_detail.html#L21
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/urls.py#L9
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/app/urls.py#L10
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/myproject/urls.py#L20
https://github.com/kraastian3-sudo/CybsecCourseProject1/blob/76aac1739e3e7efc43ba57663683fd50e826525c/myproject/urls.py#L26


