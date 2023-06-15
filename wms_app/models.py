from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Role can be WasteProducer, WasteCollector, FeesCollector
    role = models.CharField(max_length=20)  
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    def __str__(self):
        return self.username

    
# WasteProducer model
class WasteProducer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# WasteCollector model
class WasteCollector(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.fname


# models.py
class Payment(models.Model):
    waste_producer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    payment_type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Payment by {self.waste_producer} on {self.payment_date}"

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    request_count = models.IntegerField(default=0)
    montly = models.BooleanField(default=False)

# area model
class Area(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Collection model
class Collection(models.Model):
    waste_producer = models.ForeignKey(User, on_delete=models.CASCADE)
    waste_collector = models.ForeignKey(Customer, on_delete=models.CASCADE)
    collection_date = models.DateField()
    collection_status = models.BooleanField(default=False)
    time_requested = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey('Area', on_delete=models.CASCADE)

    def __str__(self):
        return f"Collection for {self.waste_producer} by {self.waste_collector}"
