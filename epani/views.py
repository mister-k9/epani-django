from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import Account

from epani.models import Machine, Card, Order, Cluster


from .serializers import MachineSerializer


# Create your views here.


def epani(request):

    filter = (request.GET['filter']).upper()

    if request.user.is_admin:
        machines_count = (Machine.objects.all()).count()
        if not filter == 'ALL':
            machines = Machine.objects.filter(machine_status=filter)
        else:
            machines = Machine.objects.all()

        machines_offline = Machine.objects.filter(machine_status='OFFLINE')
        machines_online = Machine.objects.filter(machine_status='ONLINE')

        context = {
            'machines': machines,
            'machines_count': machines_count,
            'machines_offline': machines_offline.count(),
            'machines_online': machines_online.count(),
            'filter': filter
        }

        return render(request, 'epani/machines.html', context)

    elif request.user.is_cluster:
        clus_id = request.user.cluster_id
        clus = Cluster.objects.get(id=clus_id)

        temp = list(clus.machines.split('|'))
        cluster_machines = [x for x in temp if x != '']
        macs = []
        for id in cluster_machines:
            temp = {}
            machine = Machine.objects.get(machine_id=id)
            temp['machine_id'] = machine.machine_id
            temp['machine_token'] = machine.machine_token
            temp['machine_status'] = machine.machine_status
            temp['machine_location'] = machine.machine_location
            temp['user'] = machine.user
            temp['cards_count'] = machine.cards_count()

            macs.append(temp)
        print(macs)

        context= {
            'machines': macs,
        }
        return render(request, 'epani/machines.html', context)
    
    else:
        HttpResponse('Invalid Request')


def cards(request):
    filter = (request.GET['filter']).upper()
    machine_id = request.GET['machine_id']

    try:
        machine = Machine.objects.get(machine_id=machine_id)
        if not request.user.id == machine.user.id and not request.user.is_admin and not request.user.is_cluster and not request.user.is_user:
            return HttpResponse("Invalid Request")
    except:
        pass

    active_url = request.path + f'?machine_id={machine_id}' + f'&filter=active'
    inactive_url = request.path + \
        f'?machine_id={machine_id}' + f'&filter=inactive'
    blocked_url = request.path + \
        f'?machine_id={machine_id}' + f'&filter=blocked'
   
    if request.user.is_admin:

        cards = Card.objects.filter(card_status=filter)

        active_cards_count = (Card.objects.filter(card_status='ACTIVE')).count()
        inactive_cards_count = (Card.objects.filter(card_status='INACTIVE')).count()
        blocked_cards_count = (Card.objects.filter(card_status='BLOCKED')).count()

        context = {
            'cards': cards,
            'active_cards_count': active_cards_count,
            'inactive_cards_count': inactive_cards_count,
            'blocked_cards_count': blocked_cards_count,
            'filter': filter,
            'inactive_url': inactive_url,
            'active_url': active_url,
            'blocked_url': blocked_url

        }

        return render(request, 'epani/cards.html', context)

    cards = Card.objects.filter(machine_id=machine_id, card_status=filter)

    active_cards_count = (Card.objects.filter(
        machine_id=machine_id, card_status='ACTIVE')).count()
    inactive_cards_count = (Card.objects.filter(
        machine_id=machine_id, card_status='INACTIVE')).count()
    blocked_cards_count = (Card.objects.filter(
        machine_id=machine_id, card_status='BLOCKED')).count()

    context = {
        'cards': cards,
        'active_cards_count': active_cards_count,
        'inactive_cards_count': inactive_cards_count,
        'blocked_cards_count': blocked_cards_count,
        'filter': filter,
        'active_url': active_url,
        'inactive_url': inactive_url,
        'blocked_url': blocked_url,
        'machine_id': machine_id
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
    print(card_number)

    if request.method == 'POST':

        card.holder_name = request.POST['holder-name']
        card.card_status = request.POST['card-status']
        if card.balance < int(request.POST['balance']):
            card.last_recharge_amount = int(request.POST['balance']) - card.balance
        card.balance = request.POST['balance']
        card.save()

        return redirect('/')

    card_status_choices = ['ACTIVE', 'INACTIVE', 'BLOCKED']
    for choice in card_status_choices:
        if choice == card.card_status:
            card_status_choices.remove(choice)

    print(card_status_choices)
    context = {
        'card': card,
        'card_status_choices': card_status_choices
    }

    return render(request, 'epani/edit_card.html', context)


def users(request):
    filter = request.GET['filter']
    if request.user.is_admin:
        if filter == 'machine':
            users = Account.objects.filter(is_user=True, is_superadmin=False)
        elif filter == 'cluster':
            users = Account.objects.filter(is_cluster=True, is_superadmin=False)

        machine_users_count = (Account.objects.filter(is_user=True, is_superadmin=False)).count()
        cluster_users_count = (Account.objects.filter(is_cluster=True, is_superadmin=False)).count()

        context = {
            'users': users,
            'machine_users_count':machine_users_count,
            'cluster_users_count':cluster_users_count,
            'filter':filter.upper()

        }

        return render(request, 'accounts/users.html', context)


def edit_machine(request):
    mac_id = request.GET['machine_id']

    mac = Machine.objects.get(machine_id=mac_id)

    excluding_mac_user_users = []
    users = Account.objects.filter(is_user=True, is_superadmin=False)
    if mac.user:
        for user in users:
            if user == mac.user:
                continue
            else:
                excluding_mac_user_users.append(user)

    if request.method == 'POST':

        user_id = request.POST['user-select']
        user = Account.objects.get(id=user_id)

        mac.user = user
        mac.machine_id = request.POST['machine-id']
        mac.machine_token = request.POST['machine-token']
        mac.machine_status = request.POST['machine-status']
        mac.machine_location = request.POST['machine-location']
        mac.save()

        return redirect('/')

    context = {
        'machine': mac,
        'users': users,
        'excluding_mac_user_users': excluding_mac_user_users
    }
    return render(request, 'epani/edit_machine.html', context)


def edit_user(request):

    id = request.GET['id']
    usr = Account.objects.get(id=id)

    macs = Machine.objects.all()
    excluding_user_mac_macs = []
    if usr.machine_id:
        for mac in macs:
            if mac == usr.machine_id: continue
            excluding_user_mac_macs.append(mac)

    clusts = Cluster.objects.all()
    excluding_user_c_cs = []

    clust_name = ""
    if usr.cluster_id:
        clust_name = Cluster.objects.get(id=usr.cluster_id)
        for clust in clusts:
            if clust.id == usr.cluster_id:continue
            excluding_user_c_cs.append(clust)

    print(excluding_user_c_cs)

    if request.method == 'POST':

        usr.first_name = request.POST['first-name']
        usr.last_name = request.POST['last-name']
        # usr.email = request.POST['email']
        usr.phone_number = request.POST['phone-number']
        if usr.is_user:
            usr.machine_id = request.POST['machine-id']
        if usr.is_cluster:
            usr.cluster_id = request.POST['cluster-id']
        usr.save()

        return redirect('/')

    context = {
        'usr': usr,
        'excluding_user_mac_macs': excluding_user_mac_macs,
        'excluding_user_c_cs':excluding_user_c_cs,
        'clusters':clusts,
        'machines':macs,
        'clust_name':clust_name
    }

    return render(request, 'accounts/edit_user.html', context)


def clusters(request):
    if request.user.is_admin:
        clusters = Cluster.objects.all()
    
        context= {
            'clusters':clusters,
            'clusters_count':clusters.count(),
        }
        return render(request, 'epani/clusters.html',context)


def new_cluster(request):
    users = Account.objects.filter(is_cluster=True, is_superadmin=False)

    if request.method == 'POST':
        user_id = request.POST['user-select']
        
        cluster = Cluster()
        if user_id:
            user = Account.objects.get(id=user_id)
            cluster.user = user
        cluster.name = request.POST['name']
        try:
            cluster.save()

        except Exception as e:
            return HttpResponse(e)

        return redirect('/')
    
    context = {
        'users':users
    }

    return render(request, 'epani/new_cluster.html',context)

def edit_cluster(request):
    c_id = request.GET['id']

    cluster = Cluster.objects.get(id=c_id)

    excluding_c_user_users = []
    users = Account.objects.filter(is_cluster=True, is_superadmin=False)
    if cluster.user:
        for user in users:
            if user == cluster.user:
                continue
            else:
                excluding_c_user_users.append(user)

    if request.method == 'POST':
        user_id = request.POST['user-select']
        user = Account.objects.get(id=user_id)

        cluster.user = user
        cluster.name = request.POST['name']
        
        cluster.save()

        return redirect('/')

    context = {
        'cluster': cluster,
        'users': users,
        'excluding_c_user_users': excluding_c_user_users
    }
    return render(request, 'epani/edit_cluster.html', context)


def cluster(request):
    c_id = request.GET['id']
    cluster = Cluster.objects.get(id=c_id)
    temp = list(cluster.machines.split('|'))
    cluster_machines = [x for x in temp if x != '']
    macs = []
    for id in cluster_machines:
        temp = {}
        machine = Machine.objects.get(machine_id=id)
        temp['machine_id'] = machine.machine_id
        temp['machine_token'] = machine.machine_token
        temp['machine_status'] = machine.machine_status
        temp['machine_location'] = machine.machine_location
        temp['user'] = machine.user
        temp['cards_count'] = machine.cards_count()

        macs.append(temp)
    print(macs)

    
    # is_assigned option into machines model
    mac_ids = []
    machines = Machine.objects.all()
    for machine in machines:
        if machine.machine_id in cluster_machines:continue
        mac_ids.append(machine.machine_id)

    if request.method == "POST":
        mac = request.POST['machine-select']
        cluster.machines += f"{mac}|"
        cluster.save()

        return redirect(f'/epani/cluster/?id={cluster.id}')
    
    context = {
        'cluster':cluster,
        'mac_ids':mac_ids,
        'macs':macs
    }

    return render(request, 'epani/cluster.html',context)
