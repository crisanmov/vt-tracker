import simplejson as json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.utils import timezone
from accounts.models import User
from fleetservice.forms import (
    BinnacleForm,
    RefuelForm,
    ServiceForm,)
from fleetservice.models import (
    Driver,
    Vehicle,
    Binnacle,
    DriverBinacle,
    DriverService,
    DriverRefuel,)

@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    #users = User.objects.all().filter(is_superuser=False)
    drivers =  Driver.objects.all().select_related('user')
    args = {
        'user': current_user,
        'drivers': drivers,
        }
    return render(request, 'home/index.html', args)

@login_required(login_url='/accounts/login/')
def fleetAdmin(request):
    return render(request, 'fleetAdmin/index.html')

@login_required(login_url='/accounts/login/')
def getDrivers(request):
    response_data = {}

    try:
        drivers = Driver.objects.all().select_related('user')
        list = []
        #depth QuerySet
        for driver in drivers:
            list.append({
                'pk': driver.pk,
                'username': driver.user.username,
                'name': driver.user.name + " " + driver.user.lastP + " " + driver.user.lastM,
                'alias': driver.name,
                'email': driver.user.email,
                'is_active': driver.is_active,
            })

        response_data['status'] = True
        response_data['data'] = list
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
def getBinnacles(request):
    response_data = {}

    data = serializers.serialize('json', DriverBinacle.objects.all(), use_natural_foreign_keys=True)
    response_data['status'] = True
    response_data['data'] = data
    response_data['msg'] = "QuerySet Status::Done"
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def getServices(request):
    response_data = {}

    data = serializers.serialize('json', DriverService.objects.all(), use_natural_foreign_keys=True)
    response_data['status'] = True
    response_data['data'] = data
    response_data['msg'] = "QuerySet Status::Done"
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def getVehicles(request):
    response_data = {}

    data = serializers.serialize('json', Vehicle.objects.all())
    response_data['status'] = True
    response_data['data'] = data
    response_data['msg'] = "QuerySet Status::Done"
    return HttpResponse(json.dumps(response_data), content_type="application/json")

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

    try:
        user = User.objects.get(pk=request.POST.get('idUser'))
        Driver.objects.create(name=request.POST.get('alias'), user=user, is_active=True)
        user.is_active = False
        user.save(update_fields=['is_active'])

        response_data['status'] = True
        response_data['msg'] = "Conductor se creo correctamente."
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        response_data['status'] = False
        response_data['msgError'] = e
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data['msgError'] = "Error:: No se pudo crear el conductor en la DB."
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def createVehicle(request):
    response_data = {}

    try:
        Vehicle.objects.create(enrollment=request.POST.get('enrollment'),
        alias=request.POST.get('name'),
        data_service=request.POST.get('date_service'))

        response_data['status'] = True
        response_data['msg'] = "Vehiculo creado correctamente."
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        response_data['status'] = False
        response_data['msgError'] = e
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data['msgError'] = "Error:: No se pudo crear el vehiculo en la DB."
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def registerBinnacle(request):

    if request.method == 'POST':
        form = BinnacleForm(request.POST)
        response_data = {}

        if form.is_valid():

            binnacle = form.save(commit=False)
            binnacle.vehicle = Vehicle.objects.get(pk=request.POST.get('vehicle_id'))
            binnacle.save()
            #***************save relation m2m*****************
            driver = Driver.objects.get(user=request.user.pk)
            DriverBinacle.objects.create(driver=driver, binnacle=binnacle, date_joined=timezone.now())
            #*************************************************

            response_data['status'] = True
            response_data['msg'] = "Registro de bitacora exitoso."
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['status'] = False
            response_data['errors'] = form.errors
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
    	form = BinnacleForm()
    	args = {'form': form}
    	return render(request, 'binnacle/registerBinnacle.html', args)

@login_required(login_url='/accounts/login/')
def registerRefuel(request):

    if request.method == 'POST':
        form = RefuelForm(request.POST)
        response_data = {}

        if form.is_valid():
            refuel = form.save(commit=False)
            refuel.save()
            #***************save relation m2m*****************
            driver = Driver.objects.get(user=request.user.pk)
            DriverRefuel.objects.create(driver=driver, refuel=refuel, date_joined=timezone.now())
            #*************************************************

            response_data['status'] = True
            response_data['msg'] = "Recarga de combustible guardada."
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['status'] = False
            response_data['errors'] = form.errors
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
    	form = RefuelForm()
    	args = {'form': form}
    	return render(request, 'refuel/registerRefuel.html', args)

@login_required(login_url='/accounts/login/')
def registerService(request):

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        response_data = {}
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            #***************save relation m2m*****************
            driver = Driver.objects.get(user=request.user.pk)
            DriverService.objects.create(driver=driver, service=service, date_joined=timezone.now())
            #*************************************************
            response_data['status'] = True
            response_data['msg'] = "Encomienda registrada exitosamente"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['status'] = False
            response_data['errors'] = form.errors
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        form = ServiceForm()
        args = {'form': form}
        return render(request, 'service/registerService.html', args)
