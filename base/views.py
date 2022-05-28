from urllib.request import Request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# restricting pages
from django.contrib.auth.decorators import login_required

# user registration
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {"id":1, "name":"Learn JavaScript"},
#     {"id":2, "name":"German A1 classes for beginners"},
#     {"id":3, "name":"Design with Figma masterclass"},
# ]

"""

queryset = ModelName.objects.all()

"""

def login_page(request):

    page = "login"

    if request.user.is_authenticated:
        return redirect("home")


    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "Username or password does not exist")

    context = {"page": page}
    return render(request, "base/login_register.html", context)

def logout_user(request):
    logout(request)
    return redirect("home")

def register_page(request):
    # page = "register"
    form = UserCreationForm()

    # process form request
    if request.method == "POST":
        form = UserCreationForm(request.POST) # credentials entered
        if form.is_valid():
            # process user if form is valid
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        # if something screws up
        else:
            messages.error(request, "Error occured while registering")
    
    return render(request, "base/login_register.html", {"form": form})


def home(request):
    # return HttpResponse("Home Page") # without templates
    # return render(request, "home.html")
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "base/home.html", context) 

def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i

    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)

@login_required(login_url="login") # restrict to logged in users only
def create_room(request):
    form = RoomForm()
    if request.method == "POST": # post data
        form = RoomForm(request.POST) # add data to the form 
        if form.is_valid(): # check if it is valid
            form.save() # save if true
            return redirect("home") # redirect to homepage


    context = {"form": form}
    return render(request, "base/room_form.html", context)

@login_required(login_url="login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You don't have sufficient permissions to view this.")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form" : form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You don't have sufficient permissions to view this.")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})