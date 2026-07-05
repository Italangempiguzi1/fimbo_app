from django.contrib import admin
from .models import CreatorEarning, Payout, RewardConfig

admin.site.register(RewardConfig)
admin.site.register(CreatorEarning)
admin.site.register(Payout)
