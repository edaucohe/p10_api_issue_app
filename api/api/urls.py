"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import SignUpViewSet, UserViewSet, ContributorViewSet
from projects.views import ProjectViewSet
from issues.views import IssueViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# /projects/   ||   /projects/{id}/
router.register(r'projects', ProjectViewSet, basename='project')

# /projects/{id}/issues/   ||   /projects/{id}/issues/{id}
project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'issues', IssueViewSet, basename='issue')

# /projects/{id}/users/   ||   /projects/{id}/users/{id}
project_router.register(r'users', ContributorViewSet, basename='contributor')

# /projects/{id}/issues/{id}/comments/   ||   /projects/{id}/issues/{id}/comments/{id}/
# TODO Add when CommentViewSet implemented
# issue_router = routers.NestedSimpleRouter(router, r'issues', lookup='issues')
# router.register(r'comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', SignUpViewSet.as_view(), name='signup'),
    path(r'', include(router.urls)),
    path(r'', include(project_router.urls)),
    # TODO Add when CommentViewSet implemented
    # path(r'', include(issue_router.urls)),
]

