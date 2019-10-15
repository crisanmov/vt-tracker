import xmltodict
import simplejson as json
import random
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.utils import timezone
from django.conf import settings
from django.db.models import Max, Min
from accounts.models import User
from fleetservice.forms import (
    BinnacleForm,
    RefuelForm,
    ServiceForm,)
from fleetservice.models import (
    Driver,
    Vehicle,
    Binnacle,
    Service,
    Refuel,
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
        data = serializers.serialize('json', Driver.objects.all().select_related('user'), use_natural_foreign_keys=True)
        #drivers = Driver.objects.all().select_related('user')
        #list = []
        #depth QuerySet
        """for driver in drivers:
            list.append({
                'pk': driver.pk,
                'username': driver.user.username,
                'name': driver.user.name + " " + driver.user.lastP + " " + driver.user.lastM,
                'alias': driver.name,
                'email': driver.user.email,
                'is_active': driver.is_active,
            })"""

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
def getBinnacles(request):
    response_data = {}

    data = serializers.serialize('json', \
        DriverBinacle.objects.all().order_by('binnacle_id')[::-1], \
        use_natural_foreign_keys=True)

    response_data['status'] = True
    response_data['data'] = data
    response_data['msg'] = "QuerySet Status::Done"

    return HttpResponse(json.dumps(response_data), \
        content_type="application/json")

@login_required(login_url='/accounts/login/')
def getServices(request):
    response_data = {}

    data = serializers.serialize('json', \
        DriverService.objects.all().order_by('service_id')[::-1], \
        use_natural_foreign_keys=True)

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
        data = serializers.serialize('json', User.objects.filter(
        is_superuser=False),
        fields=('name', 'lastP', 'lastM', 'email', 'phone', 'address'))

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
def getRefuels(requests):
    response_data = {}

    data = serializers.serialize('json', \
        Refuel.objects.all().order_by('id_refuel')[::-1], \
        use_natural_foreign_keys=True)

    response_data['status'] = True
    response_data['data'] = data
    response_data['msg'] = "QuerySet Status::Done"

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def createDriver(request):
    response_data = {}

    try:
        user = User.objects.get(pk=request.POST.get('idUser'))

        Driver.objects.create(
            name=request.POST.get('alias'),
            user=user,
            is_active=True,
            license_number=request.POST.get('license_number'),
            license_expedition=request.POST.get('license_expedition'),
            license_expiration=request.POST.get('license_expiration'),
            )

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
            vehicle = Vehicle.objects.get(pk=request.POST.get('vehicle_id'))

            binnacle = form.save(commit=False)
            binnacle.vehicle = vehicle
            binnacle.save()

            #***************save relation m2m***************************
            driver = Driver.objects.get(user=request.user.pk)
            DriverBinacle.objects.create(driver=driver, binnacle=binnacle, \
                date_joined=timezone.now())
            #***********************************************************

            #******************save file with current mileages**********
            vehicle = 'kilometraje-actual-' + vehicle.alias
            current_mileages = str(binnacle.end_kilometer)

            path_file = settings.MEDIA_ROOT + '/current_mileages/' + vehicle + '.txt'
            with open(path_file, 'w') as file:
                file.write(current_mileages)
            #***********************************************************

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
    if request.method == 'POST' and request.FILES:
        form = RefuelForm(request.POST, request.FILES)
        response_data = {}

        if form.is_valid():
            refuel = form.save(commit=False)
            refuel.vehicle = Vehicle.objects.get(pk=request.POST.get('vehicle_id'))
            refuel.save()
            #***********save image***********
            image =  request.FILES['image']
            #file_storage = FileSystemStorage()
            #file = file_storage.save(image.name, image)
            #path_file = file_storage.url(file)
            path_file = 'documents/' + image.name
            #********************************

            #***************save relation m2m*****************
            driver = Driver.objects.get(user=request.user.pk)
            DriverRefuel.objects.create(driver=driver, refuel=refuel, date_joined=timezone.now())
            #*************************************************

            response_data['status'] = True
            response_data['msg'] = "Recarga de combustible guardada."
            response_data['path_file'] = path_file
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
            vehicle = Vehicle.objects.get(pk=request.POST.get('vehicle_id'))

            service = form.save(commit=False)
            service.vehicle = vehicle
            service.save()

            #***************save relation m2m*****************
            driver = Driver.objects.get(user=request.user.pk)
            DriverService.objects.create(driver=driver, service=service, date_joined=timezone.now())
            #*************************************************

            #******************save file with current mileages**********
            vehicle = 'kilometraje-actual-' + vehicle.alias
            current_mileages = str(service.end_kilometer)

            path_file = settings.MEDIA_ROOT + '/current_mileages/' + vehicle + '.txt'
            with open(path_file, 'w') as file:
                file.write(current_mileages)
            #***********************************************************

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

@login_required(login_url='/accounts/login/')
def binnacleSearch(request):
    response_data = {}

    startDate = request.GET.get('startDateB')
    endDateB = request.GET.get('endDateB')

    if request.GET.get('option') == 'one':
        vehicle = request.GET.get('vehicle')

        data = serializers.serialize('json', Binnacle.objects.filter(
        datetime__range=(startDate, endDateB),
        vehicle=vehicle),
        use_natural_foreign_keys=True)

        response_data['status'] = True
        response_data['data'] = data

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        data = serializers.serialize('json', Binnacle.objects.filter(
        datetime__range=(startDate, endDateB)),
        use_natural_foreign_keys=True)

        response_data['status'] = True
        response_data['data'] = data

        return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def serviceSearch(request):

    response_data = {}

    startDateS = request.GET.get('startDateS')
    endDateS = request.GET.get('endDateS')

    if request.GET.get('option') == 'one':
        vehicle = request.GET.get('vehicle')

        data = serializers.serialize('json', Service.objects.filter(
        datetime__range=(startDateS, endDateS),
        vehicle=vehicle),
        use_natural_foreign_keys=True)

        response_data['status'] = True
        response_data['data'] = data

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        data = serializers.serialize('json', Service.objects.filter(
        datetime__range=(startDateS, endDateS)),
        use_natural_foreign_keys=True)

        response_data['status'] = True
        response_data['data'] = data

        return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def generateFileXml(request):

    object = request.POST.get('json')
    object = json.loads(object)
    startDate = request.POST.get('startDateB')
    endDate = request.POST.get('endDateB')
    now = timezone.now()
    now = str(now)
    now = now[:10]
    """
    path_file = settings.MEDIA_ROOT + '/bitacora-generate-at' + now + '.json'
    with open(path_file, 'w') as file:
        file.write(object_json)
    """
    #json.loads decoded JSON
    #json.dumps encoded JSON
    xmlString = xmltodict.unparse(json.loads(json.dumps(object)), pretty=True)
    file_name = '/binnacles/bitacora-' + \
        str(random.randrange(1, 10000000) + 1) + \
        '-' + startDate +  '-at-' + endDate + '.xls'

    path_file = settings.MEDIA_ROOT + file_name
    with open(path_file, 'w') as file:
        file.write(xmlString)

    response_data = {}
    response_data['status'] = True
    response_data['file_name'] = file_name

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/accounts/login/')
def getCurrentMileagesVehicle(request):
    response_data = {}
    print(request.GET.get('vehicle'))
    if request.GET.get('from_file'):

        filename = 'kilometraje-actual-' + request.GET.get('vehicle')
        path_file = settings.MEDIA_ROOT + '/current_mileages/' + filename + '.txt'

        f = open(path_file, "r")
        if f.mode == 'r':
            current_mileages = f.read()

        response_data['status'] = True
        response_data['current_mileages'] = current_mileages
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        vehicle_id = request.GET.get('id_vehicle')
        current_mileages_vehicle = Binnacle.objects.filter(vehicle_id = vehicle_id).aggregate( \
            Max('end_kilometer'))

        response_data['status'] = True
        response_data['end_kilometer__max'] = current_mileages_vehicle['end_kilometer__max']

        return HttpResponse(json.dumps(response_data), content_type="application/json")

def generatePerformance(request):

    startDate = request.POST.get('startDateP')
    endDate = request.POST.get('endDateP')
    vehicle = request.POST.get('vehicle')

    data = serializers.serialize('json', Refuel.objects.filter(datetime__range=(startDate, endDate)), use_natural_foreign_keys=True)
    data = json.loads(data)

    array = []
    vehicle = ""
    for i in range(len(data)):
        pk = data[i]['fields']['vehicle']['pk']
        vehicleName = data[i]['fields']['vehicle']['name']
        liters = data[i]['fields']['liters']
        amount = data[i]['fields']['amount']

        if vehicle != vehicleName:
            object = { 'pk': pk, 'vehicle': vehicleName, 'liters': liters, 'amount': amount }
            array.append(object)
            vehicle = vehicleName
        else:
            for j in range(len(array)):
                if vehicle == vehicleName:
                    litersCount = float(liters) + float(array[j]['liters'])
                    litersCount = round(litersCount, 2)
                    array[j]['liters'] = str(litersCount)
                    amountCount = float(amount) + float(array[j]['amount'])
                    amountCount = round(amountCount, 2)
                    array[j]['amount'] = str(amountCount)
                    vehicle = vehicleName



    for k in range(len(array)):
        id_vehicle = array[k]['pk']
        print('##########################')
        print(id_vehicle)

        #last kilometer register that vehicle
        kmMax = Binnacle.objects.filter(datetime__range=(startDate, endDate), \
        vehicle_id = id_vehicle).aggregate(Max('end_kilometer'))

        #first kilometer register that vehicle
        kmMin = Binnacle.objects.filter(datetime__range=(startDate, endDate), \
        vehicle_id = id_vehicle).aggregate(Min('start_kilometer'))

        print(kmMin)
        print(kmMax)
        kmTraveled = float(kmMax['end_kilometer__max']) - float(kmMin['start_kilometer__min'])
        array[k]['mileages'] = kmTraveled
        print('##########################')


    print(array)
    response_data = {}
    response_data['status'] = True
    response_data['data'] = json.dumps(array)
    #print(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
