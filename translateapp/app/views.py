from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .models import Job, Bid, Dispute, Message, Rating
from .forms import JobForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    context = {}
    return render(request, 'app/home.html', context)

@login_required
def jobs_index(request):
    if request.user.account.translator:
        jobs = Job.objects.filter(status='available')
        context = {
            'jobs': jobs,
        }
        return render(request, 'app/jobs_index.html', context)
    else:
        return HttpResponseRedirect(reverse('home_path'))

@login_required
def new_job(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JobForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # save the form data to model and persist to db
            job = form.save(commit=False)
            # set the user to the current user
            job.user = request.user
            # set the status to available using the enum defined in the model class
            job.status = Job.Status.AVAILABLE
            # Persist the job to the db
            job.save()

            # redirect to job listing page:
            return HttpResponseRedirect(reverse('app:jobs'))
        else: 
            # if form is not valid, render the form with error messages
            # and the data the user entered. The error messages are contained
            # in the form.errors dictionary and can be accessed in the template.
            return render(request, 'app/new_job.html', {'form': form})
    else:
        # if a GET (or any other method) we'll create a blank form
        # and render it in the template like usual
        form = JobForm()
        context = {
            'form': form,
        }
        return render(request, 'app/jobs_new.html', context)

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    context = {
        'job': job,
    }
    return render(request, 'app/jobs_detail.html', context)
