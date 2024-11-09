from django.db import models

# Create your models here.
class customer_register_table(models.Model):
    full_name=models.CharField(max_length=100)
    email_id=models.EmailField()
    phone_number=models.CharField(max_length=15)
    deposit_amount=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    account_number=models.CharField(max_length=100)
    registered_dt=models.CharField(max_length=100)
    
class bank_statment_table(models.Model):
    full_name=models.CharField(max_length=100)
    account_number=models.CharField(max_length=100)
    deposit_number=models.CharField(max_length=100)
    withdraw_amount=models.CharField(max_length=100)
    registered_dt=models.CharField(max_length=100)
    balance_amount=models.CharField(max_length=100)
    
    
    
    
