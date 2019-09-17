from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



ORDER_TYPE_CHOICES = [
    ('Bid', 'Bid'),
    ('Ask', 'Ask')
]

ORDER_COIN_CHOICES = [
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum')

]

ORDER_STATUS_CHOICES = [
    ('Open', 'Open'),
    ('Filled', 'Filled')
]

# class Transaction(models.Model):
#     # bid_id = models.OneToOneField(
#     #     Order,
#     #     on_delete=models.CASCADE,
#     #     primary_key = True
#     # )
#     # ask_id = models.OneToOneField(
#     #     Order,
#     #     on_delete=models.CASCADE,
#     #     primary_key = True
#     # )
#     bid = models.CharField(max_length=200)
#     ask = models.CharField(max_length=200)

##### Create Transaction
class TransactionManager(models.Manager):
    def create_transaction(self, bid_order, ask_order):
        transaction = self.create(bid_order = bid_order, ask_order = ask_order)
        # do something with the book
        b = Order.objects.get(id=bid_order)
        a = Order.objects.get(id=ask_order)
        b.status = 'Filled'
        a.status = 'Filled'
        b.transaction = transaction
        a.transaction = transaction
        b.save()
        a.save()
        return transaction

class Transaction(models.Model):
    bid_order = models.CharField(max_length=100)
    ask_order = models.CharField(max_length=100)

    objects = TransactionManager()

    

class Order(models.Model):
    amount= models.DecimalField(
        max_digits=30,
        decimal_places = 8
    )
    order_type= models.CharField(
        max_length = 3,
        choices = ORDER_TYPE_CHOICES,

    )
    coin_type= models.CharField(
        max_length = 3,
        choices = ORDER_COIN_CHOICES,
       
    )

    status = models.CharField(
        max_length =  9,
        choices = ORDER_STATUS_CHOICES,
        default = 'Open'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.id})
    
