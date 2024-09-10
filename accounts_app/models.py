from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
 

# Create your models here.

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
        DEALER = "DEALER", "Dealer"
        VENDOR = "VENDOR", "Vendor"  # Add Vendor role here


    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)
    
    
    
class UserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.USER)


class  User(CustomUser):
    base_role = CustomUser.Role.USER
    user = UserManager()

    class Meta:
        proxy = True

    
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    

class   DealerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.DEALER)


    
class Dealer(CustomUser):
    base_role = CustomUser.Role.DEALER
    dealer = DealerManager()

    class Meta:
        proxy = True    


class VendorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.VENDOR)

    
class Vendor(CustomUser):
    base_role = CustomUser.Role.VENDOR
    vendor = VendorManager()

    class Meta:
        proxy = True 