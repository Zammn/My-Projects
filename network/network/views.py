from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import logging
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from .models import Post
from .models import FollowingAndFollower
from .models import Like
import json
from django.views.decorators.csrf import csrf_exempt



def index(request):
    allPosts = Post.objects.all().order_by('id').reverse()
    
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)
    
    allLikes = Like.objects.all()
    userLiked = []
    
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                userLiked.append(like.post.id)
    except:
        userLiked = []
                    
    
    return render(request, "network/index.html", {
        "allPosts": allPosts,
        "page_posts": page_posts,
        "userLiked": userLiked
    })


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allPosts = Post.objects.filter(owner=user).order_by('id').reverse()
    
    following = FollowingAndFollower.objects.filter(user=user)
    followers = FollowingAndFollower.objects.filter(user_follower=user)     
   
    try:
        checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False
        
        
                
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)
    
    
    return render(request, "network/profile.html", {
        "profileUser": user.username,
        "allPosts": allPosts,
        "page_posts": page_posts,
        "following": following,
        "followers": followers,
        "correct_profile": user,
        "isFollowing": isFollowing
    })

def follow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    
    f = FollowingAndFollower(user=currentUser, user_follower=userfollowData)
    f.save()
    
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))
    
    
def unfollow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    
    f = FollowingAndFollower.objects.get(user=currentUser, user_follower=userfollowData)
    f.delete()
    
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


def following(request):
    userNow = User.objects.get(pk=request.user.id)
    currentlyFollowing = FollowingAndFollower.objects.filter(user=userNow)
    allPosts = Post.objects.all().order_by('id').reverse()

    showingPosts = []
    
    for post in allPosts:
        for p in currentlyFollowing:
            if p.user_follower == post.owner:
                showingPosts.append(post)
    
    allPosts = Post.objects.all().order_by('id').reverse()
    
    paginator = Paginator(showingPosts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)
    
    
    return render(request, "network/following.html", {
        "page_posts": page_posts
    })


def addPost(request):
    if request.method == "POST":
        posts = request.POST['posts']
        post = Post(posts=posts, owner=request.user)
        post.save()
        
        logging.info(f"User (request.user) added new post.")
        return HttpResponseRedirect(reverse(index))


def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    post.content = content
    post.save()
    return JsonResponse({'content': post.posts})


def liked(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like(user=user, post=post)
    like.save()
    return JsonResponse({"message: Post liked"}, safe=False)
    
def unliked(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"message: Post unliked"}, safe=False)


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
