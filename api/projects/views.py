# from django.shortcuts import render
from typing import Optional

from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.models import Project

from projects.serializers import ProjectSerializer
from users.models import Contributor
from projects import service


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        # Afficher la liste des projets rattachés à l'utilisateur
        queryset = Project.objects.filter(author_user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        data = {
            "title": request.POST.get('title', None),
            "description": request.POST.get('description', None),
            "type": request.POST.get('type', None),
            "author_user": user.pk,
            }
        serializer = self.serializer_class(data=data, context={'author': user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = request.user
        project = self.get_object()

        is_user_authorized = service.can_user_access_project(project, user)
        if is_user_authorized:
            response = Response(self.serializer_class(project).data, status=status.HTTP_200_OK)
        else:
            response = Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)
        return response

    def update(self, request, pk=None, *args, **kwargs):
        user = request.user
        project: Project = self.get_object()
        is_user_authorized = can_user_access_project(project, user, role=Contributor.Role.Author)

        if not is_user_authorized:
            return Response({'message': 'You must be the author to update'}, status=status.HTTP_403_FORBIDDEN)

        data = {
            "title": request.POST.get('title', None),
            "description": request.POST.get('description', None),
            "type": request.POST.get('type', None),
            }
        serializer = self.serializer_class(
            instance=project,
            data=data,
            context={'author': user},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        # you custom logic #
        return super(ProjectViewSet, self).destroy(request, pk, *args, **kwargs)
