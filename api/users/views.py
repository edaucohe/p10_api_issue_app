# from django.shortcuts import render
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from users.models import User
# from users.serializers import UserSerializer, SignUpSerializer


# Create your views here.
from users.serializers import UserSerializer, SignUpSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']

    # @route('/me')
    @action(detail=True, methods=['get'])
    def get_users(self):
        # users = User.objects.all()
        queryset = User.objects.filter(active=True)
        username = self.request.GET.get('username')
        if username is not None:
            queryset = queryset.filter(username=username)
        # user = User.objects.filter(Q(user=user))
        # serializer = self.serializer_class(user, many=True)
        return queryset


class SignUpViewSet(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return get_user_model().objects.all()
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
