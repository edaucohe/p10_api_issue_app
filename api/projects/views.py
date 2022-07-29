from django.shortcuts import render
from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.models import Project

from projects.serializers import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post']

    def get_queryset(self):
        # Afficher la liste des projets rattachés à l'utilisateur
        queryset = Project.objects.filter(author_user=self.request.user)
        return queryset

    # def create(self, request, *args, **kwargs):
    #     user = request.user
    #     data = {
    #         "title": request.POST.get('title', None),
    #         }
    #     serializer = self.serializer_class(data=data, context={'author': user})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     serializer.save(author_user=self.request.user)

    # def retrieve(self, request, pk=None):
    #     instance = self.get_object()
    #     # query = request.GET.get('query', None)  # read extra data
    #     return Response(self.serializer_class(instance).data, status=status.HTTP_200_OK)
