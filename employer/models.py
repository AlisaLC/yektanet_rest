from django.conf import settings
from django.db import models

from job.models import JobField


class Employer(models.Model):
    name = models.CharField(max_length=200)
    founding_year = models.IntegerField(default=1400)
    address = models.TextField()
    phone_number = models.IntegerField()
    job_fields = models.ManyToManyField(JobField, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
