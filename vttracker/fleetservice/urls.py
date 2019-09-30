from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/$', views.fleetAdmin, name='fleetAdmin'),
    url(r'^get_drivers/$', views.getDrivers, name='getDrivers'),
    url(r'^get_users/$', views.getUsers, name='getUsers'),
    url(r'^get_refuels/$', views.getRefuels, name='getRefuels'),
    url(r'^get_vehicles/$', views.getVehicles, name='getVehicles'),
    url(r'^get_binnacles/$', views.getBinnacles, name='getBinnacles'),
    url(r'^get_services/$', views.getServices, name='getServices'),
    url(r'^create_driver/$', views.createDriver, name='createDriver'),
    url(r'^create_vehicle/$', views.createVehicle, name='createVehicle'),
    url(r'^register_binnacle/$', views.registerBinnacle, name='registerBinnacle'),
    url(r'^register_refuel/$', views.registerRefuel, name='registerRefuel'),
    url(r'^register_service/$', views.registerService, name='registerService'),
    url(r'^binnacle_search/$', views.binnacleSearch, name='binnacleSearch'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
