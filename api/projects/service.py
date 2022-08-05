from typing import Optional

from users.models import Contributor, User
from projects.models import Project


def can_user_access_project(project: Project, user: User, role: Optional[Contributor.Role] = None) -> bool:
    return Contributor.objects.filter(project=project, user=user, role=role).exists()


def can_user_edit_project(project: Project, user: User, role: Optional[Contributor.Role] = None) -> bool:
    if role == 'AUTHOR':
        return Contributor.objects.filter(project=project, user=user, role=role).exists()
    else:
        return False

# issues
# comments
