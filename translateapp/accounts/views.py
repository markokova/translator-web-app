from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

# Create your views here.

def dashboard(request):
    user = request.user
    my_jobs = user.job_set.all()
    context = {
        'my_jobs': my_jobs,
    }

    return render(request, 'accounts/dashboard.html', context)
