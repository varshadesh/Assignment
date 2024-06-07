import uuid
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager,GroupManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission

# Create your models here.
class user(AbstractBaseUser):
    name=models.CharField(verbose_name="full_name",max_length=2250)
    email =models.EmailField(verbose_name="email ",max_length=22250,unique=True)
    password = models.CharField(max_length=250, blank=True,  default='null', null=True)
  #  email=EmailField(unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email



class FriendRequest(models.Model):
    sender = models.ForeignKey(user, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(user, related_name='received_friend_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sender', 'receiver')