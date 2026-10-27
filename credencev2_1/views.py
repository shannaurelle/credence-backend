from rest_framework.viewsets import generics
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
# Create your views here.

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