from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, WasteProducer, WasteCollector, Collection, Payment, Area, Account

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'address','contact_number')

class WasteProducerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'contact_number')

class WasteCollectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('waste_producer', 'waste_collector', 'collection_date')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('waste_producer', 'payment_date', 'amount')

class AreaAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'request_count', 'montly')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(WasteProducer, WasteProducerAdmin)
admin.site.register(WasteCollector, WasteCollectorAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Account, AccountAdmin)
