# from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

from projects import service
from projects.serializers import ProjectSerializer
from projects.models import Project
from users.models import Contributor


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Project.objects.all()

    def list(self, request):
        user = self.request.user
        projects = [contributor.project for contributor in Contributor.objects.filter(user=user)]
        projects = sorted(projects, key=lambda order_by: order_by.id)
        return Response(self.serializer_class(projects, many=True).data, status=status.HTTP_200_OK)

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

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            user = request.user
            project = self.get_object()

            user_role = Contributor.objects.filter(user=user, project=project).get().role
            is_user_authorized = service.can_user_access_project(project, user, role=user_role)
            if is_user_authorized:
                return Response(self.serializer_class(project).data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            user = request.user
            project: Project = self.get_object()

            user_role = Contributor.objects.filter(user=user, project=project).get().role
            is_user_authorized = service.can_user_edit_project(project, user, role=user_role)
            if not is_user_authorized:
                return Response({'message': 'You must be the author to update.'}, status=status.HTTP_403_FORBIDDEN)

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

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            user = request.user
            project: Project = self.get_object()

            user_role = Contributor.objects.filter(user=user, project=project).get().role
            is_user_authorized = service.can_user_edit_project(project, user, role=user_role)

            if not is_user_authorized:
                return Response({'message': 'You must be the author to delete.'}, status=status.HTTP_403_FORBIDDEN)

            return super(ProjectViewSet, self).destroy(request, pk, *args, **kwargs)

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project'}, status=status.HTTP_403_FORBIDDEN)
