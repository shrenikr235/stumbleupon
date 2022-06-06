from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]


class RoomForm(ModelForm):
    class Meta:
        model = Room # model that we want to create a form for
        fields = "__all__" 

        # create fields based on the fields (host, topic, name, desc etc) in the Room model.
        # later on, fields = ["name", "body"] or only the required fields
        exclude = ["host", "participants"]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["avatar","name", "username", "email", "bio"]