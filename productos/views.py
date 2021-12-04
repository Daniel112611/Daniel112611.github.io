from builtins import dict

from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from xhtml2pdf import pisa

from django.views.generic import View
from productos.prueba import render_pdf

from .models import Price_product, Product_type, Product, Product_provider, Provider, Tax_price_product, Tax, \
    Ticket_detail, Ticket, Person, Person_person_type, Person_type
from django.contrib import messages
from .forms import customerRegisterForm
from django.contrib.auth.forms import User
from decimal import *

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


# Arreglar proveedor de productos

def paginainicio(request):
    precioProductos = Price_product.objects.all()
    product = Product.objects.all()
    productProvider = Product_provider.objects.all()

    variable = {
        'Precioproductos': precioProductos,
        'product': product,
        'productProvider':productProvider,

    }

    return render(request, "faces/index.html", variable)


@login_required()
def crear_proceso_factura(request, id):
    productoPric = Price_product.objects.get(id=id)
    idProduct = Product.objects.get(id=id)
    idtaxPriceProduct = Tax_price_product.objects.get(id=id)


    taxPriceProduct = Tax_price_product.objects.all()
    person = Person.objects.all()
    persontype = Person_type.objects.all()
    productObjects = Product.objects.all()

    variable = {
        'productoPric': productoPric,
        'taxPriceProduct': taxPriceProduct,
        'person': person,
        'persontype': persontype,
        'productObjects':productObjects,
        'idProduct':idProduct,
        'idtaxPriceProduct':idtaxPriceProduct,
    }

    if request.POST:
        ticket = Ticket()

        # persona.id = request.POST.get('infoCajero')
        ticket.fk_id_person_cachier = Person.objects.get(id = request.POST.get('infoCajero'))


        ticketDetail = Ticket_detail()
        ticket.half_payment = request.POST.get('infoTipoPago')
        ticketDetail.fk_id_ticket = ticket
        ticket.ticket_date = request.POST.get('infoFechaTicket')
        ticketDetail.amount = request.POST.get('infoAmount')

        # persona.id = request.POST.get('infoCliente')
        ticket.fk_id_person_costumer = Person.objects.get(id = request.POST.get('infoCliente'))

        taxpricepro = Tax_price_product()
        taxpricepro.id = request.POST.get('infoIdTaxPricePro')
        ticketDetail.fk_id_tax_price_product = taxpricepro

        try:
            variable['mensaje'] = 'La factura se ha creado exitosamente'

        except:
            variable['mensaje'] = "Error. Ha habido una falla en la creacion de la factura"
        ticket.save()
        ticketDetail.save()
        return redirect('supermercado:registroFactura')

    return render(request, "procesoFactura.html", variable)

@login_required()
def registroCompras(request):
    ticket = Ticket.objects.all()
    ticketDetail = Ticket_detail.objects.all()
    product = Product.objects.all()
    # product = Product.objects.filter(=)

    variable={
        'ticket':ticket,
        'ticketDetail':ticketDetail,
        'product':product,
    }

    return render(request,"registrosCompras.html",variable)



def crear_producto_principal(request):
    provider = Provider.objects.all()
    tax = Tax.objects.all()
    taxPriceProduct = Tax_price_product.objects.all()
    variable = {
        'provider': provider,
        'tax': tax,
        'taxPriceProduct': taxPriceProduct

    }
    if request.POST:
        prod = Product()

        prod.product_name = request.POST.get('nameProduct')
        # prodProv.fk_id_product = prod

        provider = Provider()
        prodProv = Product_provider()
        provider.id = request.POST.get('idProvider')
        prodProv.fk_id_provider = provider

        taxpriceproduct = Tax_price_product()
        priceProd = Price_product()
        priceProd.shop_price = request.POST.get('priceShop')
        taxpriceproduct.fk_id_price_product = priceProd
        priceProd.sale_price = request.POST.get('priceSale')
        priceProd.start_date = request.POST.get('startDate')

        tax = Tax()
        tax.id = request.POST.get('infoTax')
        taxpriceproduct.fk_id_tax = tax

        try:

            variable['mensaje'] = 'Se ha creado exitosamente'

        except:
            variable['mensaje'] = "Error. No se ha creado exitosamente"
        prod.save()
        prodProv.save()
        priceProd.save()
        taxpriceproduct.save()

    return render(request, "faces/crear/crear_producto_principal.html", variable)




@login_required()
def crear_persona(request):
    personType = Person_type.objects.all()

    variable = {
        'personType': personType
    }

    if request.POST:
        person = Person()
        ppType = Person_person_type()
        person.person_name = request.POST.get('infoName')
        ppType.fk_id_person = person
        person.person_last_name = request.POST.get('infoLastName')
        person.person_address = request.POST.get('infoAddress')
        person.person_dni = request.POST.get('infoDni')

        personType = Person_type()
        personType.person_type_name = request.POST.get('infoTypeUser')
        ppType.fk_id_person_type = personType



        try:
            person.save()
            personType.save()
            ppType.save()

            variable['mensaje'] = "Se ha creado exitosamente"
        except:
            variable['mensaje'] = "Error, ha habido una falla en el crear"


    return render(request, "faces/crear/crear_persona.html", variable)

class PDF(View):
    def get(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=self.kwargs['id'])
        ticketDetail = Ticket_detail.objects.get(id=self.kwargs['id'])

        priceProd = Price_product.objects.all()
        product = Product.objects.all()
        variable = {
            'ticketDetail': ticketDetail,
            'ticket': ticket,
            'priceProd': priceProd,
            'product':product,
        }

        cantidad = ticketDetail.amount
        ivaProducto = ticketDetail.fk_id_tax_price_product.fk_id_tax.tax_value
        variable['name'] = ticketDetail.fk_id_tax_price_product.id

        precioProducto = ticketDetail.fk_id_tax_price_product.fk_id_price_product.shop_price

        for a in product:
            if  a.id == ticketDetail.fk_id_tax_price_product.id:
                variable['nombreProducto'] = a.product_name

        pago = ticket.half_payment
        pago_float = float(pago)

        variable['precioMostrar'] = precioProducto
        precioProd = precioProducto

        float_ivaProducto = float(ivaProducto)
        float_precioProd = float(precioProd)
        costoIva = float_ivaProducto * float_precioProd
        variable['costoIvaMostrar'] = float_ivaProducto * float_precioProd
        variable['totalMostrar'] = (cantidad * float_precioProd) + costoIva
        total = (cantidad * float_precioProd) + costoIva
        float_total = float(total)
        variable['cambioMostrar'] = pago_float - float_total
        variable['positivo'] = True
        cambio = pago_float - float_total

        variable['subtotal'] = (cantidad * float_precioProd)


        if cambio < 0:
            variable['positivo'] = False
            variable['cambioMostrar'] = -1 * cambio


        pdf = render_pdf("factura.html",variable)
        return HttpResponse(pdf, content_type="application/pdf")





def calc(request,id):
    ticket = Ticket.objects.get(id=id)
    ticketDetail = Ticket_detail.objects.get(id=id)

    priceProd = Price_product.objects.all()
    variable = {
        'ticketDetail': ticketDetail,
        'ticket':ticket,
        'priceProd':priceProd,
    }


    cantidad = ticketDetail.amount
    ivaProducto = ticketDetail.fk_id_tax_price_product.fk_id_tax.tax_value
    variable['name'] = ticketDetail.fk_id_tax_price_product.id

    precioProducto = ticketDetail.fk_id_tax_price_product.fk_id_price_product.shop_price

    pago = ticket.half_payment
    pago_float = float(pago)

    variable['PrecioMostrar'] = precioProducto
    precioProd = precioProducto

    float_ivaProducto = float(ivaProducto)
    float_precioProd = float(precioProd)
    costoIva = float_ivaProducto * float_precioProd
    variable['costoIvaMostrar'] = float_ivaProducto * float_precioProd
    variable['totalMostrar'] = (cantidad * float_precioProd) + costoIva
    total = (cantidad * float_precioProd) + costoIva
    float_total = float(total)
    variable['cambioMostrar'] = pago_float - float_total
    variable['positivo'] = True
    cambio = pago_float - float_total

    if cambio < 0:
        variable['positivo'] = False
        variable['cambioMostrar'] = -1*cambio

    return render(request, "factura.html",variable)






# def documento( request, id, doc) :
#     ticket = Ticket.objects.all()
#     variable={
#         'ticket':ticket,
#     }
#
#     return render(request, 'docs/5. htal', variable)
#
#
#     def docunentopdf(request, id, doc):
#         d = doc
#         t= Familia.objects.get(idwid)
#
# variable={
#     'page-size' : 'Letter' ,
#     'margin-top': 'lin',
#     'margin-right' : 'lin',
#     'margin-bottom': 'lin',
#     'margin-Left': 'lin',
#     'encodina': 'UTF-8',
# }


# def registrarUsuario(request):
#     if request.method == 'POST':
#         form = customerRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#
#             return redirect('supermercado:inicio')
#
#     return render(request, "registration/registrar.html", {"form": customerRegisterForm()})


# user = authenticate(username=username, password=password)


def plantillaPrincipal_administrador(request):
    return render(request, "principal_administrar_productos.html")


# CRUD de precio de producto

def adminproductos_priceproduct(request):
    Precioproductos = Price_product.objects.all()
    product = Product.objects.all()
    variable={
        'Precioproductos':Precioproductos,
        'product':product,
    }

    return render(request, "faces/listar/administrar_precio_productos.html",variable)


def crearPrecioProductos(request):
    a = Price_product.objects.all()
    productProvider = Product_provider.objects.all()
    product = Product.objects.all()
    variable = {
        'CrearPrePro': a,
        'productProvider': productProvider,
        'product':product ,
    }

    if request.POST:
        proP = Price_product()
        proP.sale_price = request.POST.get('infoSale_price')
        proP.shop_price = request.POST.get('infoShop_price')
        proP.start_date = request.POST.get('infoStart_date')
        proP.user_update = request.POST.get('infoUser_update')
        proP.date_update = request.POST.get('infoDate_update')

        productProv = Product_provider()
        productProv.id = request.POST.get('infoId')
        proP.fk_id_product_provider = productProv

        try:
            proP.save()
            variable['mensaje'] = 'Se ha creado exitosamente'
        except:
            variable['mensaje'] = 'Error. Ha habido una falla en la creacion'

    return render(request, "faces/crear/crear_precio_productos.html", variable)


def borrarPrecioProductos(request):
    return render(request, "faces/borrar/borrar_precio_productos.html",
                  {"BorrarPrecioproductos": Price_product.objects.all})


def eliminarPreprods(request, id):
    a = Product.objects.get(id=id)
    b = Product_provider.objects.get(id=id)
    c = Price_product.objects.get(id=id)
    d = Tax_price_product.objects.get(id=id)

    try:
        a.delete()
        b.delete()
        c.delete()
        d.delete()
        mensaje = "Se ha eliminado correctamente"
        messages.success(request, mensaje)
    except:
        mensaje = "Error, no se ha eliminado correctamente"
        messages.error(request, mensaje)
    return redirect('supermercado:listarprecioprod')


def modificarPrecioProductos(request, id):
    a = Price_product.objects.get(id=id)

    variable = {
        'EditarPrePro': a
    }

    if request.POST:
        proP = Price_product()
        proP.id = request.POST.get('infoId')
        proP.sale_price = request.POST.get('infoSale_price')
        proP.shop_price = request.POST.get('infoShop_price')
        proP.start_date = request.POST.get('infoStart_date')
        proP.user_update = request.POST.get('infoUser_update')
        proP.date_update = request.POST.get('infoDate_update')

        try:
            proP.save()
            mensg = 'Se ha modificado exitosamente'
            messages.success(request, mensg)
        except:
            mensg = 'Error. Ha habido una falla en la modificación'
            messages.error(request, mensg)
        return redirect('supermercado:listarprecioprod')

    return render(request, "faces/modificar/modificar_precio_productos.html", variable)


# CRUD de tipo de producto

# @login_required


@permission_required('supermercado:view_Product_type')
def adminproductos_productType(request):
    return render(request, "faces/listar/administrar_tipo_producto.html", {"productType": Product_type.objects.all})

def crearTipoProducto(request):
    a = Price_product.objects.all()
    variable = {
        'CrearTipPro': a
    }

    if request.POST:
        proT = Product_type()
        proT.product_type_name = request.POST.get('infoType_prod')

        try:
            proT.save()
            variable['mensaje'] = 'Se ha creado exitosamente'
        except:
            variable['mensaje'] = 'Error. Ha habido una falla en la creacion'

    return render(request, "faces/crear/crear_tipo_producto.html", variable)


def borrarTipoProductos(request):
    return render(request, "faces/borrar/borrar_tipo_productos.html",
                  {"borrarTipPro": Product_type.objects.all})


def borrarTipoPro(request, id):
    a = Product_type.objects.get(id=id)
    try:
        a.delete()
        mensaje = "Se ha eliminado correctamente"
        messages.success(request, mensaje)
    except:
        mensaje = "Error, no se ha eliminado correctamente"
        messages.error(request, mensaje)

    return redirect('supermercado:listartp')


def modificarTipoProducto(request, id):
    a = Product_type.objects.get(id=id)

    variable = {
        'EditarProType': a
    }

    if request.POST:
        proType = Product_type()
        proType.id = request.POST.get('infoId')
        proType.product_type_name = request.POST.get('EditarProType')

        try:
            proType.save()
            mensg = 'Se ha modificado exitosamente'
            messages.success(request, mensg)
        except:
            mensg = 'Error. Ha habido una falla en la modificación'
            messages.error(request, mensg)
        return redirect('supermercado:listartp')

    return render(request, "faces/modificar/modificar_tipo_productos.html", variable)


# ARREGLAAAAAAAAAAAR


# CRUD de productos

def admin_productos(request):
    return render(request, "faces/listar/administrar_productos.html", {"productos": Product.objects.all})


def crearProducto(request):
    tipoProducto = Product_type.objects.all()
    variable = {
        'tipoProducto': tipoProducto
    }

    if request.POST:
        pro = Product()
        pro.product_name = request.POST.get('infoNamePro')

        prodType = Product_type()
        prodType.id = request.POST.get('infoTipoProducto')
        pro.fk_id_product_type = prodType

        try:
            pro.save()
            variable['mensaje'] = 'Se ha creado exitosamente'
        except:
            variable['mensaje'] = 'Error. Ha habido una falla en la creacion'

    return render(request, "faces/crear/crear_productos.html", variable)


def borrarProductos(request):
    return render(request, "faces/borrar/borrar_productos.html",
                  {"borrarProds": Product.objects.all})


def eliminarPro(request, id):
    a = Product.objects.get(id=id)
    b = Product_provider.objects.get(id=id)
    c = Price_product.objects.get(id=id)
    d = Tax_price_product.objects.get(id=id)
    # Product.objects.filter(id=id).delete()
    try:
        a.delete()
        b.delete()
        c.delete()
        d.delete()
        mensaje = "Se ha eliminado correctamente"
        messages.success(request, mensaje)
    except:
        mensaje = "Error, no se ha eliminado correctamente"
        messages.error(request, mensaje)

    return redirect('supermercado:listarprods')


# def nombre_de_la_funcion(request):
#     return render(request, "Donde se encuentra el html",
#                   {"": Price_product.objects.all})

def modificarProductos(request, id):
    producto = Product.objects.get(id=id)
    tipoProductos = Product_type.objects.all()

    variable = {
        "producto": producto,
        "tipoProds": tipoProductos
    }

    if request.POST:
        prods = Product()
        prods.id = request.POST.get('infoId')
        prods.product_name = request.POST.get('infoNamePro')

        prodtyp = Product_type()
        prodtyp.id = request.POST.get('infoTipoProducto')
        prods.fk_id_product_type = prodtyp

        try:
            prods.save()
            mensaje = 'Se ha modificado exitosamente'
            messages.success(request, mensaje)
        except:
            mensaje = 'Error. Ha habido una falla en la modificación'
            messages.error(request, mensaje)
        return redirect('supermercado:listarprods')

    return render(request, "faces/modificar/modificar_productos.html", variable)


# proveedor

def admin_proveedor(request):
    return render(request, "faces/listar/administrar_proveedor.html", {"proveedor": Provider.objects.all})


def crearProveedor(request):
    a = Provider.objects.all()
    variable = {
        'proveedor': a

    }

    if request.POST:
        provi = Provider()
        provi.name = request.POST.get('infoName')
        provi.nit = request.POST.get('infoNit')
        # provi.url = request.POST.get('')
        provi.address = request.POST.get('infoAddress')
        provi.phone_number = request.POST.get('infoNumber')

        try:
            provi.save()
            variable['mensaje'] = 'Se ha creado exitosamente'
        except:
            variable['mensaje'] = 'Error. Ha habido una falla en la creacion'

    return render(request, "faces/crear/crear_proveedores.html", variable)


def borrarProveedor(request):
    return render(request, "faces/borrar/borrar_proveedor.html",
                  {"borrarProveeds": Provider.objects.all})


def eliminarProvdr(request, id):
    a = Provider.objects.get(id=id)
    try:
        a.delete()
        mensaje = "Se ha eliminado correctamente"
        messages.success(request, mensaje)
    except:
        mensaje = "Error, no se ha eliminado correctamente"
        messages.error(request, mensaje)

    return redirect('supermercado:listarprovds')


def modificarProveedor(request, id):
    a = Provider.objects.get(id=id)

    variable = {
        "provider": a,
    }

    if request.POST:
        provdr = Provider()
        provdr.id = request.POST.get('infoId')
        provdr.name = request.POST.get('infoName')
        provdr.nit = request.POST.get('infoNit')
        # provi.nit = request.POST.get('')
        provdr.address = request.POST.get('infoAddress')
        provdr.phone_number = request.POST.get('infoNumber')

        try:
            provdr.save()
            mensg = 'Se ha modificado exitosamente'
            messages.success(request, mensg)
        except:
            mensg = 'Error. Ha habido una falla en la modificación'
            messages.error(request, mensg)
        return redirect('supermercado:listarprovds')

    return render(request, "faces/modificar/modificar_proveedor.html", variable)


# CRUD de proveedor de productos

def admin_proveedor_productos(request):
    return render(request, "faces/listar/administrar_proveedor_productos.html",
                  {"productosProveedor": Product_provider.objects.all})


def crear_proveedor_productos(request):
    a = Provider.objects.all()
    productos = Product.objects.all()

    variable = {
        'provider': a,
        'productos': productos
    }
    if request.POST:
        Prodprov = Product_provider()
        Prodprov.bar_code = request.POST.get('infoCodigoBarra')
        Prodprov.stock = request.POST.get('infoExistencias')

        provdr = Provider()
        provdr.id = request.POST.get('infoProveedor')
        Prodprov.fk_id_provider = provdr

        prod = Product()
        prod.id = request.POST.get('infoProducto')
        Prodprov.fk_id_product = prod

        try:
            Prodprov.save()
            variable['mensaje'] = 'Se ha creado exitosamente'
        except:
            variable['mensaje'] = 'Error. Ha habido una falla en la creacion'

    return render(request, "faces/crear/crear_proveedor_productos.html", variable)


def borrarProveedorProductos(request):
    return render(request, "faces/borrar/borrar_proveedor_productos.html",
                  {"provedorProds": Product_provider.objects.all})


def eliminarProveedorprods(request, id):
    a = Product.objects.get(id=id)
    b = Product_provider.objects.get(id=id)
    c = Price_product.objects.get(id=id)
    d = Tax_price_product.objects.get(id=id)

    try:
        a.delete()
        b.delete()
        c.delete()
        d.delete()

        mensaje = "Se ha eliminado correctamente"
        messages.success(request, mensaje)
    except:
        mensaje = "Error, no se ha eliminado correctamente"
        messages.error(request, mensaje)

    return redirect('supermercado:listarprovdsprods')


def modificarProveedorProductos(request, id):
    producto_provider = Product_provider.objects.get(id=id)
    provider = Provider.objects.all()
    product = Product.objects.all()

    variable = {
        'producto_provider': producto_provider,
        'provider': provider,
        'product': product
    }

    if request.POST:

        Prodprov = Product_provider()
        Prodprov.id = request.POST.get('infoId')
        Prodprov.bar_code = request.POST.get('infoCodigoBarra')
        Prodprov.stock = request.POST.get('infoExistencias')

        provdr = Provider()
        provdr.id = request.POST.get('infoProveedor')
        Prodprov.fk_id_provider = provdr

        prod = Product()
        prod.id = request.POST.get('infoProducto')
        Prodprov.fk_id_product = prod
        try:
            Prodprov.save()
            mensg = 'Se ha modificado exitosamente'
            messages.success(request, mensg)
        except:
            mensg = 'Error. Ha habido una falla en la modificación'
            messages.error(request, mensg)
        return redirect('supermercado:listarprovdsprods')

    return render(request, "faces/modificar/modificar_proveedor_productos.html", variable)

# *************
