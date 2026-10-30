from django.contrib import admin
from .models import User
from .models import UserAccount
# Register your models here.
admin.site.register(User)
admin.site.register(UserAccount)
