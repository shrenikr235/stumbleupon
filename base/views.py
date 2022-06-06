from pydoc import describe
from urllib.request import Request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# restricting pages
from django.contrib.auth.decorators import login_required

# user registration

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
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, email=email, password=password)

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
    form = MyUserCreationForm()

    # process form request
    if request.method == "POST":
        form = MyUserCreationForm(request.POST) # credentials entered
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

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()

    # recent activity feature
    # room_messages = Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q)) # filter by room name



    context = {"rooms": rooms, "topics": topics, "room_count": room_count, "room_messages": room_messages}
    return render(request, "base/home.html", context) 

def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i

    room = Room.objects.get(id=pk)
    # chatroom messages CRUD
    room_messages = room.message_set.all() # query child objects of speific room

    participants = room.participants.all()


    if request.method  == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user) # add user to manytomany field
        return redirect("room", pk = room.id)

    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms": rooms, "room_messages": room_messages, "topics": topics}
    return render(request, "base/profile.html", context)



@login_required(login_url="login") # restrict to logged in users only
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST": # post data
        topic_name = request.POST.get("topic")
        # created is a boolean value
        topic, created = Topic.objects.get_or_create(name = topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get("name"),
            description = request.POST.get("description"),
        )
        return redirect("home") # redirect to homepage


    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)

@login_required(login_url="login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You don't have sufficient permissions to view this.")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        # created is a boolean value
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("home")

    context = {"form" : form, "topics": topics, "room": room}
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

@login_required(login_url="login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You don't have sufficient permissions to view this.")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="login")
def update_user(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk = user.id)


    return render(request, "base/update-user.html", {"form": form})


def topics_page(request):
    q = request.GET.get("q") if request.GET.get("q") != None else "" 
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "base/topics.html", {"topics": topics})

def activity_page(request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", {"room_messages": room_messages})