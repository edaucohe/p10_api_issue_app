# from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField, ValidationError, EmailField
from django.contrib.auth import get_user_model

# from users.models import User
from rest_framework.validators import UniqueValidator

from users.models import Contributor


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


class SignUpSerializer(ModelSerializer):
    email = EmailField(required=False, validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Please write the same password"})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ContributorSerializer(ModelSerializer):
    # user = CharField(source="user.username", read_only=True)
    # project = CharField(source='project.title', read_only=True)
    # role = CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']

    def create(self, validated_data):
        return Contributor.objects.create(**validated_data)
