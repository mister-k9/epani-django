from celery import shared_task
from time import sleep
from epani.models import Order, Card
from datetime import datetime


@shared_task
def sleepy(duration):
    sleep(duration)
   
    return None


@shared_task
def celery_create_order(order_details):
    order = Order()
    order.order_id = order_details['order_id']
    order.machine_id = order_details['mid']
    order.card_number = order_details['cno']
    order.order_status = order_details['order_status']
    order.amount = order_details['am']
    order.volume_in_ml = order_details['volume']
    order.sync_status = order_details['sync_status']
    order.local_timestamp = order_details['timestamp']
    order.save()

    return None
    