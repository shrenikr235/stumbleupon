from urllib.request import Request
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# rooms = [
#     {"id":1, "name":"Learn JavaScript"},
#     {"id":2, "name":"German A1 classes for beginners"},
#     {"id":3, "name":"Design with Figma masterclass"},
# ]

"""

queryset = ModelName.objects.all()

"""

def home(request):
    # return HttpResponse("Home Page") # without templates
    # return render(request, "home.html")
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "base/home.html", context) 

def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i

    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)


def create_room(request):
    form = RoomForm()
    if request.method == "POST": # post data
        form = RoomForm(request.POST) # add data to the form 
        if form.is_valid(): # check if it is valid
            form.save() # save if true
            return redirect("home") # redirect to homepage


    context = {"form": form}
    return render(request, "base/room_form.html", context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form" : form}
    return render(request, "base/room_form.html", context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})