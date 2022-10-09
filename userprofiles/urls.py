from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('history_order/<ordering_number>', views.history_order,
         name='history_order'),
]