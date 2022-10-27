from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_blog, name='blog'),
    path('blog_post/<int:pk>/', views.blog_post, name='blog_post'),
    path('add/', views.adding_post, name='adding_post'),
    path('edit/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('delete/<int:pk>/', views.delete_blog, name='delete_blog'),
]
