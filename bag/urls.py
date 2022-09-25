from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_bag, name='show_bag'),
    path('add/<item_id>/', views.add_item_to_bag, name='add_item_to_bag'),
    path('remove_bag/<item_id>/', views.remove_bag, name='remove_bag'),
    path('update_bag/<item_id>/', views.update_bag, name='update_bag'),
    
]
