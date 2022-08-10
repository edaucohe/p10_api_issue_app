from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from comments.serializers import CommentSerializer
from comments.models import Comment

from issues.models import Issue
from projects.models import Project
from users.models import Contributor

from projects import service


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset

    def list(self, request, project_pk=None, issues_pk=None, *args, **kwargs):
        try:
            user = self.request.user
            project = Project.objects.filter(pk=project_pk).get()
            issue = Issue.objects.filter(pk=issues_pk).get()
            issue_project = issue.project

            if not issue_project == project:
                return Response({'message': 'Issue does not correspond to the project'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            user_role = Contributor.objects.filter(user=user, project=project).get().role
            is_user_authorized = service.can_user_access_project(project, user, role=user_role)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            comments = list(Comment.objects.filter(issue=issues_pk).order_by('id'))
            return Response(self.serializer_class(comments, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project or issue does not exist'},
                            status=status.HTTP_403_FORBIDDEN)

    def create(self, request, project_pk=None, issues_pk=None, *args, **kwargs):
        try:
            user = request.user
            current_project = Project.objects.filter(pk=project_pk).get()
            issue = Issue.objects.filter(pk=issues_pk).get()
            issue_project = issue.project
            if not issue_project == current_project:
                return Response({'message': 'Issue does not correspond to the project'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            user_role = Contributor.objects.filter(user=user, project=project_pk).get().role
            is_user_authorized = service.can_user_access_project(current_project, user, role=user_role)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            issue_id = issue.pk
            data = {
                "description": request.POST.get('description', None),
                "author_user": user.pk,
                "issue": issue_id,
                }

            serializer = self.serializer_class(data=data, context={'author': user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'Project does not exist'}, status=status.HTTP_403_FORBIDDEN)
