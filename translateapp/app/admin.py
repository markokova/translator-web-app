from django.contrib import admin

from app.models import Account, Job, Bid, Dispute, Message, Rating

admin.site.register(Account)
admin.site.register(Job)
admin.site.register(Bid)
admin.site.register(Dispute)
admin.site.register(Message)
admin.site.register(Rating)

