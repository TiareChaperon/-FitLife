"""
URL configuration for fitlife project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from dashboard.views import inicio
from accounts.views import InicioSesionView, panel_cliente, reservar_clase, cancelar_reserva, ingresar_lista_espera

from accesos.views import control_acceso

from dashboard.views import dashboard_aforo

urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', InicioSesionView.as_view(), name='login'),
    path('panel/', panel_cliente, name='panel_cliente'),
    path('reservar/<int:clase_id>/', reservar_clase, name='reservar_clase'),
    path('cancelar-reserva/<int:reserva_id>/', cancelar_reserva, name='cancelar_reserva'),
    path('lista-espera/<int:clase_id>/', ingresar_lista_espera, name='ingresar_lista_espera'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('control-acceso/', control_acceso, name='control_acceso'),
    path('aforo/', dashboard_aforo, name='dashboard_aforo'),
    path('admin/', admin.site.urls),
]
