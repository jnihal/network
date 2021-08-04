
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API Routes
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
