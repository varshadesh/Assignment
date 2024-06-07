from django.contrib import admin
from .models import user,FriendRequest
# Register your models here.

admin.site.register(user)
admin.site.register(FriendRequest)