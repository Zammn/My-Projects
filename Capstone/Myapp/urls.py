from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("todo", views.todo, name="todo"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("recipe", views.recipe, name="recipe"),
    path("create", views.create, name="create"),
    path("get_random", views.get_random, name="get_random"),
]