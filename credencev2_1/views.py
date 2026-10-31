from rest_framework.viewsets import generics
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# List and Create new Users
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAccountListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserAccount.objects.select_related('user').all()
    serializer_class = UserAccountSerializer

class UserAccountListDetailAPIView(generics.RetrieveAPIView):
    queryset = UserAccount.objects.select_related('user').all()
    serializer_class = UserAccountSerializer
    lookup_field='pk'

class UserAccountListDetailEdit(generics.UpdateAPIView):
    queryset = UserAccount.objects.select_related('user').all()
    serializer_class = UserAccountSerializer
    lookup_field='pk'

class ProfileView(generics.RetrieveAPIView):
    queryset = UserAccount.objects.select_related(
        'user',
        'address'
    ).all()
    serializer_class = ProfileDetailsSerializer
    lookup_field='pk'

class ProfileUpdate(generics.RetrieveAPIView):
    queryset = UserAccount.objects.select_related('user', 'address').all()
    serializer_class = ProfileDetailUpdateSerializer
    lookup_field='pk'

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