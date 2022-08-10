from typing import Optional

from users.models import Contributor, User
from projects.models import Project
from issues.models import Issue
from comments.models import Comment


# project authorization
def can_user_access_project(project: Project, user: User) -> bool:
    return Contributor.objects.filter(project=project, user=user).exists()


def can_user_edit_project(project: Project, user: User, role: Optional[Contributor.Role] = None) -> bool:
    if role == 'AUTHOR':
        return Contributor.objects.filter(project=project, user=user, role=role).exists()
    else:
        return False


# issue authorization
def can_user_edit_issue(issue: Issue, user: User) -> bool:
    return user == issue.author_user


# contributor authorization
def can_user_delete_contributor(author: User, user: User) -> bool:
    return user == author


# comment authorization
def can_user_edit_comment(comment: Comment, user: User) -> bool:
    return user == comment.author_user
