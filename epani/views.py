from django.http import HttpResponse
from django.shortcuts import redirect, render

from epani.models import Machine, Card, Order


from .serializers import MachineSerializer


# Create your views here.


def epani(request):

    filter = (request.GET['filter']).upper()

    if request.user.is_admin:
        if not filter == 'ALL':
            machines = Machine.objects.filter(machine_status=filter)
        else:
            machines = Machine.objects.all()

        machines_offline = Machine.objects.filter(machine_status='OFFLINE')
        machines_online = Machine.objects.filter(machine_status='ONLINE')

        context = {
            'machines': machines,
            'machines_count': machines.count(),
            'machines_offline': machines_offline.count(),
            'machines_online': machines_online.count(),
            'filter': filter
        }

        return render(request, 'epani/machines.html', context)

    if not filter == 'ALL':
        machines = Machine.objects.filter(
            user=request.user, machine_status=filter)
    else:
        machines = Machine.objects.filter(user=request.user)

    machines_offline = Machine.objects.filter(
        machine_status='OFFLINE', user=request.user)
    machines_online = Machine.objects.filter(
        machine_status='ONLINE', user=request.user)

    context = {
        'machines': machines,
        'machines_count': machines.count(),
        'machines_offline': machines_offline.count(),
        'machines_online': machines_online.count(),
        'filter': filter
    }

    return render(request, 'epani/machines.html', context)


def cards(request):
    filter = (request.GET['filter']).upper()
    machine_id = request.GET['machine_id']

    active_url = request.path + f'?machine_id={machine_id}'+ f'&filter=active'
    inactive_url = request.path + f'?machine_id={machine_id}'+ f'&filter=inactive'

    if request.user.is_admin:
        if not filter == 'ALL':
            cards = Card.objects.filter(card_status=filter)
        else:
            cards = Card.objects.all()

        cards_active = Card.objects.filter(card_status='ACTIVE')
        cards_inactive = Card.objects.filter(card_status='INACTIVE')

        context = {
            'cards': cards,
            'cards_count': cards.count(),
            'cards_inactive': cards_inactive.count(),
            'cards_active': cards_active.count(),
            'filter': filter,
            'inactive_url':inactive_url,
            'active_url':active_url,

        }

        return render(request, 'epani/cards.html', context)

    if not filter == 'ALL':
            cards = Card.objects.filter(machine_id=machine_id,card_status=filter)
    else:
            cards = Card.objects.filter(machine_id=machine_id)

    cards_active = Card.objects.filter(machine_id=machine_id,card_status='ACTIVE')
    cards_inactive = Card.objects.filter(machine_id=machine_id,card_status='INACTIVE')



    context = {
        'cards': cards,
        'cards_count':cards.count(),
        'cards_inactive':cards_inactive.count(),
        'cards_active':cards_active.count(),
        'filter': filter,
        'active_url':active_url,
        'inactive_url':inactive_url,
        'machine_id':machine_id
    }

    return render(request, 'epani/cards.html', context)


def orders(request):

    card_number = request.GET['card_number']
    orders = Order.objects.all().filter(card_number=card_number)

    context = {
        'orders': orders,
    }

    return render(request, 'epani/orders.html', context)


def order(request):

    if request.method == 'POST':
        order = Order()

        order.order_id = request.POST['order_id']
        order.card_number = request.POST['card_number']
        order.machine_id = request.POST['machine_id']
        order.amount = request.POST['amount']
        order.volume_in_ml = request.POST['volume_in_ml']
        order.order_status = request.POST['order_status']
        order.sync_status = request.POST['sync_status']
        order.local_timestamp = request.POST['local_timestamp']

        try:
            order.save()
        except Exception as e:
            return HttpResponse(e)

        return redirect('/')

    return render(request, 'epani/order.html')


def card(request):

    if request.method == 'POST':
        card = Card()

        card.holder_name = request.POST['holder_name']
        card.card_number = request.POST['card_number']
        card.machine_id = request.POST['machine_id']
        card.balance = request.POST['balance']

        try:

            card.save()

        except Exception as e:
            return HttpResponse(e)

        return redirect('/')

    return render(request, 'epani/card.html')



def machine(request):

    if request.method == 'POST':
        machine = Machine()
        machine.user = request.user
        machine.machine_location = request.POST['machine_location']
        machine.machine_status = request.POST['machine_status']
        machine.machine_id = request.POST['machine_id']
        machine.machine_token = request.POST['machine_token']

        try:

            machine.save()

        except Exception as e:
            return HttpResponse(e)

        return redirect('/')

    return render(request, 'epani/machine.html')


def edit_card(request):

    card_number = request.GET['card_number']

    card = Card.objects.get(card_number=card_number)

    if request.method == 'POST':
        
        card.holder_name = request.POST['holder_name']
        card.balance = request.POST['balance']
        card.save()

        return redirect('/')

    context = {
        'card':card
    }

    return render(request, 'epani/edit_card.html', context)


