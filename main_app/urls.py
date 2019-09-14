from django.contrib.auth.models import User
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.OrderList.as_view(), name='order_index'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    path('orders/create/', views.OrderCreate.as_view(), name='order_create'),
    path('accounts/signup', views.signup, name='signup'),
    
    # path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]