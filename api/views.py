from django.http import HttpResponse, JsonResponse
import json
from datetime import datetime
from django.forms.models import model_to_dict
from epani.models import Card, Order, Machine
from epani.serializers import CardSerializer, OrderSerializer, MachineSerializer
from rest_framework import generics, permissions, authentication

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.views import View

from random import randint

@api_view(["GET"])
def deduct_card_balance(request):
    if request.method == 'GET':
        card_num = request.GET['cno']
        amount = int(request.GET['am'])
        txn_stmp = request.GET['txn_ts']
        mid = request.GET['mid']
        mtoken = request.GET['mtoken']
        try:
            machine = Machine.objects.get(machine_id=mid)
            if not mtoken == machine.machine_token:
                return Response('Invalid Request!')
            
            card = Card.objects.get(card_number=card_num)
            if not card.card_status == 'ACTIVE':
                return Response('Invalid Card')
            if card.balance >= amount:
                f_bal = card.balance - amount
                card.balance = f_bal
                card.last_txn_timestamp = txn_stmp
                card.save()
                return Response({'balance':card.balance,'name':card.holder_name})
            else:
                return Response({'balance':card.balance,'name':card.holder_name})
        
        except Exception as e:
            print(e)
            if 'Machine' in str(e):
                return Response('Invalid Machine')
            if 'Card' in str(e):
                return Response('Invalid Card')
            


@api_view(["GET","POST"])
def get_cards(request):
    if request.method == 'GET': 
        mid = request.GET['mid']
        mtoken = request.GET['mtoken']
        try:
            machine = Machine.objects.get(machine_id=mid)
            if not mtoken == machine.machine_token:
                return Response('Invalid Request!')
            
            cards = Card.objects.filter(machine_id=machine.machine_id)
            if cards:
                serializer = CardSerializer(cards, many=True)
                return Response(serializer.data)
            else:
                return Response('No cards')
        except Exception as e:
            #print(e)
            if 'Machine' in str(e):
                return Response('Invalid Machine')


    if request.method == 'POST':
        json_data = json.loads(request.body) 
        cards = json_data['data']
        for local_card_data in cards:
            instance = Card.objects.get(card_number=local_card_data['card_number'])
            online_card_data = (CardSerializer(instance)).data
            if online_card_data['last_txn_timestamp']:
                onl_datetime = datetime.strptime(((online_card_data['last_txn_timestamp'].split('.'))[0]), "%Y-%m-%d %H:%M:%S")
                loc_datetime = datetime.strptime(((local_card_data['last_txn_timestamp'].split('.'))[0]), "%Y-%m-%d %H:%M:%S")
                if loc_datetime > onl_datetime:
                    instance.balance = local_card_data['balance']
                    instance.last_txn_volume = local_card_data['last_txn_volume']
                    instance.last_txn_status = local_card_data['last_txn_status']
                    instance.last_txn_timestamp = local_card_data['last_txn_timestamp']
                    instance.save()
                   
                # IF ONLINE DB > LOCAL DB UPDATE LOCAL DB
                # IF TRANSACTION DONE ON OTHER MACHINE
                
            
        
        return Response('POSTED')


@api_view(["POST"])
def create_order(request):
    
    if request.method == 'POST':
        mid = request.GET['mid']
        mtoken = request.GET['mtoken']
        json_data = json.loads(request.body)
    
        try:
            machine = Machine.objects.get(machine_id=mid)
            if not mtoken == machine.machine_token:
                return Response('Invalid Request!')
        except Exception as e:
            #print(e)
            if 'Machine' in str(e):
                return Response('Invalid Machine')

        value = randint(0, 1000000)

        order = Order()
        order.order_id = value
        order.machine_id = mid
        order.card_number = json_data['card_number']
        order.order_status = json_data['order_status']
        order.amount = json_data['amount']
        order.volume_in_ml = json_data['volume_in_ml']
        order.sync_status = 'SYNCED'
        order.local_timestamp = json_data['local_timestamp']
        order.save()

        return Response('Successful!')

        
            
            
        


