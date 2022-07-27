# from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField, ValidationError, EmailField
from django.contrib.auth import get_user_model

# from users.models import User
# from rest_framework.validators import UniqueValidator


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


# class SignUpSerializer(ModelSerializer):
#     email = EmailField(required=False, validators=[UniqueValidator(queryset=User.objects.all())])
#     password = CharField(write_only=True, required=True, validators=[validate_password])
#     password_confirm = CharField(write_only=True, required=True)
#
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'first_name', 'last_name', 'email', 'password']
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': False}
#         }
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password_confirm']:
#             raise ValidationError({"password": "Please write the same password"})
#
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user
