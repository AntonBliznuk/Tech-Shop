from django.db import models
from main.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    user_phone = models.IntegerField(blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.product} -> ({self.ordered_at}) [{self.is_complete}]"
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['ordered_at']
