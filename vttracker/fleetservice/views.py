from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    print(current_user.id)
    print(current_user.is_superuser)

    args = {'user': current_user}
    return render(request, 'home/index.html', args)

@login_required(login_url='/accounts/login/')
def fleetAdmin(request):
    return render(request, 'fleetAdmin/index.html')

@login_required(login_url='/accounts/login/')
def driverIndex(request):
    return render(request, 'driver/index.html')
