from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderingLineItem

@receiver(post_save, sender=OrderingLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update ordering total on lineitem update/create
    Borrowed this code from code institute, boutique ado project
    """
    instance.ordering.update_sum()

@receiver(post_delete, sender=OrderingLineItem)
def delete_on_save(sender, instance, **kwargs):
    """
    Update ordering sum on lineitem delete
    Borrowed this code from code institute, boutique ado project
    """
    instance.ordering.update_sum()