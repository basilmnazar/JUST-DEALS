from django.shortcuts import render,redirect
from django.contrib import messages
from deal_app.models import*
from django.shortcuts import render, get_object_or_404
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login


def vendor_register(request):
    if request.method == 'POST':
        # Extract form data from POST request
        vendor_name = request.POST.get('fname')
        vendor_type = request.POST.get('vendor_type')
        point_of_contact = request.POST.get('point_of_contact')
        phone = request.POST.get('phone')
        terms = request.POST.get('terms')
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Extract new form fields
        account_holder_name = request.POST.get('account_holder_name')
        bank_name = request.POST.get('bank_name')
        branch = request.POST.get('branch')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')
        commission_percentage = request.POST.get('commission_percentage')

        # Handle file upload
        image = request.FILES.get('image')

        # Validate that passwords match
        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return render(request, 'vendor_register.html', {
                'temp_unique_id': uuid.uuid4().hex[:8].upper(),
                'choices': Vendor.VENDOR_TYPE_CHOICES
            })

        # Validate commission percentage
        try:
            if commission_percentage:
                commission_percentage = float(commission_percentage)
                if commission_percentage < 0 or commission_percentage > 100:
                    raise ValueError("Commission percentage must be between 0 and 100.")
            else:
                commission_percentage = 0.00
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'vendor_register.html', {
                'temp_unique_id': uuid.uuid4().hex[:8].upper(),
                'choices': Vendor.VENDOR_TYPE_CHOICES
            })

        # Check if the username already exists
        if Vendor.objects.filter(uname=uname).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'vendor_register.html', {
                'temp_unique_id': uuid.uuid4().hex[:8].upper(),
                'choices': Vendor.VENDOR_TYPE_CHOICES
            })

        # Create a new vendor instance
        vendor = Vendor(
            fname=vendor_name,
            vendor_type=vendor_type,
            point_of_contact=point_of_contact,
            phone=phone,
            terms=terms,
            image=image,
            uname=uname
        )
        vendor.set_password(password)
        vendor.account_holder_name = account_holder_name
        vendor.bank_name = bank_name
        vendor.branch = branch
        vendor.account_number = account_number
        vendor.ifsc_code = ifsc_code
        vendor.commission_percentage = commission_percentage

        # Save the vendor to the database
        vendor.save()

        # Capture the unique ID
        unique_id = vendor.pk

        # Pass the unique ID to the success page
        messages.success(request, f"Vendor registered successfully. Your unique ID is {unique_id}.")
        return redirect('vendor_login')  # Redirect to login page

    else:
        temp_unique_id = uuid.uuid4().hex[:8].upper()

    return render(request, 'vendor_register.html', {
        'temp_unique_id': temp_unique_id,
        'choices': Vendor.VENDOR_TYPE_CHOICES
    })
def admin_vendors(request):
    # Fetch all vendors from the database
    vendors = Vendor.objects.all()
    
    return render(request, 'admin_vendors.html', {
        'vendors': vendors,
    })

def vendor_dashboard(request):
    # Check if vendor_id is set in session
    vendor_id = request.session.get('vendor_id')
    
    if not vendor_id:
        messages.error(request, "You need to log in to access the dashboard.")
        return redirect('vendor_login')  # Redirect to login page

    try:
        # Fetch the logged-in vendor
        logged_in_vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        messages.error(request, "Vendor not found.")
        return redirect('vendor_login')  # Redirect to login page
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        logged_in_vendor = None

    # Fetch dealers related to the logged-in vendor
    dealers = Dealers.objects.filter(vendor=logged_in_vendor)

    return render(request, 'vendor_dashboard.html', {
        'logged_in_vendor': logged_in_vendor,  # Pass the logged-in vendor details to the template
        'dealers': dealers,  # Pass the list of dealers to the template
    })

def vendor_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')

        try:
            vendor = Vendor.objects.get(uname=uname)
            if vendor.check_password(password):
                # Login successful, set the session
                request.session['vendor_id'] = vendor.id
                messages.success(request, "Login successful!")
                return redirect('vendor_dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, "Invalid username or password.")
        except Vendor.DoesNotExist:
            messages.error(request, "Invalid username or password.")

    return render(request, 'vendor_login.html')



def vendor_detail(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    return render(request, 'vendor_dashboard.html', {'vendor': vendor})



# def vendor_redirect(request, id):
#     # Fetch the vendor to ensure it exists
#     vendor = get_object_or_404(Vendor, pk=id)
    
#     # Redirect to the index page with the vendor ID as a query parameter
#     return redirect(f'/index/?vendor_id={id}')

def admin_detail(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    return render(request, 'admin_vendors.html', {'vendor': vendor})