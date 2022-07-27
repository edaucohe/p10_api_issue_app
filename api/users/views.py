# from django.shortcuts import render
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# from users.models import User
# from users.serializers import UserSerializer, SignUpSerializer


# Create your views here.
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_user_model().objects.all()


# class SignUpViewSet(CreateAPIView):
#     serializer_class = SignUpSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         return get_user_model().objects.all()

