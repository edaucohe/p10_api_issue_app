from typing import Optional

from users.models import Contributor, User
from projects.models import Project
from issues.models import Issue


# project authorization
def can_user_access_project(project: Project, user: User, role: Optional[Contributor.Role] = None) -> bool:
    return Contributor.objects.filter(project=project, user=user, role=role).exists()


def can_user_edit_project(project: Project, user: User, role: Optional[Contributor.Role] = None) -> bool:
    if role == 'AUTHOR':
        return Contributor.objects.filter(project=project, user=user, role=role).exists()
    else:
        return False


# issue authorization
def can_user_edit_issue(issue: Issue, user: User) -> bool:
    if user == issue.author_user:
        return True
    else:
        return False


# comment authorization
