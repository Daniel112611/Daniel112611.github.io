# from unittest.mock import _patch
from django.contrib import admin
from django.urls import path, include
from productos.views import PDF

from django.http.response import HttpResponse
from django.shortcuts import redirect
# from productos.views import crearPrecioProductos,paginainicio,adminproductos_productType,borrar1


from productos.admin import prod_type_Admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('supermercado/', include('productos.urls', namespace="productos")),
    path('accounts/',include('django.contrib.auth.urls')),
    path('pdf/<int:id>', PDF.as_view() ,name="pdf" ),



]


