from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
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
    contact_number = PhoneNumberField(blank=True, null=True, unique=True) 

    def __str__(self):
        return f"UserAccount {self.user.id}"

class Platform (models.Model):
    platform_name = models.CharField(max_length=100)
    platform_type = models.CharField(max_length=100)
    def __str__(self):
        return self.platform_name

class JobInfo (models.Model):
    user_account= models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    job_name  = models.CharField(max_length=100)
    job_type  = models.CharField(max_length=100)
    job_description = models.CharField(max_length=300)

    def __str__(self):
        return self.job_name

class Address(models.Model):
    user_account = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="address"
    )

    region = models.CharField(max_length=150)
    province = models.CharField(max_length=150)
    municipality_city = models.CharField(max_length=150)
    barangay = models.CharField(max_length=150)
    street_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.barangay}, {self.municipality_city}"

