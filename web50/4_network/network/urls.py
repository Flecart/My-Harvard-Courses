
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("api/get_posts", views.get_posts, name="postapi"),
    path("api/like", views.like, name="likeapi")
]
