from django.urls import path
from .views import *

urlpatterns =[
   path('register_and_add_outlet/<int:vendor_id>/', register_and_add_outlet, name='register_and_add_outlet'),
   path('dealer_index',dealer_index,name='dealer_index'),  
   path('dealer_login',dealer_login,name='dealer_login'),  
   # path('index',index_main,name='index_main'),
   path('',main_login,name='main_login'),
   path('index',index,name='index'),
   path('voucher_add',voucher_add,name='voucher_add'), 
   path('outlet_deatails/<int:pk>/',outlet_deatails,name='outlet_deatails'),
   # path('outlet_fields_add',outlet_fields_add,name='outlet_add'),
   path('unauthorized',unauthorized,name='unauthorized'),
   path('dealer_logout',dealer_logout,name='dealer_logout'),
   path('outlet_category', outlet_category, name='outlet_category'),
   path('add_voucher_coupon', add_voucher_coupon, name='add_voucher_coupon'),
   path('coupon_list/', coupon_list, name='coupon_list'),
   path('edit_voucher_coupon/<int:pk>/', edit_voucher_coupon, name='edit_voucher_coupon'),
   path('delete_voucher_coupon/<int:pk>/', delete_voucher_coupon, name='delete_voucher_coupon'),
   path('vendor/<int:vendor_id>/index/',vendor_index, name='vendor_index'),


]