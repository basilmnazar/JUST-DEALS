from django.db import models
from django.contrib.auth.models import User
from datetime import time
from django.core.exceptions import ValidationError
from accounts_app.models import*
from django.contrib.auth.hashers import make_password, check_password

class Vendor(models.Model):
    VENDOR_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
        # Add more vendor types as needed
    ]
    
    # Vendor name
    fname = models.CharField(max_length=255)

    # Vendor type
    vendor_type = models.CharField(max_length=50, choices=VENDOR_TYPE_CHOICES)

    # Point of contact (integer field)
    point_of_contact = models.IntegerField(default=0)

    # Phone
    phone = models.CharField(max_length=15)

    # Vendor logo (image field)
    image = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)

    account_holder_name = models.CharField(max_length=255, default='')
    bank_name = models.CharField(max_length=255, default='')
    branch = models.CharField(max_length=255, default='')
    account_number = models.CharField(max_length=20, default='')
    ifsc_code = models.CharField(max_length=11, default='')

    # Terms and conditions
    terms = models.TextField()

    # Username
    uname = models.CharField(max_length=150, unique=True)

    # Password
    password = models.CharField(max_length=128)  # Consider using Django's built-in User model for authentication

    # Confirm password (not stored in the model, used for validation only)
    cpassword = models.CharField(max_length=128)

    # Commission percentage
    commission_percentage = models.DecimalField(
        max_digits=5,  # Total number of digits
        decimal_places=2,  # Number of decimal places
        default=0.00,  # Default value
    )

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def __str__(self):
        return self.fname



def validate_time_format(value):
  try:
    # Assuming your time fields are TimeFields
    time.fromisoformat(value)  # Attempt conversion (ISO format)
  except ValueError:
    raise ValidationError('Invalid time for mat. Use HH:MM format.')

# Create your models here.

class Dealers(models.Model):
    MERCHANT_TYPE_CHOICES = (
        ("hotel", "Hotel"),
        ("restaurant", "Restaurant"),
        ("spa", "Spa"),
        ("saloon", "Saloon")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    merchant_name = models.CharField(max_length=255,null=True, blank=True)
    business_owner_name = models.CharField(max_length=255, null=True, blank=True)
    merchant_type = models.CharField(choices=MERCHANT_TYPE_CHOICES, max_length=30, null=True, default='hotel')
    merchant_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    contact_person = models.IntegerField(null=True, blank=True)
    outlet_name = models.CharField(max_length=255, null=True, blank=True)
    outlet_description = models.TextField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    outlet_img = models.ImageField(upload_to='images/',null=True, blank=True )
   


class Voucher(models.Model):
    dealer = models.ForeignKey(Dealers, on_delete=models.CASCADE, null=True, blank=True)
    voucher_name =models.CharField(max_length=255, blank=True, null=True)  # Optional, allows empty strings and NULLs
    voucher_price = models.IntegerField(default=0)  # Default value of 0, no need for null=True
    voucher_about = models.TextField(blank=True, default='')  # Default value of an empty string
    voucher_description = models.TextField(blank=True, default='')  
    button_link = models.URLField(blank=True, null=True)  # Add this line for button link
    voucher_date = models.DateField(null=True, blank=True)

class VoucherCoupon(models.Model):
    coupon_name = models.CharField(max_length=255, null=True, default='')
    coupon_description = models.TextField(blank=True, null=True, default='')
    coupon_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon_button_link = models.URLField(max_length=200, blank=True, null=True)


class Users(models.Model):
    name_user = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=10, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.name_user