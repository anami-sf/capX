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

@login_required
def account(request):
    # user= request.user
    # user_id=user.id
    # return user_details(request, user_id)
    user_id = request.user.id
    return user_details(request)
    

########################################

def order_execute(request, pk):
    order = Order.objects.get(id=pk) 
    orders = Order.objects.all()    
    wallet = Wallet.objects.get(user = request.user.id)
    other_wallet = Wallet.objects.get(user = order.user) 

    if order.order_type == "Bid" and order.status == "Open":
        bid_order = order
        for order in orders:
            if order.order_type == "Ask" and (order.amount == bid_order.amount) and order.user.id != bid_order.user.id:
                ask_order = order
                break
    elif order.order_type == "Ask" and order.status == "Open":
        ask_order = order      
        for order in orders:
            if order.order_type == "Bid" and (order.amount == ask_order.amount) and order.user.id != ask_order.user.id:
                bid_order = order
                break
    
    #We need an else here to render error page
    if ask_order and bid_order:
        transaction = Transaction.objects.create_transaction(bid_order.id, ask_order.id)
        if order.order_type == "Ask": #other wallet bid/buy for eth+
            #btc balance for other wallet was already adjusted down
            wallet.btc_balance = wallet.btc_balance + order.amount
            wallet.save()
            other_wallet.eth_balance = other_wallet.eth_balance + order.amount
            other_wallet.save()
        if order.order_type == "Bid": #other wallet ask/sell for eth -
            wallet.eth_balance = wallet.eth_balance + order.amount
            wallet.save()
            other_wallet.btc_balance = other_wallet.eth_balance + order.amount
            other_wallet.save()
        
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


def order_index(request):
    order_list=Order.objects.all()
    return render(request, 'orders/index.html', {'order_list': order_list})

def order_details(request, order_id):
    order = Order.objects.get(id = order_id)
    return render(request, 'orders/details.html', {'order':order})

@login_required
def order_create(request):
    wallet = Wallet.objects.get(user = request.user.id)
    print(f'>>>>{wallet}>>>')
    if request.method == "POST":
        form = OrderForm(request.POST)
        order_amount = Decimal(request.POST['amount'])
        order_order_type = request.POST['order_type']  ####### Take the user's input
        order_coin = request.POST['coin_type']
        if wallet.eth_balance - order_amount < 0 and order_order_type =='Ask' and order_coin =='ETH' or wallet.btc_balance - order_amount < 0 and order_order_type =='Bid' and order_coin =='ETH':
            return redirect('/orders/create/')
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            print(f'>>>>>{order.user}')  
            if order_order_type =='Ask' and order_coin =='ETH':
                wallet.eth_balance = (wallet.eth_balance - order.amount)
            elif order_order_type =='Bid' and order_coin =='ETH':
                wallet.btc_balance = (wallet.btc_balance - order.amount)
            order.save()
            wallet.save()
            return redirect('order_detail', pk=order.pk)
    else:
         form = OrderForm()
    return render(request, 'main_app/order_form.html', {'form':form})

@login_required
def order_delete(request, order_id):
    user_id = request.user.id
    order = Order.objects.get(id=order_id)
    wallet = Wallet.objects.get(user = request.user)
    if order.order_type == 'Bid' and order.user.id == user_id:
        wallet.btc_balance = (wallet.btc_balance + order.amount)
    elif order.order_type == 'Ask' and order.user.id == user_id:
        wallet.eth_balance = (wallet.eth_balance + order.amount)
    else:
        return redirect('/orders')
        # render or redirect to proper error message/route
    wallet.save()
    order.delete()
    order.save()
    return redirect('/orders')
   
    


    
    


@login_required
def order_update(request,order_id):
    order= Order.objects.get(id = order_id)
    wallet = Wallet.objects.get(user = request.user.id)
    before_order_id = order.id
    before_order_amount = order.amount
    print(f'>>>> BEFORE order ID{before_order_id}>>>')
    print(f'>>>> BEFORE order submission{order.amount}>>>')
    print(f'>>>>{wallet}>>>')


    if request.method == "POST":
        form = OrderForm(request.POST)
        print(f'>>>>>POST {request.POST}')  
        order_amount = Decimal(request.POST['amount'])
        print(f'>>>>>ORDER_amount{order_amount}')  
        order_order_type = request.POST['order_type']
        order_coin = request.POST['coin_type']
        if wallet.eth_balance - order_amount < 0 and order_order_type =='Ask' and order_coin =='ETH' or wallet.btc_balance - order_amount < 0 and order_order_type =='Bid' and order_coin =='ETH':
            return redirect('/orders/create/')
        if form.is_valid():
            print(f'>>>>>ORDER .id{order.id}')  
            order = form.save(commit=False)
            order.user = request.user
            order.id = before_order_id
            print(f'>>>>>ORDER _id{order_id}')  
            print(f'>>>>>ORDER .id{order.id}')  
            print(f'>>>>>ORDER _AMOUNT{order_amount}')  
            print(f'>>>>>ORDER.AMOUNT{order.amount}')  
            if order_order_type =='Ask' and order_coin =='ETH':
                wallet.eth_balance = (wallet.eth_balance + before_order_amount)
                print(f'>>>>>>WALLET ETH BALANCE:{wallet.eth_balance} <<<<')
                wallet.eth_balance = (wallet.eth_balance - order_amount)
            if order_order_type =='Bid' and order_coin =='ETH':
                wallet.btc_balance = (wallet.btc_balance + before_order_amount)
                print(f'>>>>>>WALLET ETH BALANCE:{before_order_amount} <<<<')
                wallet.btc_balance = (wallet.btc_balance - order_amount)
            wallet.save()
            order.save()
            return redirect('order_detail', order_id=order.id)
    else:
         form = OrderForm()
    return render(request, 'main_app/order_form.html', {'form':form})
    

# class OrderUpdate(LoginRequiredMixin,UpdateView):
#     model = Order
#     fields = ['amount', 'order_type', 'coin_type']


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
            print('>>>>>>request.user:', request.user)
            wallet = Wallet.objects.create_wallet(request.user)
            return redirect('/users/account/')
    else:
        error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    
    return render(request, 'registration/signup.html', context)


@login_required
def user_details(request):
    user_id = request.user.id
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
    # else:
    #     return redirect('/orders')
        
    