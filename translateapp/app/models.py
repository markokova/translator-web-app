from django.db import models

from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    translator = models.BooleanField()
    def __str__(self):
        return f"{self.id} - {self.name}"

    def rating(self):
        ratings = Rating.objects.filter(rated=self.user)
        if ratings.count() == 0:
            return "No ratings yet"
        else:
            score = [ rating.rating for rating in ratings ]
            return sum(score) / len(score)

    def raise_if_invalid_balance(self):
        if self.balance < 0:
            raise ValueError("Balance cannot be negative")

class Job(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', "Available"
        ASSIGNED = 'assigned', "Assigned"
        IN_PROGRESS = 'in_progress', "In Progress"
        COMPLETED = 'completed', "Completed"

    class Field(models.TextChoices):
        ART = 'art', "Art"
        BUS = 'business', "Business"
        COMP = 'computers', "Computers"
        EDU = 'education', "Education"
        ENG = 'engineering', "Engineering"
        FIN = 'finance', "Finance"
        LAW = 'law', "Law"
        LIT = 'literature', "Literature"
        MED = 'medicine', "Medicine"
        SCI = 'science', "Science"
        SOC = 'social_sciences', "Social Sciences"
        TECH = 'technology', "Technology"

    class Language(models.TextChoices):
        ENG = 'en', "English"
        SPA = 'spa', "Spanish"
        FRE = 'fr', "French"
        GER = 'de', "German"
        ITA = 'it', "Italian"
        JPN = 'ja', "Japanese"
        CRO = 'hr', "Croatian"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    source_lang = models.CharField(
            max_length=3, 
            choices=Language.choices,
            default=Language.ENG,
    )
    target_lang = models.CharField(
            max_length=3,
            choices=Language.choices,
            default=Language.CRO,
    )
    field = models.CharField(
            max_length=100,
            choices=Field.choices,
            default=Field.ENG,
    )
    budget = models.DecimalField(max_digits=8, decimal_places=2)
    text = models.TextField()
    status = models.CharField(
            max_length=100, 
            choices=Status.choices,
            default=Status.AVAILABLE,
    )
    translation = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.account.name} - {self.title}"

    def accepted_bid(self):
        return self.bid_set.filter(accepted=True).first()

    def accepted_bidder(self):
        return self.accepted_bid().bidder.account

    def owner(self):
        return self.user.account

    # Helper method to check if the job is available, since checking the status
    # directly from the template is not very readable.
    def is_available(self):
        return self.status == self.Status.AVAILABLE

    def is_completed(self):
        return self.status == self.Status.COMPLETED

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
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.bidder.account.name} - {self.job.title} - {self.price}"
    def job_owner(self):
        return self.job.user

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
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE)
    rating = models.IntegerField()
