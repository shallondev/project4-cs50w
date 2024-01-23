from django.contrib import admin

from .models import Posting, User

# Register your models here.
admin.site.register(Posting)
admin.site.register(User)