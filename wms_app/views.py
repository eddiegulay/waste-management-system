from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import *

# project landing page
def landing_view(request):
    return render(request, 'landing/index.html', {})

# login view
def login_view(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        user = authenticate(request, username=mobile, password=password)
        if user is not None:
            login(request, user)
            # get user status
            if user.is_superuser:
                return redirect('/dashboard')
            else:
                # get customer with user_id
                customer = Customer.objects.get(user=user)
                if int(customer.role) == 1:
                    # waste producer
                    return redirect('/producer_dashboard')
                else:
                    # waste collector
                    return redirect('/collector_dashboard')
                      
        else:
            # Invalid login credentials
            error_message = "Invalid mobile number or password"
            return render(request, 'dashboard/login.html', {'error_message': error_message})
    

    return render(request, 'dashboard/login.html')

#logout view
def logout_view(request):
    logout(request)
    return redirect('/') 

# Register View
def register_view(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        
        password = request.POST['pwd1']
        role = request.POST['role']
        address = request.POST['address']
        contact_number = request.POST['mobile']
        username = contact_number

        # Create User
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        
        # Create Customer
        customer = Customer(user=user, role=role, address=address, contact_number=contact_number)
        customer.save()

        # Redirect to success page or home page
        return redirect('/login') 

    areas = Area.objects.all()

    return render(request, 'dashboard/register.html', {'areas': areas}) 


# Dashboard View
def dashboard_view(request):
    return render(request, 'dashboard/admin.html')

def address_view(request):
    areas = Area.objects.all()
    area_data = []
    for area in areas:
        customers_count = Customer.objects.filter(address=area.id).count()
        area_data.append({'area': area, 'customer_count': customers_count})

    return render(request, 'dashboard/address.html', {'area_data': area_data})
    

# Customer View
def customer_view(request):
    customers = Customer.objects.filter(role=1)
    customer_data = []
    for customer in customers:
        address_id = customer.address
        try:
            address = Area.objects.get(pk=address_id)
            address_name = address.name
        except Area.DoesNotExist:
            address_name = ''

        data = {
            'first_name': customer.user.first_name,
            'mobile': customer.contact_number,
            'role': customer.role,
            'address_name': address_name,
        }
        customer_data.append(data)

    context = {'customer_data': customer_data}
    return render(request, 'dashboard/customer.html', context)

# collectors View
def collector_view(request):
    customers = Customer.objects.filter(role=2)
    customer_data = []
    for customer in customers:
        address_id = customer.address
        try:
            address = Area.objects.get(pk=address_id)
            address_name = address.name
        except Area.DoesNotExist:
            address_name = ''

        data = {
            'first_name': customer.user.first_name,
            'mobile': customer.contact_number,
            'role': customer.role,
            'address_name': address_name,
        }
        customer_data.append(data)

    context = {'customer_data': customer_data}
    return render(request, 'dashboard/collector.html', context)