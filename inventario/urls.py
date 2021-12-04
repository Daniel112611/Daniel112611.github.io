from django.contrib import admin
from django.urls import path
from . import views

app_name = "bodegas"

urlpatterns = [
    path('', views.listar, name="listar_bodega"),
    path('guardar', views.guardar,name="almacenar_bodega"),
    path('detalle/<int:id>', views.detalle,name="detalle_bodega"),
    path('borrar/<int:id>', views.borrar,name="borrar_bodega"),

]
