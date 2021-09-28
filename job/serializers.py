from rest_framework import serializers

from job.models import JobAd, JobApplication


class JobAdRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAd
        fields = ['title', 'image', 'expiration_date', 'job_fields', 'description', 'salary', 'work_hours_per_week']


class JobAdSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    advertiser = serializers.ReadOnlyField(source='advertiser.name')

    class Meta:
        model = JobAd
        fields = ['id', 'advertiser', 'title', 'image', 'expiration_date', 'job_fields', 'description', 'salary',
                  'work_hours_per_week']


class JobApplicationRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['description']

    def create(self, validated_data):
        return JobApplication.objects.create(ad=validated_data['ad'], applicant=validated_data['applicant'],
                                             description=validated_data['description'])

    def to_representation(self, instance):
        return JobApplicationSerializer(instance).data


class JobApplicationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    ad = serializers.ReadOnlyField(source='ad.__str__')
    applicant = serializers.ReadOnlyField(source='applicant.__str__')

    class Meta:
        model = JobApplication
        fields = ['id', 'ad', 'applicant', 'description']
