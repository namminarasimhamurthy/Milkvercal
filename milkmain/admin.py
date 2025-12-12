from django.contrib import admin
from .models import MilkUser
from .models import DailyRecord

admin.site.register(MilkUser)
admin.site.register(DailyRecord)