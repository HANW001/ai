from django.db import models

class Order(models.Model):
    idx = models.CharField(primary_key=True, max_length=255)
    order_mall = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    order_date = models.DateField()
    order_name = models.CharField(max_length=255)
    order_options = models.CharField(max_length=45)
    order_price = models.CharField(max_length=45)
    order_option_price = models.CharField(max_length=45, blank=True, null=True)
    order_count = models.CharField(max_length=45)
    order_person = models.CharField(max_length=45)
    order_address = models.CharField(max_length=45)
    order_phone = models.CharField(max_length=45)
    order_delivery = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'orders'