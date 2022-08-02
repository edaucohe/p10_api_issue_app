from rest_framework.serializers import ModelSerializer

from projects.models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.author = self.context['author']
        instance.save()
        return instance
