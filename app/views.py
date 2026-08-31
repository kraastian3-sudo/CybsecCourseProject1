from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate # FIX: Comment authenticate out
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# FIX: Comment these out
from .models import UnsafePost
from .forms import UnsafeRegisterForm, UnsafeLoginForm, UnsafePostForm, UnsafeCommentForm
# FIX: Uncomment the next two lines
# from .models import Post
# from .forms import RegisterForm, PostForm, CommentForm

# A07:2025 - AUTHENTICATION FAILURES
# The application uses Unsafeuser, which stores passwords in plaintext.
# The password is compared against the plaintext password in the database.
# There is no password hashing or secure password verification.
# FIX:
# Djangos normal User and authentication system hash and verify passwords.


def register(request):
    if request.method == "POST":
        form = UnsafeRegisterForm(request.POST) # Comment this out
# FIX:
        # form = RegisterForm(request.POST)

        # if form.is_valid():
        user = form.save() # Comment this out
# FIX: 
            # user = form.save()
            # login(request, user)
            # return redirect("post_list")

            # The vulnerable backends.py is used here
            # Comment the rest of the visible code from this function
        authenticated_user = authenticate(request, username=user.username, password=user.password) # Comment this out

        if authenticated_user is not None: # Comment this out
            login(request, authenticated_user, backend="app.backends.UnsafeAuthBackend") # Comment this out
            return redirect("post_list") # Comment this out

    else:
        form = UnsafeRegisterForm() # Comment this out
# FIX:
    # else:
    #     form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

# A07: The login uses plaintext passwords through UnsafeAuthBackend.
# A09: Failed login attempts are deliberately NOT logged.
# FIX: Use Django's normal authentication system and appropriate security logging/monitoring for failed authentication events.

# FIX: Comment this whole function out along with unsafe logout. A ready made login() exists within django.
def unsafe_login(request):
    if request.method == "POST":
        form = UnsafeLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user, backend="app.backends.UnsafeAuthBackend")
                return redirect("post_list")
            
            # The failed login attempt is not logged.

            form.add_error(None, "Invalid username or password.")

    else:
        form = UnsafeLoginForm()

    return render(request, "registration/login.html", {"form": form})

def unsafe_logout(request):
    from django.contrib.auth import logout

    logout(request)
    return redirect("post_list")

def post_list(request):
# Comment from here until FIX
    posts = UnsafePost.objects.all().order_by("-created_time")

    return render(request, "blog/post_list.html", {"posts": posts})

# FIX:
#    posts = Post.objects.all().order_by("-created_time")
#    return render(request, "blog/post_list.html", {"posts": posts})

# FIX: Comment the lines on top of the commented lines and uncomment the comments in this function
def post_detail(request, pk):
    post = get_object_or_404(UnsafePost, pk=pk)
    # post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect("login")
        
        form  = UnsafeCommentForm(request.POST)
        # form = CommentForm(request.POST)  
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect("post_detail", pk=post.pk)

    else:
        form = UnsafeCommentForm()
        # form = CommentForm()

    return render(request, "blog/post_detail.html", {"post": post, "form": form})

# FIX: Change UnsafePostForm to postForm 
@login_required
def create_post(request):
    if request.method == "POST":
        form = UnsafePostForm(request.POST)
        # form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
       form = UnsafePostForm()
        # form = PostForm()

    return render(request, "blog/post_form.html", {"form": form})


# A01:2025 - BROKEN ACCESS CONTROL
# There is no authorization check verifying that the currently authenticated user owns the post.
# FIX: Verify that post.author == request.user before allowing the deletion.

@login_required
def delete_post(request, pk):
    post = get_object_or_404(
        UnsafePost, # FIX: Change this to Post
        pk=pk
    )


    # FIX:
    # Here the author is verified. Enable the code below.
    # if post.author != request.user:
    #     messages.error(request, "You are not the owner of this post.")
    #     return redirect("post_list")

    # No authorization check before this block.
    if request.method == "POST":
        post.delete()
        return redirect("post_list")

    return render(request, "blog/delete_post.html", {"post": post})

# A05:2025 - INJECTION
# User input is directly put into an SQL query.
# FIX:
# Djangos ORM safely handles the user's input instead of treating it as part of the SQL syntax.

def search(request):
    query = request.GET.get("q", "")

    # The user's input is directly inserted into the SQL query.
    sql = (f"SELECT * FROM {UnsafePost._meta.db_table}\nWHERE title LIKE '%{query}%'")

    # Raw SQL is intentionally used here so that the vulnerable
    # Here is a query that will dump all users and passwords:
    # ' UNION SELECT id, username, password, null, null FROM app_unsafeuser -- 
    posts = UnsafePost.objects.raw(sql)

    # Instead of the Two previous lines this code queries safely.
    # posts = Post.objects.filter(title__icontains=query) 
    # Remember to enable the safe models first to me this work

    return render(request, "blog/search.html", {"posts": posts, "query": query})