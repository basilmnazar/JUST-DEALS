from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns =[
    
    # path('admin_register/',admin_register,name='admin_register'),
    # path('admin_login/',admin_login,name='admin_login'),
    path('admin_index/',admin_index,name='admin_index'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('logout/',admin_logout, name="admin_logout"), 
    path('about_page/',about_page, name="about_page"), 
    #email
   
    
]