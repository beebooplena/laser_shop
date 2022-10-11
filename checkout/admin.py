from django.contrib import admin
from .models import Ordering, OrderingLineItem


class OrderingLineItemAdminInline(admin.TabularInline):

    """
    OrderingAdmin model, code credited to code institute
    from the boutique Ado project
    """
    model = OrderingLineItem
    readonly_fields = ('lineitem_sum',)


class OrderingAdmin(admin.ModelAdmin):
    """
    OrderingAdmin model, code credited to code institute
    from the boutique Ado project
    """

    inlines = (OrderingLineItemAdminInline,)

    readonly_fields = (
        'ordering_number', 'time',
        'delivery_payment', 'ordering_total',
        'sum_total', 'original_bag',
        'stripe_pid',)

    fields = (
        'ordering_number', 'customer_profile', 'time', 'full_name', 'email',
        'mobile_number', 'country',
        'zip_code', 'city', 'street_address', 'delivery_payment',
        'discount', 'ordering_total', 'sum_total',
        'original_bag', 'stripe_pid',)

    list_display = ('ordering_number', 'time', 'full_name',
                    'ordering_total', 'delivery_payment',
                    'sum_total',)

    ordering = ('-time',)


admin.site.register(Ordering, OrderingAdmin)
