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
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed')
]







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
        default = 'Pending'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.id})
    
class Transaction(models.Model):
    # bid_id = models.OneToOneField(
    #     Order,
    #     on_delete=models.CASCADE,
    #     primary_key = True
    # )
    # ask_id = models.OneToOneField(
    #     Order,
    #     on_delete=models.CASCADE,
    #     primary_key = True
    # )
    bid = models.CharField(max_length=200)
    ask = models.CharField(max_length=200)