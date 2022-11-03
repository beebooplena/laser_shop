from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomerProfile(models.Model):
    """
    A customer profile model for updating or creating
    profile information and order history.
    inspired from
    the boutique ado project, code institute
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_mobile_number = models.CharField(max_length=25,
                                             null=True, blank=True)
    default_country = models.CharField(max_length=45, null=True, blank=True)
    default_zip_code = models.CharField(max_length=25, null=True, blank=True)
    default_city = models.CharField(max_length=50, null=True, blank=True)
    default_street_address = models.CharField(max_length=100,
                                              null=True, blank=True)
    web_site = models.CharField(max_length=260, null=True, blank=True)
    want_wishes = models.TextField(max_length=260,
                                   blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    """
    Update or create the customer profile
    This function is borrowed from code institute
    from the boutique Ado project.
    """
    if created:
        CustomerProfile.objects.create(user=instance)
        #users that exist: only save the profile
        instance.customerprofile.save()
