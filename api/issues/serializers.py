from rest_framework.serializers import ModelSerializer, CharField, IntegerField

from issues.models import Issue


class IssueSerializer(ModelSerializer):
    # tag = CharField(source='get_tag_display')
    # priority = CharField(source='get_priority_display')
    # status = CharField(source='get_status_display')
    # project = CharField(source='project.title')
    # author_user = CharField(source="author_user.username")
    # assignee_user = CharField(source="assignee_user.username")

    class Meta:
        model = Issue
        fields = [
            'id',
            'author_user',
            'assignee_user',
            'title',
            'description',
            'created_time',
            'tag',
            'priority',
            'status',
            'project'
        ]

    def create(self, validated_data):
        return Issue.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.project = validated_data.get('project', instance.project)
        instance.author = self.context['author']
        instance.assignee_user = validated_data.get('assignee_user', instance.assignee_user)
        instance.save()
        return instance
