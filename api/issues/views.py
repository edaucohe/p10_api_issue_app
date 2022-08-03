from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from issues.serializers import IssueSerializer

from issues.models import Issue


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        # Afficher la liste des projets rattachés à l'utilisateur
        queryset = Issue.objects.filter(author_user=self.request.user)
        return queryset
