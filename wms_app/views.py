from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
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
            return redirect('/dashboard')  
        else:
            # Invalid login credentials
            error_message = "Invalid mobile number or password"
            return render(request, 'dashboard/login.html', {'error_message': error_message})
    

    return render(request, 'dashboard/login.html')

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

    return render(request, 'dashboard/register.html') 


# Dashboard View
def dashboard_view(request):
    return render(request, 'dashboard/admin.html')