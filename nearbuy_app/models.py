from django.db import models
from accounts_app.models import*




# Create your models here.

class register_user(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    gender=models.CharField(null=True,max_length=10)
    state=models.CharField(null=True,max_length=30)
    city=models.CharField(null=True,max_length=40)
    phone=models.IntegerField(null=True)
