from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comments, Bids


def index(request):
    activeLists = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeLists,
        "categories": categories
    })

def newListing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/new.html", {
            "categories": categories 
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        
        activeUser = request.user
        
        categoryInfo = Category.objects.get(categoryName=category)
        bid = Bids(bid=int(price), user=activeUser)
        bid.save()
        
        newListing = Listing(
            title=title,
            description=description,
            imageUrl=imageurl,
            price=bid,
            category=categoryInfo,
            owner=activeUser
        )
        
        newListing.save()
        return HttpResponseRedirect(reverse(index))
    
def chooseCategory(request):
    if request.method == "POST":
        userCategory = request.POST["category"]
        category = Category.objects.get(categoryName=userCategory)
        activeLists = Listing.objects.filter(isActive=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeLists,
            "categories": categories
        })
        
def listing(request, id):
    listingInfo = Listing.objects.get(pk=id)
    watchlist = request.user in listingInfo.watchlist.all()
    everyComment = Comments.objects.filter(listing=listingInfo)
    ifOwner = request.user.username == listingInfo.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingInfo,
        "watchlist": watchlist,
        "everyComment": everyComment,
        "ifOwner": ifOwner
    })            

def add(request, id):
    listingInfo = Listing.objects.get(pk=id)
    activeUser = request.user 
    listingInfo.watchlist.add(activeUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def remove(request, id):
    listingInfo = Listing.objects.get(pk=id)
    activeUser = request.user   
    listingInfo.watchlist.remove(activeUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlistPage(request):
    activeUser = request.user
    listings = activeUser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
    
def comments(request, id):
    activeUser = request.user
    listingInfo = Listing.objects.get(pk=id)
    comment = request.POST['new']
    
    new = Comments (
        commentator=activeUser,
        listing=listingInfo,
        comment=comment
    )
    
    new.save()
    
    return HttpResponseRedirect(reverse(listing,args=(id, )))

def newBid(request, id):
    newBid = request.POST["newBid"]
    listingInfo = Listing.objects.get(pk=id)
    
    if int(newBid) > listingInfo.price.bid:
        updatedBid = Bids(user=request.user, bid=int(newBid))
        updatedBid.save()
        listingInfo.price = updatedBid
        listingInfo.save()
        ifOwner = request.user.username == listingInfo.owner.username

        return render(request, "auctions/listing.html", {
            "listing": listingInfo,
            "message": "Bid updated successfully",
            "update": True,
            "ifOwner": ifOwner
        })
    else:
            return render(request, "auctions/listing.html", {
            "listing": listingInfo,
            "message": "Bid failed",
            "update": False
        }) 
            
def endAuction(request, id):
    listingInfo = Listing.objects.get(pk=id)
    listingInfo.isActive = False
    listingInfo.save()
    watchlist = request.user in listingInfo.watchlist.all()
    everyComment = Comments.objects.filter(listing=listingInfo)
    ifOwner = request.user.username == listingInfo.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingInfo,
        "watchlist": watchlist,
        "everyComment": everyComment,
        "ifOwner": ifOwner,
        "update": True,
        "message": "Your auction is closed."
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
