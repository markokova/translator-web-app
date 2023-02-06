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

    def accepted_bid(self):
        return self.bid_set.filter(accepted=True).first()

    def accepted_bidder(self):
        return self.accepted_bid().bidder.account

    @classmethod
    def accepted_jobs_for(cls, user):
        # Svi bidovi gdje je user napravio job na koji je biddano
        accepted_bids = Bid.objects.filter(job__in=user.job_set.all(), accepted=True)
        # Svi jobovi gdje je user napravio job i bidano je na job 
        accepted_jobs = [ bid.job for bid in accepted_bids if bid.job.status != "completed" ]
        return accepted_jobs

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    accepted = models.BooleanField()
    def __str__(self):
        return f"{self.bidder.account.name} - {self.job.title} - {self.price}"

class Dispute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    reason = models.TextField()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender.account.name} - {self.receiver.account.name} - {self.text[:20]}"

class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rater')
    rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    rating = models.IntegerField()
