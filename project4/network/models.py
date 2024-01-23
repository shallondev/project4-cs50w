from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

class Posting(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")  
    content = models.CharField(max_length=64, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Post {self.id} made by {self.user}"
        