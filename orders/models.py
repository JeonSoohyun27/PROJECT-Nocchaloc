from django.db       import models

from users.models    import User
from products.models import Product, Option

class Cart(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    option   = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'carts'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_status'

class ItemStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'item_status'

class Order(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'orders'

class OrderItems(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_status = models.ForeignKey(ItemStatus, on_delete=models.SET_NULL, null=True)
    order       = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    option      = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'order_items'