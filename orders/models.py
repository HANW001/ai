from django.db import models

class Order(models.Model):
    cafe24_order_id = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    buyer_name = models.CharField(max_length=255)
    buyer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
