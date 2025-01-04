from datetime import datetime
from django.utils import timezone  # Import timezone for correct date/time handling
# Create your models here.
from django.db import models

class Thali(models.Model):
    # Define the columns for the table
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    category = models.CharField(max_length=20)  # Category of thali
    short_name = models.CharField(max_length=20)  # Renamed from 'name' to 'short_name'
    price = models.IntegerField()  # Price as a whole number (integer)
    long_name = models.TextField(blank=True)  # Renamed from 'description' to 'long_name'

    def __str__(self):
        return self.short_name  # Return the short_name as the string representation of the object

class Extra(models.Model):
    # Define the columns for the 'extra' table
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    short_name = models.CharField(max_length=20)  # Short name for the sidedish
    long_name = models.TextField(max_length=20)  # Long description for the sidedish
    price = models.IntegerField()  # Price as a whole number (integer)

    def __str__(self):
        return self.short_name  # Return the short_name as the string representation of the object

class Customer(models.Model):
    # Define the columns for the customer table
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=15)  # Full name of the customer
    mobile = models.CharField(max_length=10, blank=True, null=True)  # Mobile number (can be blank)
    email = models.EmailField(blank=True, null=True)  # Email field (can be blank)


    def __str__(self):
        return self.name  # Return the long_name as the string representation of the object

class Concession(models.Model):
    # Define the columns for the concession table
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    category = models.CharField(max_length=4)  # Category field
    category_name = models.CharField(max_length=10)  # Category name field

    def __str__(self):
        return f"Category: {self.category}, Name: {self.category_name}"



class Wallet(models.Model):
    # Define the columns for the wallet table
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    transaction_time = models.CharField(max_length=100, default=datetime.now().strftime('%Y%m%d%H%M%S'))  # Time of the transaction (auto-set to current time)
    mobile = models.CharField(max_length=10, null=True)  # Mobile number, should be unique
    transaction = models.CharField(max_length=50)  # Transaction details, can be any text (e.g., transaction ID)
    credit = models.IntegerField(default=0)  # Credit amount (whole number)
    debit = models.IntegerField(default=0)  # Debit amount (whole number)
    balance = models.IntegerField(default=0)  # Balance in the wallet (calculated as credit - debit)

    def __str__(self):
        return f"Wallet ({self.mobile}): Balance = {self.balance}"

class Order(models.Model):
    # Define the columns for the order table
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    order_id = models.CharField(max_length=100, default=datetime.now().strftime('%Y%m%d%H%M%S'))  # Order ID (timestamp)

    # Directly store the customer details (no foreign keys)
    concession_category = models.CharField(max_length=4, blank=True, null=True)  # Concession category (directly stored as a char field)
    customer_mobile = models.CharField(max_length=10, blank=True, null=True)  # Customer mobile number (directly stored)
    customer_name = models.CharField(max_length=200, blank=True, null=True)  # Customer name (directly stored)
    pay_mode = models.CharField(max_length=4, null=True )  # Payment mode (e.g., "CASH", "BILL", "FREE", "WALL", etc.)
    thali_type = models.CharField(max_length=20, blank=True, null=True)  # Thali type (stored as a char field)
    thali_type_name = models.CharField(max_length=20, blank=True, null=True)  # Thali type (stored as a char field)

    # Optional Extra items (stored as short names)
    extra_item1 = models.CharField(max_length=20, blank=True, null=True)  # Extra item 1 (short name)
    extra_item1_name = models.CharField(max_length=20, blank=True, null=True)
    extra_item2 = models.CharField(max_length=20, blank=True, null=True)  # Extra item 2 (short name)
    extra_item2_name = models.CharField(max_length=20, blank=True, null=True)
    extra_item3 = models.CharField(max_length=20, blank=True, null=True)  # Extra item 3 (short name)
    extra_item3_name = models.CharField(max_length=20, blank=True, null=True)
    extra_item4 = models.CharField(max_length=20, blank=True, null=True)  # Extra item 4 (short name)
    extra_item4_name = models.CharField(max_length=20, blank=True, null=True)  # Extra item 1 (short name)

    total_price = models.IntegerField()  # Total price for the order

    def __str__(self):
        return f"Order ID: {self.order_id}, Customer: {self.customer_name}, Total Price: {self.total_price}"