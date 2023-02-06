from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import Account, Job, Bid, Dispute, Message, Rating

# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    my_jobs = user.job_set.all()
    my_messages = Message.objects.filter(receiver=user) | Message.objects.filter(sender=user)
    my_messages = my_messages.order_by('-sent_at')
    context = {
        'my_jobs': my_jobs,
        'my_messages': my_messages,
    }

    return render(request, 'accounts/dashboard.html', context)


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    accepted_jobs = Job.accepted_jobs_for(user)
    completed_jobs = Job.objects.filter(user=user, status='completed')


    context = {
        'profile_user': user,
        'accepted_jobs': accepted_jobs,
        'completed_jobs': completed_jobs,
    }
    return render(request, 'accounts/profile.html', context)
