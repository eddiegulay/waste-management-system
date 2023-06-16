from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import *
import datetime
import requests

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

# Area View
def address_view(request):
    areas = Area.objects.all()
    area_data = []
    for area in areas:
        customers_count = Customer.objects.filter(address=area.id, role='1').count()
        area_data.append({'area': area, 'customer_count': customers_count})

    return render(request, 'dashboard/address.html', {'area_data': area_data})
    
# Customer collections and payments view
def collections_payments_view(request):
    collections = Collection.objects.all()
    payments = Payment.objects.all()

    context = {'collections': collections, 'payments': payments}
    return render(request, 'dashboard/collections_payments.html', context)

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

        # subtract 5000 from account balance
        account.balance = account.balance - 5000
        if account.request_count >=1:
            account.request_count -= 1
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

# collector dashboard view
def collector_dashboard_view(request):
    greetings = get_greeting() + request.user.first_name
    collector = Customer.objects.get(user=request.user)
    collections = Collection.objects.filter(waste_collector=collector, collection_status=False)
    collections_count = len(collections)
    if collections_count == 0:
        collections = False
    complete_collections = Collection.objects.filter(waste_collector=collector, collection_status=True)

    collector_area = Area.objects.get(id=collector.address)
    collector_area_name = collector_area.name
    


    context = {'greetings': greetings, 'collections': collections, 'collection_count': collections_count, 'complete_collections': complete_collections, 'collector_area_name': collector_area_name}
    return render(request, 'dashboard/collector_dashboard.html', context)



def get_coordinates(area_name):
    geocoding_url = f"https://nominatim.openstreetmap.org/search?format=json&q={area_name}"
    response = requests.get(geocoding_url)
    data = response.json()

    if data:
        latitude = float(data[0]['lat'])
        longitude = float(data[0]['lon'])
        return latitude, longitude

    return -6.7924,39.2083




# process collection
def process_request_view(request, id):
    greetings = get_greeting() + request.user.first_name
    collection = Collection.objects.get(id=id)
    customer_id = collection.waste_producer.id
    user = User.objects.get(id=customer_id)
    customer = Customer.objects.get(user=user)
    account = Account.objects.get(user=user)
    collection_date = datetime.date.today()
    collector_account = Account.objects.get(user=request.user)
    customer_collector = Customer.objects.get(user=user)
    all_collector_collections = Collection.objects.filter(waste_collector=customer_collector, collection_status=False)

    area = Area.objects.get(id=customer.address)
    


    if request.method == 'POST':
        collection.collection_status = True
        collection.collection_date = collection_date
        collection.save()

        # add 5000 to collector account balance
        collector_account.balance = account.balance + 5000
        collector_account.save()

        return redirect('/collector_dashboard')

    context = {'greetings': greetings, 'collection': collection, 'customer': customer, 'account': account, 'map_link': '', 'all_collector_collections': len(all_collector_collections), 'area': area}

    return render(request, 'dashboard/process_requests.html', context)
