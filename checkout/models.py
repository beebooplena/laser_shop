import uuid


from django.db import models
from django.db.models import Sum

from django.conf import settings
from items.models import Item


class Ordering(models.Model):
    ordering_number = models.CharField(
        max_length=32, null=False, editable=False
        )
    full_name = models.CharField(max_length=60, null=False, blank=False)
    email = models.EmailField(max_length=260, null=False, blank=False)
    mobile_number = models.CharField(max_length=25, null=False, blank=False)
    country = models.CharField(max_length=45, null=False, blank=False)
    zip_code = models.CharField(max_length=25, null=True, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    street_address = models.CharField(max_length=100, null=False, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    delivery_payment = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
        )
    discount = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
        )
    ordering_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    sum_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_ordering_number(self):
        """
        Generate and make a random ordering number using UUID
        This code is borrowed from code institute from the boutique ado project
        """
        return uuid.uuid4().hex.upper()
   
    def update_sum(self):
        """
        Update sum_total everytime a line item is added,
        accounting for discount and delivery cost.
        """
        self.ordering_total = self.lineitems.aggregate(
            Sum('lineitem_sum'))['lineitem_sum__sum'] or 0
        self.delivery_payment = settings.STANDARD_DELIVERY_PRICE
        if Item.discount_value is True:
            Item.discount_value = self.discount
        else:
            self.discount = 0
        self.sum_total = (
            self.ordering_total + self.delivery_payment - self.discount)
        self.save()

   
    def save(self, *args, **kwargs):
        """
        If a ordering number does not exist before,
        it will override the original save method and
        set an ordering number
        This code is borrowed from code institute from the boutique ado project
        """
        if not self.ordering_number:
            self.ordering_number = self._generate_ordering_number()
        super().save(*args, **kwargs)

   
    def __str__(self):
        return self.ordering_number

class OrderingLineItem(models.Model):
    ordering = models.ForeignKey(
        Ordering, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems')
    item = models.ForeignKey(Item, null=False, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, blank=False, default=0)
    name_engraved = models.CharField(max_length=40, null=True, blank=True)
    lineitem_sum = models.DecimalField(
        max_digits=6, decimal_places=2, null=False,
        blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method and
        set lineitem sum and update the ordering total.
        This code is borrowed from code institute from the boutique ado project
        """

        self.lineitem_sum = self.item.price * self.amount
        super().save(*args, **kwargs)
   

    def __str__(self):
        return f'SKU {self.item.sku} on ordering {self.ordering.ordering_number}'