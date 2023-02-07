from .models import Job, Bid, Dispute, Message, Rating, Account
from django.contrib.auth.models import User

from django import forms
from django.forms import ModelForm

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'field', 'source_lang', 'target_lang', 'budget', 'text']

        widgets = {
            'text': forms.Textarea(attrs={'rows': 20}),
        }

# We use two modelForms for the user and the account, because we want to avoid 
# having a custom user model. We want to use the default user model provided by
# Django. The default user model does not have all the fields we need, so we
# create a separate model for the account and link it to the user model.
# Using two forms gives us easier validation, since each form can have its own
# validation logic.
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    #https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#interaction-with-model-validation
    #https://docs.djangoproject.com/en/4.1/ref/forms/validation/#cleaning-a-specific-field-attribute
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2




class AccountForm(ModelForm):
    class Meta: 
        model = Account
        fields = ['name', 'translator']

        labels = {
            "translator": "Do you want to be a translator?",
        }

class BidForm(forms.Form):
    price = forms.DecimalField(max_digits=8, decimal_places=2, min_value=0.01)


class TranslationForm(forms.Form):
    translation = forms.CharField(widget=forms.Textarea(attrs={'rows': 20}))

    def clean(self):
        cleaned_data = super().clean()
        translation = cleaned_data.get('translation')
        if not translation:
            self.add_error('translation', 'Translation must not be empty')


class DisputeForm(ModelForm):
    class Meta: 
        model = Dispute
        fields = ['reason']

    labels = {
        "reason": "Please explain your reasons for the dispute",
    }

