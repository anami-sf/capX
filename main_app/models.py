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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # transaction = models.ForeignKey // 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.id})

    
