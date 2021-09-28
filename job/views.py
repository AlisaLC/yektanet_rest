from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from job.filters import SalaryFilter
from job.models import JobAd, JobApplication
from job.permissions import IsEmployer, IsOwnerOrReadOnly, IsApplicant
from job.serializers import JobAdRegisterSerializer, JobAdSerializer, JobApplicationRegisterSerializer


class JobAdRegisterView(generics.CreateAPIView):
    queryset = JobAd.objects.all()
    serializer_class = JobAdRegisterSerializer
    permission_classes = [IsEmployer]

    def perform_create(self, serializer):
        try:
            serializer.save(advertiser=self.request.user.employer)
        except:
            raise ValidationError({'error': 'User is not applicant'}, code=status.HTTP_401_UNAUTHORIZED)


class JobAdRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobAd.objects.all()
    serializer_class = JobAdSerializer
    permission_classes = [IsOwnerOrReadOnly]


class JobApplicationRegisterView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationRegisterSerializer
    permission_classes = [IsApplicant]

    def perform_create(self, serializer):
        try:
            serializer.save(applicant=self.request.user.applicant, ad=JobAd.objects.filter(id=self.kwargs['pk']).get())
        except:
            raise ValidationError({'error': 'User is not applicant'}, code=status.HTTP_401_UNAUTHORIZED)


class ApplicantJobAdListView(generics.ListAPIView):
    serializer_class = JobAdSerializer
    permission_class = [IsApplicant]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_class = SalaryFilter

    def get_queryset(self):
        try:
            return JobAd.get_unexpired_queryset_with_common_job_fields_applicant(self.request.user.applicant)
        except:
            return JobAd.get_unexpired_queryset()

    def filter_queryset(self, queryset):
        search_term = self.request.query_params.get('search')
        salary_max = self.request.query_params.get('salary__lt', 0)
        if salary_max == '':
            salary_max = 0
        salary_max = int(salary_max)
        salary_min = self.request.query_params.get('salary__gt', 0)
        if salary_min == '':
            salary_min = 0
        salary_min = int(salary_min)
        if not search_term and not salary_min and not salary_max:
            return queryset
        if search_term:
            # queryset = queryset.filter(Q(title__contains=search_term) | Q(description__contains=search_term) | Q(
            #     job_fields__name__contains=search_term))
            queryset = JobAd.search(queryset, search_term)
        if salary_min or salary_max:
            queryset = JobAd.get_queryset_by_salary(queryset, salary_min, salary_max)
        return queryset
