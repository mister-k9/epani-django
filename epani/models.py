
from operator import mod
from django.db import models

from accounts.models import Account

# Create your models here.
class Order(models.Model):
    ORDER_STATUS = (
        ('DONE_PAYMENT', 'DONE_PAYMENT'),
        ('DISPENSED', 'DISPENSED'),
    )
    SYNC_STATUS = (
        ('SYNCED', 'SYNCED'),
        ('NOT_SYNCED', 'NOT_SYNCED'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=50, unique=True)
    machine_id = models.CharField(max_length=50)
    card_number = models.CharField(max_length=27)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS)
    amount = models.IntegerField()
    volume_in_ml = models.FloatField()
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS)
    local_timestamp = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

class Card(models.Model):
    CARD_STATUS = (
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    )
    card_number = models.CharField(max_length=27,unique=True)
    card_status = models.CharField(max_length=27,choices=CARD_STATUS,default='ACTIVE')
    # machine_id = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    machine_id = models.CharField(max_length=50,default='0')
    holder_name = models.CharField(max_length=50)
    balance = models.IntegerField()
    last_recharge_amount = models.IntegerField(blank=True, null=True)
    last_txn_volume = models.FloatField(blank=True, null=True)
    last_txn_status = models.CharField(max_length=20, blank=True, null=True)
    last_txn_timestamp = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.card_number

    def orders_count(self):
        return (Order.objects.all().filter(card_number=self.card_number)).count()

class Machine(models.Model):
    STATUS = (
        ('OFFLINE', 'OFFLINE'),
        ('ONLINE', 'ONLINE'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    machine_id = models.CharField(max_length=50, unique=True)
    machine_status = models.CharField(max_length=20, choices=STATUS)
    machine_location = models.CharField(max_length=100)
    machine_token = models.CharField(max_length=100,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.machine_id

    def cards_count(self):
        return (Card.objects.all().filter(machine_id=self.machine_id)).count()

# class User(models.Model):
#     machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)





