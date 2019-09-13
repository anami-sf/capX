from django.contrib.auth.models import User
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.order_index, name='order_index'),
    path('accounts/signup', views.signup, name='signup'),
    
    # path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]