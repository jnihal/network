from django.contrib import admin
from .models import User, Profile, Post, Follower, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Like)