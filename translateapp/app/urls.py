from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
        path('jobs', views.jobs_index, name="jobs"),
        path('jobs/new', views.new_job, name="new_job"),
        path('jobs/<int:job_id>', views.job_detail, name="job_detail"),
        path('jobs/<int:job_id>/bid', views.bid, name="bid"),
        path('bids/<int:bid_id>/accept', views.accept_bid, name="accept_bid"),

]
