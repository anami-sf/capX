from django.contrib import admin
from django.contrib.auth.models import User
from .models import Order, Transaction, Wallet
# Register your models here.
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Wallet)
