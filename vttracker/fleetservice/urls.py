from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/$', views.fleetAdmin, name='fleetAdmin'),
    url(r'^get_drivers/$', views.getDrivers, name='getDrivers'),
    url(r'^get_users/$', views.getUsers, name='getUsers'),
    url(r'^get_vehicles/$', views.getVehicles, name='getVehicles'),
    url(r'^create_driver/$', views.createDriver, name='createDriver'),
    url(r'^create_vehicle/$', views.createVehicle, name='createVehicle'),
    url(r'^register_binnacle/$', views.registerBinnacle, name='registerBinnacle'),
    url(r'^register_refuel/$', views.registerRefuel, name='registerRefuel'),
    url(r'^register_service/$', views.registerService, name='registerService'),

]
