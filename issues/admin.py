from django.contrib import admin
from .models import Issue, Status, Priority 
# Register your models here.

admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Issue)