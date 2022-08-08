# from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.serializers import UserSerializer, SignUpSerializer, ContributorSerializer
from users.models import User, Contributor

from projects import service
from projects.models import Project


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


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Contributor.objects.all()

    def list(self, request, project_pk=None, *args, **kwargs):
        try:
            user = self.request.user
            project = Project.objects.filter(pk=project_pk).get()

            user_role = Contributor.objects.filter(user=user, project=project_pk).get().role
            is_user_authorized = service.can_user_access_project(project, user, role=user_role)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            contributor = list(Contributor.objects.filter(project=project_pk).order_by('id'))
            return Response(self.serializer_class(contributor, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project or projects does not exist'},
                            status=status.HTTP_403_FORBIDDEN)
