from django_filters import FilterSet

from job.models import JobAd


class SalaryFilter(FilterSet):
    class Meta:
        model = JobAd
        fields = {'salary': ['lt', 'gt']}
