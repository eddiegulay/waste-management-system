from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_view, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
]