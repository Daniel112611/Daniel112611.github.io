from django.shortcuts import render
from .carro import Carrito
from productos.models import Price_product

from django.shortcuts import redirect

# Create your views here.

# def agregarProducto(request, id):
#
#     carrito = Carrito(request)
#     producto = Price_product.objects.get(id=id)
#
#     carrito.agregar_producto_carrito(producto= producto)
#     return redirect('supermercado:inicio')
#
# def eliminarProducto(request, id):






