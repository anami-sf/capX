from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def home(request):
    return render (request,'home.html')

def order_index(request):
    return render (request,'orders/index.html')

def order_detail(request):
    return render (request,'orders/detail.html')


