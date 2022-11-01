from rest_framework import serializers

from .models import Card, Order, Machine


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'card_number',
            'machine_id',
            'holder_name',
            'balance',
            'last_recharge_amount',
            'last_txn_volume',
            'last_txn_status',
            'created_at',
            'updated_at'
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'order_id',
            'machine_id',
            'card_number',
            'order_status',
            'amount',
            'volume_in_ml',
            'sync_status',
            'local_timestamp',
            'created_at',
            'updated_at',
        ]


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = [
            'machine_id',
            'machine_status',
            'machine_location',
            'created_at',
            'updated_at',
        ]