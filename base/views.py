from urllib.request import Request
from django.shortcuts import render
# from django.http import HttpResponse
from .models import Room

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
