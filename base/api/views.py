from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.api import serializers
from base.models import Room
from .serializers import RoomSerializer

@api_view(["GET"])
def get_routes(request):
    routes = [
        "GET /api",
        "GET /api/rooms",
        "GET /api/rooms/:id"

    ]

    return Response(routes)

@api_view(["GET"])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) # multiple objects to serialize? Yes.
    return Response(serializer.data) # response cannot return python objects

@api_view(["GET"])
def get_room(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data) # response cannot return python objects
