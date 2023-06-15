from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_view, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('sign_out/', logout_view, name='sign_out'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('addresses/', address_view, name='addresses'),
    path('customers/', customer_view, name='customers'),
    path('collector/', collector_view, name='collector'),
]