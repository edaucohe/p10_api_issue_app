from typing import Optional

from projects.models import Project
from users.models import Contributor, User


def can_user_access_project(project: Project, user: User, role: Optional[Contributor.Role] = None) -> bool:
    return Contributor.objects.filter(project=project, user=user, role=role).exists()

# issues
# comments
