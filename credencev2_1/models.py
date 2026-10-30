from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.DecimalField(max_digits=11,decimal_places=0)
    address = models.CharField(max_length=128)
    password = models.CharField(max_length=128,default="gigworker")

    def __str__(self):
        return self.name

class UserAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="useraccount"
    )
    

    def __str__(self):
        return f"UserAccount {self.user.id}"