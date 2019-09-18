from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=70, blank=False, null=False)
    from_depto = models.CharField(max_length=70, blank=False, null=False)
    datetime = models.DateTimeField(max_length=6, blank = False, null=True)
    description = models.CharField(max_length=160, blank=False, null=False)

    REQUIRED_FIELDS = ['id_service', 'subject', 'from_depto', 'datetime', 'description']

    class Meta:
        verbose_name = _('servicio')
        verbose_name_plural = _('servicios')
        db_table = ('service')

    def __str__(self):
        return self.id_service

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

class Binnacle(models.Model):
    id_binacle = models.AutoField(primary_key=True)
    route = models.CharField(max_length=50, blank=False, null=False)
    start_kilometer = models.FloatField(blank=False, null=False)
    end_kilometer = models.FloatField(blank=False, null=False)
    start_fuel = models.FloatField(blank=False, null=False)
    end_fuel = models.FloatField(blank=False, null=False)
    start_datetime = models.DateTimeField(max_length=6, blank = False, null=False)
    end_datetime = models.DateTimeField(max_length=6, blank = False, null=False)
    fuel_voucher = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(max_length=6, blank = False, null=False)

    #Relationship DB
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['id_binacle',
                        'route',
                         'start_kilometer',
                         'end_kilometer',
                         'start_fuel',
                         'end_fuel',
                         'start_datetime',
                         'end_datetime',
                    ]
                    
    class Meta:
        verbose_name = _('bitacora')
        verbose_name_plural = _('bitacoras')
        db_table = ('binnacle')

    def __str__(self):
        return self.id_binacle

class Driver(models.Model):
    id_driver = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)

    #Relationship DB
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    binnacles = models.ManyToManyField('Binnacle', through='DriverBinacleService', related_name='idBinnacle')
    services = models.ManyToManyField('Service', through='DriverBinacleService', related_name='idBinnacle')

    REQUIRED_FIELDS = ['id_driver', 'name']

    class Meta:
        verbose_name = _('conductor')
        verbose_name_plural = _('conductores')
        db_table = ('driver')

    def __str__(self):
        return self.name

class DriverBinacleService(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    binnacle = models.ForeignKey('Binnacle', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    date_joined= models.DateTimeField(max_length=6, blank = True)

    REQUIRED_FIELDS = ['driver_id', 'binnacle_id', 'service_id', 'date_joined']

    class Meta:
        db_table = ('DriverBinacleService')

    def __str__(self):
        return "binnacle: %s belongs to driver: %s" % (self.binnacle_id, self.service_id)
