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
import time

# importing celery tasks
from .celery_tasks import *

@api_view(["POST"])
def deduct_card_balance(request):
    if request.method == 'POST':
        json_data=json.loads(request.body)
        mid = json_data['mid']
        mtoken = json_data['mtoken']
        
        try:
            machine = Machine.objects.get(machine_id=mid)
            if not mtoken == machine.machine_token:
                return Response('Invalid Request!')
            
            card = Card.objects.get(card_number=json_data['cno'])
            if not card.card_status == 'ACTIVE':
                return Response('Invalid Card')
            if card.balance >=  json_data['am']:
                value = randint(0, 1000000)
                order_status = 'DONE_PAYMENT'
                order_details = {
                    'order_id':value,
                    'mid': mid,
                    'cno':json_data['cno'],
                    'order_status':order_status,
                    'am':json_data['am'],
                    'volume':json_data['volume_in_ml'],
                    'sync_status':'SYNCED',
                    'timestamp':json_data['txn_ts']
                }
                celery_create_order(order_details)

                f_bal = card.balance -  json_data['am']
                card.balance = f_bal
                card.last_txn_timestamp = json_data['txn_ts']
                card.save()
                
                return Response({'balance':card.balance,'name':card.holder_name,'order_created':True})
            else:
                sleepy(10)
                return Response({'balance':card.balance,'name':card.holder_name,'order_created':False})
        
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




        
            
            
        


