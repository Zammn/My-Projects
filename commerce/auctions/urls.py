from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.newListing, name="new"),
    path("chooseCategory", views.chooseCategory, name="chooseCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("add/<int:id>", views.add, name="add"),
    path("watchlistPage", views.watchlistPage, name="watchlistPage"),
    path("comments<int:id>", views.comments, name="comments"),
    path("newBid<int:id>", views.newBid, name="newBid"),
    path("endAuction/<int:id>", views.endAuction, name="endAuction")

]
