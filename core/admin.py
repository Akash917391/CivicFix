from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(User)
admin.site.register(Staff)
admin.site.register(VolunteerGroup)
admin.site.register(Issue)
admin.site.register(IssueImage)
admin.site.register(IssueUpdate)
admin.site.register(IssueSupport)
admin.site.register(Notification)