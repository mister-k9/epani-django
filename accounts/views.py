from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from accounts.models import Account



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
       
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('login')

def register(request):
    
    if request.method == 'POST':
        user_type = request.POST['user-type']
        if not request.POST['password'] == request.POST['confirm-password']:
            return HttpResponse('Passwords did not match!')

        
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone-number']
        
        username = email.split('@')[0]
        user = Account.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.phone_number = phone_number
        user.is_active = True
        if user_type == 'machine':
            user.is_user = True
        elif user_type == 'cluster':
            user.is_cluster = True
        user.save()

           

           
        return redirect('/')
    
    return render(request, 'accounts/register.html')



