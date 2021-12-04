from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def listar(request):
    return render(request, 'bodega/index.html')

def guardar(request):
    return render(request, 'bodega/guardar.html')

def detalle(request, id):
    print(id)
    return render(request, 'bodega/detalle.html')


def borrar(request, id):
    return HttpResponse("borrar", id)
