from rest_framework.serializers import ModelSerializer

from comments.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'author_user',
            'issue',
            'description',
            'created_time'
        ]

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
