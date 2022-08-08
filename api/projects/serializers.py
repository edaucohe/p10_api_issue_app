from rest_framework.serializers import ModelSerializer, CharField

from projects.models import Project


class ProjectSerializer(ModelSerializer):
    type = CharField(source='get_type_display', read_only=True)
    author_user = CharField(source="author_user.username", read_only=True)

    class Meta:
        model = Project
        # fields = '__all__'
        fields = [
            'id',
            'author_user',
            'title',
            'description',
            'created_time',
            'type'
        ]

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.author = self.context['author']
        instance.save()
        return instance
