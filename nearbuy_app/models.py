from django.db import models
from accounts_app.models import*




# Create your models here.

class register_user(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    gender=models.CharField(null=True,max_length=10)
    state=models.CharField(null=True,max_length=30)
    city=models.CharField(null=True,max_length=40)
    phone=models.IntegerField(null=True)

class Users(models.Model):
    name_user = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=15)  # Adjust length based on your needs
    def __str__(self):
        return f"{self.name_user} ({self.user_phone_number})"