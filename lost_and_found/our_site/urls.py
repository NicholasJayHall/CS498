from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/<int:pk>/found/', views.mark_found, name='mark_found'),
    path('items/<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('report/', views.report_item, name='report_item'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('subscribe/', views.subscribe_email, name='subscribe_email'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
]
