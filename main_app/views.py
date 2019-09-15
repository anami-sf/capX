from django.urls import reverse
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Order


def home(request):
    return render (request,'home.html')


def order_execute(request, pk):
    order = Order.objects.get(id=pk)
    orders = Order.objects.all()
    if order.order_type == "Bid":
        bid_order = order
        for first_order in orders:
            if first_order.order_type == "Ask":
                ask_order = first_order
                break
       # if ask_order == 
    else:
        ask_order = order      
        for first_order in orders:
            if first_order.order_type == "Bid":
                bid_order = first_order
                break
    if ask_order and bid_order:
        return render(
            request, 
            'transactions/transaction.html/', 
            {'ask_order': ask_order, 
            'bid_order': bid_order}
        )
    else:
        return render(
            request, 
            'transactions/transaction.html/', 
            {'error': 'Unable to execute your order at this time'}
        )       


class OrderList(ListView):
    model = Order

class OrderDetail(DetailView):
    model = Order
    

class OrderCreate(CreateView):
    model = Order
    fields = ['amount', 'order_type', 'coin_type']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user
        # Instance methods are invoked by prefacing the 
        #method name with 'super()'
        return super().form_valid(form)

class OrderDelete(DeleteView):
    model = Order
    success_url = '/orders/'



class OrderUpdate(UpdateView):
    model = Order
    fields = ['amount', 'order_type', 'coin_type']




def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
        # This will add the user to the database
            user = form.save()
        # This is how we log a user in via code
            login(request, user)
            return redirect('home')
    else:
        error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

