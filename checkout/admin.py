from django.contrib import admin
from .models import Ordering, OrderingLineItem

# Register your models here.

class OrderingLineItemAdminInline(admin.TabularInline):
    model = OrderingLineItem
    readonly_fields = ('lineitem_sum',)

class OrderingAdmin(admin.ModelAdmin):

    inlines = (OrderingLineItemAdminInline,)

    readonly_fields = (
        'ordering_number', 'time',
        'delivery_payment', 'ordering_total',
        'sum_total', 'original_bag',
        'stripe_pid',)
        
    fields = (
        'ordering_number', 'time', 'full_name', 'email',
        'mobile_number', 'country',
        'zip_code', 'city', 'street_address', 'delivery_payment',
        'discount', 'ordering_total', 'sum_total',
        'original_bag','stripe_pid',)

    list_display = ('ordering_number', 'time', 'full_name',
                    'ordering_total', 'delivery_payment',
                    'sum_total',)
    
    ordering = ('-time',)

admin.site.register(Ordering, OrderingAdmin)
