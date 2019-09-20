import simplejson as json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from accounts.models import User

@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    args = {'user': current_user, 'users': User.objects.all()}
    return render(request, 'home/index.html', args)

@login_required(login_url='/accounts/login/')
def fleetAdmin(request):
    return render(request, 'fleetAdmin/index.html')

@login_required(login_url='/accounts/login/')
def driverIndex(request):
    return render(request, 'driver/index.html')

@login_required(login_url='/accounts/login/')
def getUsers(resquest):
    response_data = {}
    try:
        data = serializers.serialize('json', User.objects.filter(is_superuser=False, is_active=True), fields=('name', 'lastP', 'lastM'))
        response_data['status'] = True
        response_data['data'] = data
        response_data['msg'] = "QuerySet Status::Done"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except ObjectDoesNotExist as e:
        response_data['status'] = False
        response_data['msgError'] = e
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        response_data['status'] = False
        response_data['msgError'] = e

    response_data['msgError'] = "Error Run QuerySet Failed."
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def createDriver(request):
    response_data = {}
    esponse_data['status'] = True
    return HttpResponse(json.dumps(response_data), content_type="application/json")









    
