"""test_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers

from applicant.views import ApplicantRegisterView, ApplicantRetrieveUpdateView
from employer.views import EmployerRegisterView, EmployerRetrieveUpdateView
from job.views import JobAdRegisterView, JobAdRetrieveUpdateView, JobApplicationRegisterView, ApplicantJobAdListView

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('applicant/new', ApplicantRegisterView.as_view()),
    path('applicant/<int:pk>/', ApplicantRetrieveUpdateView.as_view()),
    path('employer/new', EmployerRegisterView.as_view()),
    path('employer/<int:pk>/', EmployerRetrieveUpdateView.as_view()),
    path('job/new', JobAdRegisterView.as_view()),
    path('job/<int:pk>/', JobAdRetrieveUpdateView.as_view()),
    path('job/<int:pk>/apply', JobApplicationRegisterView.as_view()),
    path('job/all', ApplicantJobAdListView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
