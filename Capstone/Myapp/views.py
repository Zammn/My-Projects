from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Recipe
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import random

# Create your views here.
def homepage(request):
    if request.method == "GET": 
        return render(request, "Myapp/homepage.html")
    else:
        return render(request, "Myapp/login.html")
        
@login_required
def todo(request):
    if request.method == "GET":
        return render(request, "Myapp/todo.html")
    else:
        return render(request, "Myapp/login.html")

        
def recipe(request):
    recipes = Recipe.objects.all()
    return render(request, "Myapp/recipe.html",{
      'recipes': recipes,
    })

def get_random(request):
    if request.method == "GET":
        items = Recipe.objects.order_by('title').values_list('title', flat=True).distinct()
        random_items = random.choice(list(items))
        return render(request, "Myapp/mealoftheday.html", {
            'random_items': random_items
        })
    else:
        return render(request, 'Myapp/recipe.html')
     
@login_required
def create(request):
    if request.method == "GET":
        recipes = Recipe.objects.all()
        return render(request, "Myapp/create.html", {
            "Recipes": recipes
        })
    else: 
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        directions = request.POST["directions"]
        ingredients = request.POST["ingredients"]
        
        activeUser = request.user
        
        newRecipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            directions=directions,
            imageUrl=imageurl,
            price=price,
            owner=activeUser
        )
        
        newRecipe.save()
        return HttpResponseRedirect(reverse(recipe))
    
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "Myapp/homepage.html")
        else:
            return render(request, "Myapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Myapp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Myapp/index.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Myapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Myapp/register.html")
    
    


