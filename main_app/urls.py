from django.contrib.auth.models import User
from django.urls import path
from . import views

urlpatterns = {
    path('', views.home, name='home'),
}