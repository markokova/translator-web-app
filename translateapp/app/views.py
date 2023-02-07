from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .models import Job, Bid, Dispute, Message, Rating
from .forms import JobForm, BidForm, TranslationForm
from django.contrib.auth.decorators import login_required

from django.db import transaction

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
    form = BidForm()
    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'app/jobs_detail.html', context)

@login_required
def bid(request, job_id):
    if request.method == 'POST' and request.user.account.translator:
        job = get_object_or_404(Job, pk=job_id)
        form = BidForm(request.POST)
        if form.is_valid():
            bid = Bid(price=form.cleaned_data['price'], 
                    job=job, 
                    bidder=request.user)
            bid.save()
            return HttpResponseRedirect(reverse('app:job_detail', args=(job.id,)))
        else:
            return render(request, 'app/jobs_detail.html', {'job': job, 'form': form})

@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    job = bid.job

    # check if the user is the job owner, otherwise anyone can accept any bid
    if request.method == 'POST' and job.user == request.user:
        bid.accepted = True
        bid.save()
        job.status = Job.Status.ASSIGNED
        job.save()
        return HttpResponseRedirect(reverse('accounts:dashboard'))

@login_required
def deliver_translation(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    job = bid.job

    if request.method == 'POST' and bid.accepted and request.user == bid.bidder:
        form = TranslationForm(request.POST)
        if form.is_valid():
            job.translation = form.cleaned_data['translation']
            job.status = Job.Status.COMPLETED
            job.save()
            bid.completed = True
            bid.save()
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        else:
            return render(request, 'app/deliver_translation.html', {'job': job, 'form': form})
    else:
        form = TranslationForm()
        context = {
            'job': job,
            'form': form,
        }
        return render(request, 'app/deliver_translation.html', context)

@login_required
def bid_detail(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    job = bid.job
    if request.user == bid.bidder or request.user == job.user:
        context = {
            'bid': bid,
            'job': job,
        }
        return render(request, 'app/bid_detail.html', context)
    else:
        return HttpResponseRedirect(reverse('home_path'))

@login_required
def rate_bid(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    job = bid.job

    if request.method == 'POST' and request.user == job.user:
        # Transaction is used to ensure that all the db operations are
        # atomic, ie. either all the operations succeed, or all of
        # them are rolled back. We want to avoid a situation where a
        # user rates a translation, gets tokens deducted, and then a
        # bug happens in saving the bidder balance and bidder never
        # gets the tokens. Tokens then remain in limbo, they were
        # deducted from the owner, but never arrived at the bidder's
        # account.
        #https://docs.djangoproject.com/en/4.1/topics/db/transactions/
        try: 
            with transaction.atomic():
                rating = Rating(
                    rating=request.POST['rating'],
                    rater=request.user,
                    rated=bid.bidder,
                    job=job,
                    bid=bid,
                )

                owner = request.user.account
                bidder = bid.bidder.account

                owner.balance -= bid.price
                owner.raise_if_invalid_balance()
                bidder.balance += bid.price
                bidder.raise_if_invalid_balance()

                owner.save()
                bidder.save()
                rating.save()

        except Exception as e:
            # Returning the user with the caught error in the context allows us
            # to display the error in the template. Check base.html for the
            # .alert classes. Also, we need to get the bid and job objects
            # again, because the transaction was rolled back and the objects
            # are no longer valid. The objects remained in memory and they retained
            # the reference the rating object, which never got saved to the db.
            bid = get_object_or_404(Bid, pk=bid_id)
            job = bid.job
            return render(request, 'app/bid_detail.html', {'bid': bid, 'job': job, 'error': e})


        return HttpResponseRedirect(reverse('app:bid_detail', args=[bid.id]))


