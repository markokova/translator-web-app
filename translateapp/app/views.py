from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .models import Job, Bid, Dispute, Message, Rating
from .forms import JobForm

# Create your views here.
def home(request):
    context = {}
    return render(request, 'app/home.html', context)

def jobs_index(request):
    jobs = Job.objects.filter(status='available')
    context = {
        'jobs': jobs,
    }
    return render(request, 'app/jobs_index.html', context)

def new_job(request):
    form = JobForm()
    context = {
        'form': form,
    }
    return render(request, 'app/jobs_new.html', context)
    pass

def job_detail(request, job_id):
    pass
