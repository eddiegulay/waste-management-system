from django.urls import path
from .views import *

urlspatterns = [
    path('', landing_view, name='index'),
]