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


def home(request):
    return render (request,'home.html')

def account(request):
    user= request.user
    user_id=user.id
    return user_details(request, user_id)



def wallet_details(request, user_id):
    user_wallet = Wallet.objects.get(user=user_id)
    print(user_wallet.eth_balance)
    return

def user_details(request, user_id):
    open_orders = User.objects.get(id = user_id).order_set.filter(status='Open')
    print(open_orders)
    filled_orders = User.objects.get(id = user_id).order_set.filter(status='Filled')
    user = User.objects.get(id = user_id)
    # all_orders = User.order_set.all()
    # orders = all_orders.objects.filter(user = user)
    # open_orders = orders.objects.filter(status='Open')
    # filled_orders = orders.objects.filter(status='Filled')

# def create_transaction(request, bid_order, ask_order):
#     transaction = Transaction.objects.create(bid = bid_order, ask = ask_order)



def order_execute(request, pk):
    order = Order.objects.get(id=pk)
    orders = Order.objects.all()
    if order.order_type == "Bid":
        bid_order = order
        for first_order in orders:
            if first_order.order_type == "Ask" and (first_order.amount == order.amount):
                ask_order = first_order
                break
       # if ask_order == 
    else:
        ask_order = order      
        for first_order in orders:
            if first_order.order_type == "Bid" and (first_order.amount == order.amount):
                bid_order = first_order
                break
    if ask_order and bid_order:
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
    

class OrderCreate(LoginRequiredMixin,CreateView):
    model = Order
    fields = ['amount', 'order_type', 'coin_type']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user
        
        # Instance methods are invoked by prefacing the 
        #method name with 'super()'
        return super().form_valid(form)

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
    print(open_orders)
    filled_orders = User.objects.get(id = user_id).order_set.filter(status='Filled')
    user = User.objects.get(id = user_id)
    # all_orders = User.order_set.all()
    # orders = all_orders.objects.filter(user = user)
    # open_orders = orders.objects.filter(status='Open')
    # filled_orders = orders.objects.filter(status='Filled')
    wallet = Wallet.objects.get(id=user_id)
    
    return render(request,'users/details.html', {
        'user': user,
        'wallet': wallet,
        'open_orders': open_orders,
        'filled_orders': filled_orders
    })