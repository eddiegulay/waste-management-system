from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)  # Role can be WasteProducer, WasteCollector, FeesCollector

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# FeesCollector model
class FeesCollector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Collection model
class Collection(models.Model):
    waste_producer = models.ForeignKey(WasteProducer, on_delete=models.CASCADE)
    waste_collector = models.ForeignKey(WasteCollector, on_delete=models.CASCADE)
    collection_date = models.DateField()

    def __str__(self):
        return f"Collection for {self.waste_producer.name} by {self.waste_collector.name}"


# Payment model
class Payment(models.Model):
    waste_producer = models.ForeignKey(WasteProducer, on_delete=models.CASCADE)
    fees_collector = models.ForeignKey(FeesCollector, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Payment by {self.waste_producer.name} to {self.fees_collector.name}"
