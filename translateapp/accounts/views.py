from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import Account, Job, Bid, Dispute, Message, Rating
from app.forms import UserForm, AccountForm


# Create your views here.

# See the comment in forms.py for an explanation of why we use two forms
def register(request):
    if request.method == 'POST':
        # Each form is validated separately, each form takes the data from the
        # request that is relevant to it.
        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)
        # Only if both forms are valid, we save the data to the database
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            # We need to set the password separately, because the UserForm
            # doesn't have a password field, it uses two fields for the password
            # and password confirmation.
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            # We need to set the user field on the account before we can save it
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        else:
            return render(request, 'accounts/register.html', {'user_form': user_form, 'account_form': account_form})
    else:
        user_form = UserForm()
        account_form = AccountForm()
        return render(request, 'accounts/register.html', {'user_form': user_form, 'account_form': account_form})

@login_required
def dashboard(request):
    user = request.user
    my_jobs = user.job_set.all()
    my_messages = Message.objects.filter(receiver=user) | Message.objects.filter(sender=user)
    my_messages = my_messages.order_by('-sent_at')
    my_bids = user.bid_set.all()
    my_won_bids = user.bid_set.filter(accepted=True)
    context = {
        'my_jobs': my_jobs,
        'my_messages': my_messages,
        'my_bids': my_bids,
        'my_won_bids': my_won_bids,
    }

    return render(request, 'accounts/dashboard.html', context)


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    accepted_jobs = Job.accepted_jobs_for(user)
    completed_jobs = Job.objects.filter(user=user, status='completed')

    bids = user.bid_set.all()
    won = user.bid_set.filter(accepted=True)

    context = {
        'profile_user': user,
        'accepted_jobs': accepted_jobs,
        'completed_jobs': completed_jobs,
        'bids': bids,
        'won': won,
    }
    return render(request, 'accounts/profile.html', context)
