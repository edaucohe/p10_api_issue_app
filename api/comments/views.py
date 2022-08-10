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

            # user_role = Contributor.objects.filter(user=user, project=project).get().role
            is_user_authorized = service.can_user_access_project(project, user)
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

            # user_role = Contributor.objects.filter(user=user, project=project_pk).get().role
            is_user_authorized = service.can_user_access_project(current_project, user)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            issue_id = issue.pk
            data = {
                "description": request.POST.get('description', None),
                "author_user": user.pk,
                "issue": issue_id
                }

            serializer = self.serializer_class(data=data, context={'author': user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'Project does not exist'}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, project_pk=None, issues_pk=None, *args, **kwargs):
        try:
            user = request.user
            comment = self.get_object()

            current_project = Project.objects.filter(pk=project_pk).get()
            issue = Issue.objects.filter(pk=issues_pk).get()
            project_of_issue = issue.project
            if not project_of_issue == current_project:
                return Response({'message': 'Issue does not correspond to the project'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            if not comment.issue == issue:
                return Response({'message': 'Comment does not correspond to the issue'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            current_project = Project.objects.filter(pk=project_pk).get()
            # user_role = Contributor.objects.filter(user=user, project=project_of_issue).get().role
            is_user_authorized = service.can_user_access_project(current_project, user)
            if is_user_authorized:
                return Response(self.serializer_class(comment).data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

        except ObjectDoesNotExist:
            return Response({'message': 'Project or issue may not exist'},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, project_pk=None, issues_pk=None, *args, **kwargs):
        try:
            user = request.user
            comment = self.get_object()

            current_project = Project.objects.filter(pk=project_pk).get()
            issue = Issue.objects.filter(pk=issues_pk).get()
            project_of_issue = issue.project
            if not project_of_issue == current_project:
                return Response({'message': 'Issue does not correspond to the project'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            if not comment.issue == issue:
                return Response({'message': 'Comment does not correspond to the issue'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            is_user_authorized_to_edit_issue = service.can_user_edit_comment(comment=comment, user=user)
            if not is_user_authorized_to_edit_issue:
                return Response({'message': 'You must be the author to update this comment.'},
                                status=status.HTTP_403_FORBIDDEN)

            issue_id = issue.pk
            data = {
                "description": request.POST.get('description', None),
                "author_user": user.pk,
                "issue": issue_id
            }

            serializer = self.serializer_class(
                instance=comment,
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
            return Response({'message': 'Project or issue may not exist'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, project_pk=None, issues_pk=None, *args, **kwargs):
        try:
            user = request.user
            comment: Comment = self.get_object()

            current_project = Project.objects.filter(pk=project_pk).get()
            issue = Issue.objects.filter(pk=issues_pk).get()
            project_of_issue = issue.project
            if not project_of_issue == current_project:
                return Response({'message': 'Issue does not correspond to the project'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            if not comment.issue == issue:
                return Response({'message': 'Comment does not correspond to the issue'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            is_user_authorized = service.can_user_access_project(current_project, user)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            is_user_authorized_to_delete_comment = service.can_user_edit_comment(comment=comment, user=user)
            if not is_user_authorized_to_delete_comment:
                return Response({'message': 'You must be the author to delete this comment.'},
                                status=status.HTTP_403_FORBIDDEN)

            return super(CommentViewSet, self).destroy(request, project_pk, *args, **kwargs)

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project'}, status=status.HTTP_403_FORBIDDEN)