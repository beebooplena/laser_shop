from django.db import models


class Item(models.Model):
    """
    Item model. Inspired from
    the boutique ado project, code institute.
    """
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    engraved = models.CharField(default=None, max_length=35, null=True,
                                blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    discount_value = models.DecimalField(max_digits=6, decimal_places=2,
                                         blank=True,
                                         null=True, default=0)
    discount = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Category model
    inspired from
    the boutique ado project, code institute
    """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
