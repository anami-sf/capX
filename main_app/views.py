from django.urls import reverse
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction, Order, Wallet
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderForm
from decimal import Decimal


def home(request):
    return render (request,'home.html')

def account(request):
    user= request.user
    user_id=user.id
    return user_details(request, user_id)
    
    

def order_execute(request, pk):
    user_id = request.user.id
    order = Order.objects.get(id=pk)
    orders = Order.objects.all()
    wallet = Wallet.objects.get(user = user_id)
    if order.order_type == "Bid":
        bid_order = order
        for first_order in orders:
            if first_order.order_type == "Ask" and (first_order.amount == order.amount) and first_order.user != bid_order.user:
                ask_order = first_order
                break
    else:
        ask_order = order      
        for first_order in orders:
            if first_order.order_type == "Bid" and (first_order.amount == order.amount)  and first_order.user != ask_order.user:
                bid_order = first_order
                break
    if ask_order and bid_order:
        print(ask_order)
        # create_transaction(request, bid_order, ask_order)
        transaction = Transaction.objects.create_transaction(bid_order.id, ask_order.id)

        return render(
            request, 
            'transactions/transaction.html/', 
            {'ask_order': ask_order, 
            'bid_order': bid_order,
            'transaction': transaction}
        )
    else:
        return render(
            request, 
            'transactions/transaction.html/', 
            {'error': 'Unable to execute your order at this time'}
        )       




class OrderList(ListView):
    model = Order

class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    

# class OrderCreate(LoginRequiredMixin,CreateView):
#     model = Order
#     fields = ['amount', 'order_type', 'coin_type']
    
#     def check_balances(self)


#     def form_valid(self, form):
#         # Assign the logged in user (self.request.user)
#         form.instance.user = self.request.user
#         # Instance methods are invoked by prefacing the 
#         #method name with 'super()'
#         return super().form_valid(form)

def order_create(request):
    wallet = Wallet.objects.get(user = request.user.id)
    print(f'>>>>{wallet}>>>')
    if request.method == "POST":
        form = OrderForm(request.POST)
        order_amount = Decimal(request.POST['amount'])
        order_order_type = request.POST['order_type']
        order_coin = request.POST['coin_type']
        if wallet.eth_balance - order_amount < 0 and order_order_type =='Ask' and order_coin =='ETH' or wallet.btc_balance - order_amount < 0 and order_order_type =='Bid' and order_coin =='ETH':
            return redirect('/orders/create/')
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            print(f'>>>>>{order.user}')  
            if order_order_type =='Ask' and order_coin =='ETH':
                wallet.eth_balance = (wallet.eth_balance - order_amount)
            elif order_order_type =='Bid' and order_coin =='ETH':
                wallet.btc_balance = (wallet.btc_balance - order.amount)
            order.save()
            wallet.save()
            return redirect('order_detail', pk=order.pk)
            print(order.pk)
    else:
         form = OrderForm()
    return render(request, 'main_app/order_form.html', {'form':form})

class OrderDelete(LoginRequiredMixin,DeleteView):
    model = Order
    success_url = '/orders/'



class OrderUpdate(LoginRequiredMixin,UpdateView):
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



def user_details(request, user_id):
    open_orders = User.objects.get(id = user_id).order_set.filter(status='Open')
    
    filled_orders = User.objects.get(id = user_id).order_set.filter(status='Filled')
    user = User.objects.get(id = user_id)
    # all_orders = User.order_set.all()
    # orders = all_orders.objects.filter(user = user)
    # open_orders = orders.objects.filter(status='Open')
    # filled_orders = orders.objects.filter(status='Filled')
    wallet = Wallet.objects.get(user=user_id)
    
    return render(request,'users/details.html', {
        'user': user,
        'wallet': wallet,
        'open_orders': open_orders,
        'filled_orders': filled_orders
    })