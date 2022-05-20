from urllib.request import Request
from django.shortcuts import render
# from django.http import HttpResponse

rooms = [
    {"id":1, "name":"Learn JavaScript"},
    {"id":2, "name":"German A1 classes for beginners"},
    {"id":3, "name":"Design with Figma masterclass"},
]


def home(request):
    # return HttpResponse("Home Page") # without templates
    # return render(request, "home.html")
    context = {"rooms": rooms}
    return render(request, "base/home.html", context) 
    # the first "rooms" refers to how we wanna access the second rooms dictionary in the template
    # so now we have access to the rooms dictionary in the template home.html

def room(request, pk):
    room = None
    for i in rooms:
        if i["id"] == int(pk):
            room = i
    context = {"room": room}

    return render(request, "base/room.html", context)
