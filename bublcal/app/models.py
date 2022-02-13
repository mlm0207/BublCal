from django.db import models

# Create your models here.

class user_login(models.Model):
  user_name = models.CharField(max_length=64, primary_key=True)
  email = models.ForeignKey('user_data', on_delete=models.CASCADE)
  # email = models.CharField(max_length=64) - Not sure if foreign key is working, leaving this if needed
  password = models.CharField(max_length=64)
 
class user_data(models.Model):
  email = models.CharField(max_length=64, primary_key=True)
  first_name = models.CharField(max_length=32)
  last_name = models.CharField(max_length=32)
  dob = models.DateField()
  time_zone = models.IntegerField()
  retention_date = models.DateField()

class bubl_template(models.Model):
  task_id = models.CharField(max_length=256, primary_key=True)
  email = models.ForeignKey('user_data', on_delete=models.CASCADE)
  # email = models.CharField(max_length=64) - Not sure if foreign key is working, leaving this if needed
  task_name = models.CharField(max_length=64)
  bubl_template = models.JSONField()
  
class bubl_schedule(models.Model):
  email = models.ForeignKey('user_data', on_delete=models.CASCADE)
  # email = models.CharField(max_length=64) - Not sure if foreign key is working, leaving this if needed
  schedule = models.JSONField()
  
class bubl_month_schedule(models.Model):
  email = models.ForeignKey('user_data', on_delete=models.CASCADE)
  # email = models.CharField(max_length=64) - Not sure if foreign key is working, leaving this if needed
  month = models.IntegerField
  week_bubl = models.JSONField()
  month_bubl = models.JSONField()
