from django.shortcuts import render
from .models import *

# project landing page
def landing_view(request):
    return render(request, 'landing/index.html', {})


# login page
def login_view(request):
    return render(request, 'dashboard/login.html', {})


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
        customer = Customer(user=user, role=role, address=address, longitude=longitude, latitude=latitude, contact_number=contact_number)
        customer.save()

        # Redirect to success page or home page
        return redirect('/login') 

    return render(request, 'dashboard/register.html') 