# from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
