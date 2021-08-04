from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.creator} posted on {self.timestamp}"

    def liked_users(self):
        return [x[0] for x in self.likes.values_list("user_id")]


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user} likes ({self.post})"