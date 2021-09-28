from django.conf import settings
from django.db import models

from job.models import JobField

GENDERS = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class Applicant(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, default='M', choices=GENDERS)
    job_fields = models.ManyToManyField(JobField, blank=True)
    resume = models.FileField(blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return self.first_name + ' ' + self.last_name
