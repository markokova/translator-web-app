from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

# Create your views here.
def home(request):
    context = {}
    return render(request, 'app/home.html', context)

