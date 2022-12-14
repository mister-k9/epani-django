from django.contrib import admin
from .models import Card, Order, Machine, Cluster

# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'balance']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'card_number', 'volume_in_ml']

class ClusterAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']


class MachineAdmin(admin.ModelAdmin):
    list_display = ['machine_id', 'machine_status']

admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Order, OrderAdmin)



