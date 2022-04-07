from django.db import models

# Create your models here.

class UserData(models.Model):
    email       = models.CharField(max_length=64, primary_key=True)
    password    = models.CharField(max_length=64, default='None')
    firstName   = models.CharField(max_length=32)
    lastName    = models.CharField(max_length=32)
    birthday    = models.DateField()
    #Not needed atm - time_zone = models.IntegerField()
    #Not needed atm - retention_date = models.DateField()

class Bubl(models.Model):
    email = models.ForeignKey(UserData, on_delete=models.CASCADE);
    name = models.CharField(max_length=32);
    note = models.CharField(max_length=32);
    date = models.DateField();
    time = models.TimeField(auto_now=False, auto_now_add=False);
    length = models.IntegerField();
    moved   = models.IntegerField();
    deleted = models.BooleanField(default=False);
