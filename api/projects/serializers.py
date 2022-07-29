from rest_framework.serializers import ModelSerializer

from projects.models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    # def create(self, validated_data):
    #     return Project.objects.create(**validated_data)
