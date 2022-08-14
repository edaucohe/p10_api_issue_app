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

    @action(detail=True, methods=['get'])
    def get_users(self):
        queryset = User.objects.filter(active=True)
        username = self.request.GET.get('username')
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset


class SignUpViewSet(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return get_user_model().objects.all()


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Contributor.objects.all()

    def list(self, request, project_pk=None, *args, **kwargs):
        try:
            user = self.request.user
            project = Project.objects.filter(pk=project_pk).get()

            is_user_authorized = service.can_user_access_project(project, user)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            contributor = list(Contributor.objects.filter(project=project_pk).order_by('id'))
            return Response(self.serializer_class(contributor, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'Project does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    def create(self, request, project_pk=None, *args, **kwargs):
        try:
            current_user = request.user
            project = Project.objects.filter(pk=project_pk).get()

            if not current_user == project.author_user:
                return Response({'message': 'You are not author of this project'}, status=status.HTTP_403_FORBIDDEN)

            username_of_contributor = request.POST.get('user', None)
            contributor_pk = User.objects.filter(username=username_of_contributor).get().pk
            data = {
                "user": contributor_pk,
                "project": int(project_pk),
                "role": request.POST.get('role', None)
                }

            serializer = self.serializer_class(data=data, context={'author': current_user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, project_pk=None, *args, **kwargs):
        try:
            contributor: Contributor = self.get_object()
            contributor_project = contributor.project
            project = Project.objects.filter(pk=project_pk).get()

            if not contributor_project == project:
                return Response({'message': 'Contributor is not part of this project'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            user = request.user
            is_user_authorized = service.can_user_access_project(project, user)
            if not is_user_authorized:
                return Response({'message': 'You are not a contributor'}, status=status.HTTP_403_FORBIDDEN)

            author = project.author_user
            is_user_authorized_to_delete_issue = service.can_user_delete_contributor(author=author, user=user)
            if not is_user_authorized_to_delete_issue:
                return Response({'message': 'You must be the author to delete this contributor.'},
                                status=status.HTTP_403_FORBIDDEN)

            if author == contributor.user:
                return Response({'message': 'You cannot delete yourself.'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)

            return super(ContributorViewSet, self).destroy(request, project_pk, *args, **kwargs)

        except ObjectDoesNotExist:
            return Response({'message': 'You have not access to the project'}, status=status.HTTP_403_FORBIDDEN)
