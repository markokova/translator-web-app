from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
        path('jobs', views.jobs_index, name="jobs"),
        path('jobs/new', views.new_job, name="new_job"),
        path('jobs/<int:job_id>', views.job_detail, name="job_detail"),
]
