from django.db import models

from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    translator = models.BooleanField()
    def __str__(self):
        return f"{self.id} - {self.name}"

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    source_lang = models.CharField(max_length=100)
    target_lang = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=8, decimal_places=2)
    text = models.TextField()
    status = models.CharField(max_length=100, default='available')
    translation = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.account.name} - {self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    accepted = models.BooleanField()

class Dispute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    reason = models.TextField()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    text = models.TextField()

class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rater')
    rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    rating = models.IntegerField()
