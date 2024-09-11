from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from .models import VoucherCoupon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from deal_app.models import*
from nearbuy_app.models import*
# from datetime import time
from .models import Dealers
from .models import Vendor
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from admin_backend.decorators import super_login_required
from django.shortcuts import render, redirect
# from django.core.mail import send_mail
import re
from django.contrib.auth import authenticate,login as auth_login,logout,login
# Create your views here.
@super_login_required
def dealer_index(request):
    dealerdatas = Dealers.objects.all()
    dealer_count = dealerdatas.count()  # Get the number of dealers
    return render(request, 'dealer_index.html', {'dealerdatas': dealerdatas, 'dealer_count': dealer_count})
    

def unauthorized(request):
    return render(request, 'unauthorized.html')

def main_login(request):
    if request.method == 'POST':
        # Retrieve form data
        name_user = request.POST.get('name')
        user_phone_number = request.POST.get('phone_number')
        
        # Validate the phone number
        if not re.match(r'^\d{10}$', user_phone_number):
            messages.error(request, 'Invalid phone number. It must be a 10-digit number.')
            return render(request, 'main_login.html')

        # Validate the username
        if not name_user:
            messages.error(request, 'Username cannot be empty.')
            return render(request, 'main_login.html')
        
        # Check if the username already exists
        if Users.objects.filter(name_user=name_user).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'main_login.html')

        # Save the user data to the database
        Users.objects.create(name_user=name_user, user_phone_number=user_phone_number)
        
        # Redirect to the index page
        return redirect('index')
    
    return render(request, 'main_login.html')
    



# views for registration /////////////
##############################here we need to cahange like jobportal company register#######
# @super_login_required
def register_and_add_outlet(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        # Extract form data
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        merchant_name = request.POST.get('merchant_name', '')
        business_owner_name = request.POST.get('business_owner_name', '')
        merchant_type = request.POST.get('merchant_type', 'hotel')
        merchant_address = request.POST.get('merchant_address', '')
        city = request.POST.get('city', '')
        phone = request.POST.get('phone', '')
        contact_person = request.POST.get('contact_person', 0)
        outlet_name = request.POST.get('outlet_name', '')
        outlet_description = request.POST.get('outlet_description', '')
        start_time = request.POST.get('start_time', '00:00:00')
        end_time = request.POST.get('end_time', '23:59:59')
        outlet_img = request.FILES.get('outlet_img')

        # Validate that passwords match
        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register_and_add_outlet.html', {
                'vendor': vendor,
                'merchant_type_choices': Dealers.MERCHANT_TYPE_CHOICES
            })

        # Check if the username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'register_and_add_outlet.html', {
                'vendor': vendor,
                'merchant_type_choices': Dealers.MERCHANT_TYPE_CHOICES
            })

        # Create a new user and dealer
        user = User.objects.create_user(username=uname, password=password)
        
        dealer = Dealers(
            user=user,
            vendor=vendor,
            merchant_name=merchant_name,
            business_owner_name=business_owner_name,
            merchant_type=merchant_type,
            merchant_address=merchant_address,
            city=city,
            phone=phone,
            contact_person=contact_person,
            outlet_name=outlet_name,
            outlet_description=outlet_description,
            start_time=start_time,
            end_time=end_time,
            outlet_img=outlet_img
        )
        dealer.save()

        messages.success(request, "Dealer registered and outlet added successfully.")
        return redirect('vendor_dashboard')

    merchant_type_choices = Dealers.MERCHANT_TYPE_CHOICES

    return render(request, 'register_and_add_outlet.html', {
        'vendor': vendor,
        'merchant_type_choices': merchant_type_choices,
    })


                            
                      
            
# views for login page///////

def dealer_login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dealer_vouchers')  # Redirect to the dealer vouchers page
        else:
            return render(request, 'dealer_login.html', {'message': 'Invalid credentials'})
    else:
        return render(request, 'dealer_login.html')
#forgot password///////

def forgot_password(request):
    return render(request,'password_reset_done.html')

    
    #logout

def dealer_logout(request):
    logout(request)
    return redirect("dealer_login")
# ////////////////////


# def index_main(request):
#     items = Dealers.objects.all()
#     return render(request, 'index_main.html',{'items':items} )


# @super_login_required
def voucher_add(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'cancel':
            # Redirect to a different page or perform a cancel action
            return redirect('dealer_vouchers')  # Or any other URL you'd like

        # Handle the form submission if not cancel
        voucher_name = request.POST.get('item-name')
        voucher_price = request.POST.get('item-price')
        voucher_description = request.POST.get('description')
        voucher_about = request.POST.get('about')

        if not voucher_name or not voucher_price or not voucher_description:
            return render(request, 'voucher.html', {'message': 'Please fill in all required fields'})

        try:
            voucher_price = int(voucher_price)
        except ValueError:
            return render(request, 'voucher.html', {'message': 'Invalid price format'})

        # Get the dealer associated with the logged-in user
        dealer = Dealers.objects.get(user=request.user)
        
        # Create and save the new voucher
        new_voucher = Voucher(
            dealer=dealer,
            voucher_name=voucher_name,
            voucher_price=voucher_price,
            voucher_description=voucher_description,
            voucher_about=voucher_about
        )
        new_voucher.save()

        return redirect('dealer_vouchers')  # Redirect to the dealer index page or wherever appropriate

    return render(request, 'voucher.html')

## functions for outlet_deatails 
def outlet_deatails(request, pk):
    # Fetch the Outlet instance using the primary key
    outlet_datas = get_object_or_404(Dealers, pk=pk)
    vouchers = Voucher.objects.filter(dealer=outlet_datas)
    coupons = VoucherCoupon.objects.all()

    # Render the template with the context
    return render(request, 'outlet_deatails.html', {
        'items': outlet_datas,
        'vouchers': vouchers,
        'coupons': coupons
        
        
    })


def outlet_category(request, category=None):
    # Get all merchant types for the dropdown
    merchant_types = dict(Dealers.MERCHANT_TYPE_CHOICES)
    selected_type = request.GET.get('type', category)

    # Filter dealers based on the selected type
    if selected_type and selected_type in merchant_types:
        outlets = Dealers.objects.filter(merchant_type=selected_type)
    else:
        outlets = Dealers.objects.all()

    return render(request, 'outlet_catogory.html', {
        'items': outlets,
        'merchant_types': merchant_types,
        'selected_type': selected_type,
        'current_category': merchant_types.get(selected_type, 'All Catogories')  # Default to 'All Categories' if none is selected
    })




 

#############for new index##################
def index(request):
    items = Dealers.objects.all()
    merchant_types = Dealers.objects.values_list('merchant_type', flat=True).distinct()
    
    context = {
        'items': items,
        'merchant_types': merchant_types
    }
    
    return render(request, 'index.html', context)

def vendor_index(request, vendor_id):
    # Fetch the vendor based on the provided vendor_id
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    # Fetch items related to the vendor
    # items = Dealers.objects.filter(vendor=vendor)
    items = Dealers.objects.all()
    # merchant_types = Dealers.objects.filter(vendor=vendor).values_list('merchant_type', flat=True).distinct()
    merchant_types = Dealers.objects.all().values_list('merchant_type', flat=True).distinct()
    
    context = {
        'vendor': vendor,
        'items': items,
        'merchant_types': merchant_types
    }
    
    return render(request, 'index.html', context)


def add_voucher_coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        coupon_description = request.POST.get('coupon_description', '')
        coupon_price = request.POST.get('coupon_price')
        coupon_button_link = request.POST.get('coupon_button_link', '')

        if coupon_name and coupon_price:
            try:
                coupon_price = float(coupon_price)
            except ValueError:
                return HttpResponse("Invalid price format", status=400)
            
            # Create and save the new VoucherCoupon instance
            voucher_coupon = VoucherCoupon(
                coupon_name=coupon_name,
                coupon_description=coupon_description,
                coupon_price=coupon_price,
                coupon_button_link=coupon_button_link
            )
            voucher_coupon.save()
            return redirect('index')  # Redirect to a success page or wherever you want
        else:
            return HttpResponse("Missing required fields", status=400)

    return render(request, 'add_voucher_coupon.html')



# crud for voucher coupons /////////////////

def coupon_list(request):
    coupons_list = VoucherCoupon.objects.all()
    paginator = Paginator(coupons_list, 10)  # Show 10 coupons per page
    page = request.GET.get('page')
    
    try:
        coupons = paginator.page(page)
    except PageNotAnInteger:
        coupons = paginator.page(1)
    except EmptyPage:
        coupons = paginator.page(paginator.num_pages)

    return render(request, 'coupons_list.html', {'coupons': coupons})


def edit_voucher_coupon(request, pk):
    voucher = get_object_or_404(VoucherCoupon, pk=pk)
    
    if request.method == 'POST':
        voucher.coupon_name = request.POST.get('coupon_name')
        voucher.coupon_description = request.POST.get('coupon_description')
        voucher.coupon_price = request.POST.get('coupon_price')
        voucher.coupon_button_link = request.POST.get('coupon_button_link')
        voucher.save()
        return redirect('coupon_list')  # Redirect to the list view

    return render(request, 'edit_coupons.html', {'voucher': voucher})

def delete_voucher_coupon(request, pk):
    # Get the voucher associated with the given primary key
    voucher = get_object_or_404(VoucherCoupon, pk=pk)

    if request.method == 'POST':
        # Delete the voucher if the request method is POST
        voucher.delete()
        return redirect('coupon_list')  # Redirect to the list view after deletion

    # For GET requests, just redirect to the voucher list without deleting anything
    return redirect('coupon_list')

