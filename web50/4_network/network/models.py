from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }


class Follow(models.Model):
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followed")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
