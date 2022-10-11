from django.contrib import admin
from .models import Item, Category


class ItemAdmin(admin.ModelAdmin):
    """
    ItemAdmin model
    """
    list_display = (
        'sku',
        'category',
        'name',
        'engraved',
        'price',
        'discount',
        'discount_value',
        'image',

    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin model
    """
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
