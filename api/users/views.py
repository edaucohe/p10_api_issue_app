# from django.shortcuts import render
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

# from users.models import User
# from users.serializers import UserSerializer, SignUpSerializer


# Create your views here.
from users.serializers import UserSerializer, SignUpSerializer


class UserViewSet(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    # @route('/me')
    def get(self, request):
        return request.user


class SignupView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self):
        return Response(data={'result': 'ok'}, content_type='application/json')
#
#
# class AccountView(APIView):
#     serializer_class = SignUpSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self):
#         # signu
#         print('get in queryset')
#         return get_user_model().objects.all()
#
#     @action(methods=['POST'], detail=False, permission_classes=[AllowAny], url_name='login')
#     def login(self, truc):
#         print(f'coucou {truc}')
#         return Response(data={'result': 'ok'}, content_type='application/json')
#
#
#
# # POST /signup
# # POST /login
# # /users
