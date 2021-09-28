from django.contrib.auth.models import User
from rest_framework import serializers

from applicant.models import Applicant


class ApplicantRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = Applicant
        fields = ['first_name', 'last_name', 'age', 'gender', 'username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return Applicant.objects.create(
            user=user, first_name=validated_data['first_name'], last_name=validated_data['last_name'],
            age=validated_data['age'], gender=validated_data['gender'])

    def to_representation(self, instance):
        return ApplicantSerializer(instance).data


class ApplicantSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Applicant
        fields = ['id', 'first_name', 'last_name', 'age', 'gender', 'job_fields', 'resume', 'user']
