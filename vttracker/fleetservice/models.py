from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Vehicle(models.Model):
    id_vehicle = models.AutoField(primary_key=True)
    enrollment = models.CharField(max_length=50, blank=False, null=False)
    alias = models.CharField(max_length=20, blank=False, null=False)
    data_service = models.DateTimeField(max_length=6, blank = False, null=True)

    REQUIRED_FIELDS = ['id_vehicle', 'enrollment', 'alias']

    class Meta:
        verbose_name = _('vehiculo')
        verbose_name_plural = _('vehiculos')
        db_table = ('vehicle')

    def __str__(self):
        return self.enrollment

    def natural_key(self):
        object = {
            "pk": self.id_vehicle,
            "name": self.alias,
            "enrollment": self.enrollment,
            "data_service": self.data_service,
            }
        return object

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=70, blank=False, null=False)
    from_depto = models.CharField(max_length=70, blank=False, null=False)
    start_kilometer = models.FloatField(blank=False, null=True)
    end_kilometer = models.FloatField(blank=False, null=True)
    datetime = models.DateTimeField(max_length=6, blank = False, null=True)
    start_time = models.TimeField(max_length=6, blank = False, null=False)
    end_time = models.TimeField(max_length=6, blank = False, null=False)
    description = models.CharField(max_length=160, blank=False, null=False)

    #Relationship DB
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)

    REQUIRED_FIELDS = ['id_service', 'subject', 'from_depto',
                        'start_kilometer', 'end_kilometer', 'datetime',
                        'start_time', 'end_time', 'description']

    class Meta:
        verbose_name = _('servicio')
        verbose_name_plural = _('servicios')
        db_table = ('service')

    def __str__(self):
        return self.id_service

    def natural_key(self):
        object = {
            "pk": self.id_service,
            "subject": self.subject,
            "from_depto": self.from_depto,
            "start_kilometer": self.start_kilometer,
            "end_kilometer": self.end_kilometer,
            'datetime': self.datetime,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'description': self.description,
            }
        return object

class Binnacle(models.Model):

    ROUTES = (
        ("Seleccion", "Selecciona una opción"),
        ("Playa-Corporativo", "Playa del Carmen - Corporativo"),
        ("Corporativo-Playa", "Corporativo - Playa del Carmen")
    )

    id_binacle = models.AutoField(primary_key=True)
    route = models.CharField(max_length=50, choices=ROUTES, default='Seleccion')
    start_kilometer = models.FloatField(blank=False, null=False)
    end_kilometer = models.FloatField(blank=False, null=False)
    datetime = models.DateTimeField(max_length=6, blank = False, null=False)
    start_time = models.TimeField(max_length=6, blank = False, null=False)
    end_time = models.TimeField(max_length=6, blank = False, null=False)
    created_at = models.DateTimeField(max_length=6, blank = False, null=False)

    #Relationship DB
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    REQUIRED_FIELDS = [
        'id_binacle',
        'route',
        'start_kilometer',
        'end_kilometer',
        'datetime',
        'start_time',
        'end_time'
        ]

    class Meta:
        verbose_name = _('bitacora')
        verbose_name_plural = _('bitacoras')
        db_table = ('binnacle')

    def __str__(self):
        return self.id_binacle

    def natural_key(self):
        object = {
            'pk': self.id_binacle,
            'route': self.route,
            'start_kilometer': self.start_kilometer,
            'end_kilometer': self.end_kilometer,
            'datetime': self.datetime,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'created_at': self.created_at,
            'vehicle': {
                    'pk': self.vehicle.id_vehicle,
                    'alias': self.vehicle.alias,
                }
            }
        return object

class Refuel(models.Model):
    id_refuel = models.AutoField(primary_key=True)
    liters = models.FloatField(max_length=50, blank=False)
    amount = models.FloatField(max_length=50, blank=False)
    datetime = models.DateTimeField(max_length=6, blank = False, null=False)
    #image = models.CharField(max_length=200, blank=False)
    image = models.FileField(upload_to='documents/')

    #Relationship DB
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
        related_name='user'
    )

    REQUIRED_FIELDS = ['id_refuel', 'liters', 'amount', 'datetime', 'image']

    class Meta:
        verbose_name = _('recarga')
        verbose_name_plural = _('recargas')
        db_table = ('refuel')

    def __str__(self):
        return self.name

class Driver(models.Model):
    id_driver = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    license_number = models.CharField(max_length=50, blank=False)
    license_expedition = models.DateTimeField(max_length=6, blank = False)
    license_expiration = models.DateTimeField(max_length=6, blank = False)
    is_active = models.BooleanField(default=False)

    #Relationship DB OneToOneField
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user'
    )

    #Relationship DB ManyToManyFields
    binnacles = models.ManyToManyField('Binnacle', through='DriverBinacle', related_name='driverBinacle')
    services = models.ManyToManyField('Service', through='DriverService', related_name='driverService')
    refuels = models.ManyToManyField('Refuel', through='DriverRefuel', related_name='driverRefuel')

    REQUIRED_FIELDS = ['id_driver', 'name', 'license_number', 'license_expedition', 'license_expiration']

    class Meta:
        verbose_name = _('conductor')
        verbose_name_plural = _('conductores')
        db_table = ('driver')

    def __str__(self):
        return self.name

    def natural_key(self):
        object = {
            "pk": self.id_driver,
            "name": self.name,
            "is_active": self.is_active,
            "user": {
                    "pk": self.user.id,
                    "fullname": self.user.name + self.user.lastP + self.user.lastM,
                }
            }
        return object

class DriverBinacle(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    binnacle = models.ForeignKey('Binnacle', on_delete=models.CASCADE)
    date_joined= models.DateTimeField(max_length=6, blank = True)

    REQUIRED_FIELDS = ['driver_id', 'binnacle_id', 'date_joined']

    class Meta:
        db_table = ('DriverBinacle')

    def __str__(self):
        return "binnacle: %s belongs to driver: %s" % (self.binnacle_id, self.driver_id)

class DriverService(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    date_joined= models.DateTimeField(max_length=6, blank = True)

    REQUIRED_FIELDS = ['driver_id', 'service_id', 'date_joined']

    class Meta:
        db_table = ('DriverService')

    def __str__(self):
        return "the service: %s was performed by driver: %s" % (self.binnacle_id, self.driver_id)

class DriverRefuel(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    refuel = models.ForeignKey('Refuel', on_delete=models.CASCADE)
    date_joined= models.DateTimeField(max_length=6, blank = True)

    REQUIRED_FIELDS = ['driver_id', 'refuel_id', 'date_joined']

    class Meta:
        db_table = ('DriverRefuel')

    def __str__(self):
        return "the driver: %s realized the refuel: %s" % (self.driver_id, self.refuel_id)
