from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []



class Room(models.Model):
    host  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey("Topic", on_delete=models.SET_NULL, null=True) # Topic as a string since it's written below the Room class
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # field can be blank
    participants = models.ManyToManyField(User, related_name = "participants", blank = True)
    updated = models.DateTimeField(auto_now=True) # take timestamp every time save is hit on the item
    created = models.DateTimeField(auto_now_add=True) # take timestamp when save is hit the first time i.e during creation

 
    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name

        

class Topic(models.Model):
    # topic can have multiple rooms
    # one room can have only one topic
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        message_preview = self.body[0:50]
        return message_preview

    

