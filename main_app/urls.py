from django.contrib.auth.models import User
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('orders/', views.order_index, name='order_index'),
    path('orders/<int:order_id>/', views.OrderDetail.as_view(), name='order_detail'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/update/', views.order_update, name='order_update'),
    path('orders/<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('accounts/signup', views.signup, name='signup'),
    path('orders/<int:order_id>/execute/', views.order_execute, name='order_execute'),
    path('users/', views.user_details, name='user_detail'),
    path('users/account/', views.account, name='account'),
   
    # path('wallets/<int:user_id>/', views.wallet_details, name='wallet_details')
# path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]