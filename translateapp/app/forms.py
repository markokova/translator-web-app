from .models import Job, Bid, Dispute, Message, Rating

from django import forms
from django.forms import ModelForm

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'field', 'source_lang', 'target_lang', 'budget', 'text']
