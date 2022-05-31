from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

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
        fields = ["username", "email"]