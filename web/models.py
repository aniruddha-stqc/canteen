from datetime import datetime
from django.db import models

# Thali model
class Thali(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    price = models.IntegerField()
    long_name = models.TextField(blank=True)

    def __str__(self):
        return self.short_name

# Extra model
class Extra(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=20)
    long_name = models.TextField(max_length=20)
    price = models.IntegerField()

    def __str__(self):
        return self.short_name

class Category(models.Model):
    category_id = models.CharField(max_length=10, primary_key=True)  # Make category_id a manually entered field
    category_name = models.CharField(max_length=100)  # Increased max length for category name

    def __str__(self):
        return self.category_name

class Customer(models.Model):
    mobile = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Wallet(models.Model):
    mobile = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='mobile', related_name='wallets')
    transaction_time = models.CharField(max_length=100, default=datetime.now().strftime('%Y%m%d%H%M%S'))
    transaction = models.CharField(max_length=50)
    credit = models.IntegerField(default=0)
    debit = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    class Meta:
        unique_together = ('mobile', 'transaction_time')

    def __str__(self):
        return f"Wallet ({self.mobile}, {self.transaction_time}): Balance = {self.balance}"

# Order model
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=100, default=datetime.now().strftime('%Y%m%d%H%M%S'))
    concession_category = models.CharField(max_length=4, blank=True, null=True)
    customer_mobile = models.CharField(max_length=10, blank=True, null=True)
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    pay_mode = models.CharField(max_length=4, null=True)
    thali_type = models.CharField(max_length=20, blank=True, null=True)
    thali_type_name = models.CharField(max_length=20, blank=True, null=True)
    extra_item1 = models.CharField(max_length=20, blank=True, null=True)
    extra_item1_name = models.CharField(max_length=20, blank=True, null=True)
    extra_item2 = models.CharField(max_length=20, blank=True, null=True)
    extra_item2_name = models.CharField(max_length=20, blank=True, null=True)
    extra_item3 = models.CharField(max_length=20, blank=True, null=True)
    extra_item3_name = models.CharField(max_length=20, blank=True, null=True)
    extra_item4 = models.CharField(max_length=20, blank=True, null=True)
    extra_item4_name = models.CharField(max_length=20, blank=True, null=True)
    total_price = models.IntegerField()

    def __str__(self):
        return f"Order ID: {self.order_id}, Customer: {self.customer_name}, Total Price: {self.total_price}"
