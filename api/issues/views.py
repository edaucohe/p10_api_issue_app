from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from issues.serializers import IssueSerializer

from issues.models import Issue
from users.models import User


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        # Display issues list of a project
        queryset = Issue.objects.filter(author_user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user

        assignee_user_name = request.POST.get('assignee_user', None)
        assignee_user_pk = user.pk
        # TODO To replace 'User.objects.all()' for contributors of the same project
        users = User.objects.all()
        for assignee_user in users:
            if assignee_user_name == assignee_user.username:
                assignee_user_pk = assignee_user.pk

        data = {
            "title": request.POST.get('title', None),
            "description": request.POST.get('description', None),
            "tag": request.POST.get('tag', None),
            "priority": request.POST.get('priority', None),
            "status": request.POST.get('status', None),
            "project": request.POST.get('project', None),
            "author_user": user.pk,
            "assignee_user": assignee_user_pk
            }

        serializer = self.serializer_class(data=data, context={'author': user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
