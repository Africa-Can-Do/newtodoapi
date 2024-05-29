from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'department', 'phone_number']
        read_only_fields = ['username']

        

from rest_framework import serializers
from .models import CustomUser, Department

class UserRegistrationSerializer(serializers.ModelSerializer):
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'department_id']

    def create(self, validated_data):
        department_id = validated_data.pop('department_id')
        user = CustomUser.objects.create_user(department_id=department_id, **validated_data)
        return user


from rest_framework import serializers
from django.contrib.auth.models import User

class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password")
        return value

    def validate_new_password(self, value):
        # Add any custom validation for new password here
        return value




