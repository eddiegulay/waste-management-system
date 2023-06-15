from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import *
import datetime

def get_greeting():
    current_hour = datetime.datetime.now().hour

    if 0 <= current_hour < 12:
        return "Good morning "
    elif 12 <= current_hour < 18:
        return "Good afternoon "
    else:
        return "Good evening "

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

        # create account
        account = Account(user=user)
        account.save()

        # Redirect to success page or home page
        return redirect('/login') 

    areas = Area.objects.all()

    return render(request, 'dashboard/register.html', {'areas': areas}) 

# function to get customers in an area
def get_customers_per_area(area_id):
    adr = str(area_id)
    customers = Customer.objects.filter(address=adr, role='1')
    return customers

def get_collectors_per_area(area_id):
    adr = str(area_id)
    customers = Customer.objects.filter(address=adr, role='2')
    return customers

def get_requests_per_area(area_id):
    adr = Area.objects.get(id = area_id)
    collections = Collection.objects.filter(area=adr)
    return collections


# Dashboard View
def dashboard_view(request):
    context = {}
    areas = Area.objects.all()
    context['areas'] = areas
    area_data_list = []
    for area in areas:
        area_data = {}

        area_name = area.name
        area_requests = len (get_requests_per_area(area.id))
        customers_in_area = len (get_customers_per_area(area.id))
        progress = 0
        if customers_in_area != 0:
            progress = (area_requests/customers_in_area) * 100
            progress = int(progress)
        f_progress = f"{progress} %"

        color = 'success'
        if progress > 25 and progress <= 50:
            color = 'info'
        elif progress > 50 and progress <= 75:
            color = 'warning'
        elif progress > 75:
            color = 'danger'

        area_data['name'] = area_name
        area_data['customers'] = customers_in_area
        area_data['requests'] = area_requests
        area_data['progress'] = f_progress
        area_data['counter'] = progress
        area_data['color'] = color

        area_data_list.append(area_data)
    context['area_data'] = area_data_list

    context['collectors'] = len(Customer.objects.filter(role='2'))
    context['collections'] = len(Collection.objects.all())
    context['customers'] = len(Customer.objects.filter(role='1'))

    return render(request, 'dashboard/admin.html', context)


def address_view(request):
    areas = Area.objects.all()
    area_data = []
    for area in areas:
        customers_count = Customer.objects.filter(address=area.id, role='1').count()
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


# Producer Dashboard View
def producer_dashboard_view(request):
    greetings = get_greeting() + request.user.first_name
    payments = Payment.objects.filter(waste_producer=request.user)
    collections = Collection.objects.filter(waste_producer=request.user)
    if len(collections) == 0:
        collections = False

    if len(payments) == 0:
        payments = False

    context = {'greetings': greetings, 'payments': payments, 'collections': collections}
    return render(request, 'dashboard/producer.html', context)

# function to get customers in an area
def get_waste_collector(area_id):
    adr = str(area_id)
    collector = Customer.objects.filter(address=adr, role='2').order_by('id').first()
    return collector


def request_pickup_view(request):
    customer = Customer.objects.get(user = request.user)
    account = Account.objects.get(user = request.user)

    if request.method == 'POST':
        waste_producer = request.user
        waste_collector = get_waste_collector(customer.address)
        collection_date = None
        area = Area.objects.get(id=customer.address)
        waste_type = request.POST.get('waste-type')
        house_number = request.POST.get('hno')
        bin_number = request.POST.get('bno')

        collection = Collection(
            waste_producer=waste_producer,
            waste_collector=waste_collector,
            collection_date=collection_date,
            area=area,
            waste_type=waste_type,
            house_number=house_number,
            bin_number=bin_number
        )
        collection.save()

        # substract 5000 from account balance
        account.balance = account.balance - 5000
        account.save()

        return redirect('/producer_dashboard')


    context = {'customer': customer, 'account': account}
    return render(request, 'dashboard/request.html', context)


# make payment view
def make_payment_view(request):
    customer = Customer.objects.get(user = request.user)
    account = Account.objects.get(user = request.user)
    context = {
        'customer': customer,
        'account': account
    }

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        payment_type = request.POST.get('payment_type')


        payment = Payment(
            waste_producer=request.user,
            payment_date=datetime.date.today(),
            amount=float(amount),
            status=False,
            phone_number=phone_number,
            payment_method=payment_method,
            payment_type=payment_type
        )
        payment.save()

        # add balance in account to associated customer
        acc = Account.objects.get(user=request.user)
        acc.balance += int(amount)
        if int(payment_type) == 1:
            acc.montly = True
        else:
            acc.montly = False
            counts = int(acc.balance/5000)
            acc.request_count = counts
        acc.save()

        return redirect('/producer_dashboard')



    return render(request, 'dashboard/payment.html', context)


def save_collection(request):
    if request.method == 'POST':
        waste_producer = request.user
        waste_collector = get_waste_collector()
        collection_date = request.POST.get('collection_date')
        area = request.POST.get('area')
        waste_type = request.POST.get('waste-type')
        house_number = request.POST.get('hno')
        bin_number = request.POST.get('bno')

        collection = Collection(
            waste_producer=waste_producer,
            waste_collector=waste_collector,
            collection_date=collection_date,
            area=area,
            waste_type=waste_type,
            house_number=house_number,
            bin_number=bin_number
        )
        collection.save()

        # Optionally, you can redirect the user to a success page
        return render(request, 'success.html')

    return render(request, 'collection_form.html')


