from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator, Page


from .models import User, Posting


@login_required
def edit(request, posting):

    posting_local = Posting.objects.get(id=posting)

    posting_content = posting_local.content

    if request.method == "POST" and posting_local.user == request.user:

        new_content = request.POST["content"]

        # Update the content and save to the database
        posting_local.content = new_content
        posting_local.save()

        return HttpResponseRedirect(reverse("index"))

    postings = Posting.objects.all().order_by('-timestamp')

    return render(request, "network/index.html", {
        'postings':postings,
        'posting_content':posting_content,
        'h2_label':"All",
        'h3_label':"Edit",
        'btn_value':"Edit",
    })



@login_required
def following_view(request, username):
    local_user = User.objects.get(username=username)
    following_users = local_user.following.all()
    
    # Get postings for following users
    postings = Posting.objects.filter(user__in=following_users).order_by('-timestamp')
    
    # Paginate the postings
    paginator = Paginator(postings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'h2_label': "Following",
        'h3_label': "New",
        'btn_value': "Post",
    })



def profile_view(request, username):

    user = User.objects.get(username=username)

    user_postings = Posting.objects.filter(user=user).order_by('-timestamp')

    # Get followers and following 
    followers = user.followers.all()
    following = user.following.all()

    if request.method == "POST" and request.user.is_authenticated:

        # Add or remove user based on if they are following or not.
        if request.user in followers:
            request.user.following.remove(user)
        else:
            request.user.following.add(user)

        return HttpResponseRedirect(reverse("profile_view", args=[username]))

    return render(request, "network/profile_view.html", {
        'profile_user': user,
        'postings': user_postings,
        'followers' : followers,
        'followerscount': followers.count(),
        'following': following.count(),
    })


def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        # Get content from form
        content = request.POST["content"]

        if content is not None:
            user = request.user
            Posting.objects.create(
                user=user,
                content=content,
            )

    # Get all postings
    postings = Posting.objects.all().order_by('-timestamp')

    # Paginate the postings
    paginator = Paginator(postings, 10)  # Show 10 postings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'h2_label': "All",
        'h3_label': "New",
        'btn_value': "Post",
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
