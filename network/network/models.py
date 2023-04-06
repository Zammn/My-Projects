from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    posts = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Post {self.id} posted by {self.owner} on {self.date.strftime('%d %b %Y at %H:%M')}"
     
class FollowingAndFollower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    
    def __str__(self):
        return f'{self.user} follows {self.user_follower}'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked")
    
    def __str__(self):
        return f'{self.user} liked {self.post}'