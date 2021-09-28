from django.contrib.auth.models import User
from rest_framework import serializers

from employer.models import Employer


class EmployerRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = Employer
        fields = ['name', 'founding_year', 'address', 'phone_number', 'username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return Employer.objects.create(
            user=user, name=validated_data['name'], founding_year=validated_data['founding_year'],
            address=validated_data['address'], phone_number=validated_data['phone_number'])

    def to_representation(self, instance):
        return EmployerSerializer(instance).data


class EmployerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Employer
        fields = ['id', 'name', 'founding_year', 'address', 'phone_number', 'job_fields', 'user']
