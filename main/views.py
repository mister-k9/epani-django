
from django.shortcuts import render
from epani.models import Order
from django.contrib.auth.decorators import login_required
from epani.models import Machine

@login_required(login_url='login')
def home(request):
    if request.user.is_admin:
        machines = Machine.objects.all()
        machines_offline = Machine.objects.all().filter(machine_status='OFFLINE')
        machines_online = Machine.objects.all().filter(machine_status='ONLINE')

        orders = Order.objects.all()

        total_income = 0
        total_volume = 0.0
        for order in orders:
            total_income += order.amount
            total_volume += order.volume_in_ml

        total_volume_in_l = total_volume / 1000
    
        context = {
            'machines_count': machines.count(),
            'machines_offline':machines_offline.count(),
            'machines_online':machines_online.count(),

            'orders_count':orders.count(),
            'total_volume':int(total_volume_in_l),
            'total_income':total_income,
        }
        return render(request, 'dashboard.html', context)

    machines = Machine.objects.filter(user=request.user)
    machines_offline = Machine.objects.filter(machine_status='OFFLINE', user=request.user)
    machines_online = Machine.objects.filter(machine_status='ONLINE', user=request.user)

    orders = Order.objects.filter(user=request.user)

    total_income = 0
    total_volume = 0.0
    for order in orders:
        total_income += order.amount
        total_volume += order.volume_in_ml

    total_volume_in_l = total_volume / 1000

    context = {
        'machines_count': machines.count(),
        'machines_offline':machines_offline.count(),
        'machines_online':machines_online.count(),

        'orders_count':orders.count(),
        'total_volume':int(total_volume_in_l),
        'total_income':total_income,
    }
    return render(request, 'dashboard.html', context)
