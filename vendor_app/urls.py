from django.urls import path
from .views import *

urlpatterns =[
   path('vendor_register',vendor_register,name='vendor_register'),  
   path('vendor_login', vendor_login, name='vendor_login'),
   path('admin_vendors', admin_vendors, name='admin_vendors'),
   path('admin_detail/<int:id>/', admin_detail, name='admin_detail'),
   path('vendor_dashboard', vendor_dashboard, name='vendor_dashboard'),
   path('vendor_detail/<int:id>/', vendor_detail, name='vendor_detail'),

   # path('vendor/<int:id>/', vendor_redirect, name='vendor_redirect'),



]