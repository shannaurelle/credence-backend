from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.DecimalField(max_digits=11,decimal_places=0)
    address = models.CharField(max_length=128)
    password = models.CharField(max_length=128,default="gigworker")

    def __str__(self):
        return self.name
