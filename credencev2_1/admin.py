from django.contrib import admin
from .models import User
from .models import UserAccount
from .models import Address
# Register your models here.
admin.site.register(User)
admin.site.register(UserAccount)
admin.site.register(Address)
