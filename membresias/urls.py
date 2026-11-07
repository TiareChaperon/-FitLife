from django.urls import path
from . import views

urlpatterns = [
    path('planes/', views.lista_planes, name='lista_planes'),
    path('planes/nuevo/', views.crear_plan, name='crear_plan'),
    path('planes/<int:plan_id>/editar/', views.editar_plan, name='editar_plan'),
    path('planes/<int:plan_id>/eliminar/', views.eliminar_plan, name='eliminar_plan'),
]
