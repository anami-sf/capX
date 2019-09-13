from django.db import models
from django.urls import reverse 


ORDER_TYPE_CHOICES = [
    ('Bid', 'Bid'),
    ('Ask', 'Ask')
]

ORDER_COIN_CHOICES = [
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum')

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
    # transaction = models.ForeignKey // 
