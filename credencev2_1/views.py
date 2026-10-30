from rest_framework.viewsets import generics
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# List and Create new Users
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # List and Create new Users
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_joined": user.date_joined,
        "time_joined": user.date_joined.time(),                # HH:MM:SS object
        "time_joined_formatted": user.date_joined.strftime("%I:%M %p"), # "10:03 AM"
    })