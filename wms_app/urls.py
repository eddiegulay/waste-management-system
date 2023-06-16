from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_view, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('sign_out/', logout_view, name='sign_out'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('addresses/', address_view, name='addresses'),
    path('collections_payments/', collections_payments_view, name='collections_payments'),
    path('customers/', customer_view, name='customers'),
    path('collector/', collector_view, name='collector'),
    path('producer_dashboard', producer_dashboard_view, name='producer_dashboard'),
    path('request/', request_pickup_view, name='request_pickup'),
    path('make_payments/', make_payment_view, name='payments'),
    path('collector_dashboard/', collector_dashboard_view, name='collector_dashboard'),
]