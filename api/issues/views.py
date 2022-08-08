from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from issues.serializers import IssueSerializer
from issues.models import Issue
from users.models import User, Contributor

from projects import service
from projects.models import Project


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = Issue.objects.all()
        return queryset

    def list(self, request, project_pk=None, *args, **kwargs):
        try:
            user = self.request.user
            project = Project.objects.filter(pk=project_pk).get()

            user_role = Contributor.objects.filter(user=user, project=project_pk).get().role
            is_user_authorized = service.can_user_access_project(project, user, role=user_role)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            issues = list(Issue.objects.filter(project=project_pk).order_by('id'))
            return Response(self.serializer_class(issues, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project or projects does not exist'},
                            status=status.HTTP_403_FORBIDDEN)

    def create(self, request, project_pk=None, *args, **kwargs):
        user = request.user
        assignee_user_pk = user.pk

        assignee_user_name = request.POST.get('assignee_user', None)
        contributors = list(Contributor.objects.filter(project=project_pk))
        for assignee_user in contributors:
            if assignee_user_name == assignee_user.user.username:
                assignee_user_pk = assignee_user.user_id

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

    def retrieve(self, request, project_pk=None, *args, **kwargs):
        try:
            user = request.user
            issue = self.get_object()
            project_of_issue = issue.project
            current_project = Project.objects.filter(pk=project_pk).get()

            user_role = Contributor.objects.filter(user=user, project=project_of_issue).get().role
            is_user_authorized = service.can_user_access_project(current_project, user, role=user_role)
            if is_user_authorized:
                return Response(self.serializer_class(issue).data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project of this issue'},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, project_pk=None, *args, **kwargs):
        try:
            user = request.user
            issue = self.get_object()
            project_of_issue = issue.project
            current_project = Project.objects.filter(pk=project_pk).get()

            user_role = Contributor.objects.filter(user=user, project=project_of_issue).get().role
            is_user_authorized = service.can_user_access_project(current_project, user, role=user_role)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            is_user_authorized_to_edit_issue = service.can_user_edit_issue(issue=issue, user=user)
            if not is_user_authorized_to_edit_issue:
                return Response({'message': 'You must be the author to update this issue.'},
                                status=status.HTTP_403_FORBIDDEN)

            assignee_user_username = request.POST.get('assignee_user', None)
            assignee_user = User.objects.filter(username=assignee_user_username).get()

            data = {
                "title": request.POST.get('title', None),
                "description": request.POST.get('description', None),
                "tag": request.POST.get('tag', None),
                "priority": request.POST.get('priority', None),
                "status": request.POST.get('status', None),
                "project": project_of_issue.pk,
                "assignee_user": assignee_user.pk,
                }
            serializer = self.serializer_class(
                instance=issue,
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
