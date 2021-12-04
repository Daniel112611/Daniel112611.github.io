from django.contrib import admin
from django.urls import path
from . import views,models


app_name = "supermercado"

urlpatterns = [
    path('', views.paginainicio, name="inicio"),

    # Arreglar proveedor de productos y productos


    # path('registrousuario', views.registrarUsuario, name="registuser"),
    path('crearProductosOficial', views.crear_producto_principal, name="creadorProductosOfic"),
    path('crearusuario', views.crear_persona, name="crearUsuario"),
    path('crearprocesofactura/<int:id>', views.crear_proceso_factura, name="procesoFactura"),
    # path('calculofactura/<int:id>', views., name="calculoFactura"),
    path('registrosfacturas/', views.registroCompras , name="registroFactura"),



    path('adminproductos', views.admin_productos, name="adminproduct"),
    path('admintipoproductos', views.adminproductos_productType, name="admintipopro"),
    path('priceproductos', views.adminproductos_priceproduct, name="adminpricepro"),
    path('proveedores', views.admin_proveedor, name="provider"),
    path('proveedoresproductos', views.admin_proveedor_productos, name="productsprovider"),


    # ---------------------------------------Creates-----------------------------------------------------
    path('creartipoproducto', views.crearTipoProducto, name="creartipoproducto"),
    path('crearproductos', views.crearProducto, name="crearproductos"),
    path('crearprecioproductos', views.crearPrecioProductos, name="crearpreciopro"),
    path('crearproveedor', views.crearProveedor, name="crearproveedor"),
    path('crearproveedorproductos', views.crear_proveedor_productos, name="crearproveedorproductos"),


    # ----------------------------------------Deletes----------------------------------------------------

    path('editartipoproducto', views.borrarTipoProductos, name="listartp"),
    path('eliminacion/<id>/', views.borrarTipoPro, name="eliminartipopro"),

    path('editarproductos',views.borrarProductos, name="listarprods"),
    path('eliminacionP/<int:id>',views.eliminarPro, name="eliminarpro"),

    path('editarpriceproduct',views.borrarPrecioProductos, name="listarprecioprod"),
    path('borrarpriceproduct/<int:id>',views.eliminarPreprods, name="eliminarproprice"),

    path('editarproveedor', views.borrarProveedor, name="listarprovds"),
    path('borrarproveedor/<int:id>', views.eliminarProvdr, name="eliminarprovds"),

    path('editarProvedorprod', views.borrarProveedorProductos, name="listarprovdsprods"),
    path('editarProvedorprod/<int:id>', views.eliminarProveedorprods, name="eliminarprovedorprods"),



    # ----------------------------------------Modificar--------------------------------------------------
    path('modificartipopro/<int:id>',views.modificarTipoProducto, name="modificartippro"),
    path('modificarproducto/<int:id>',views.modificarProductos, name="modificarprods"),
    path('modificarprovider/<int:id>',views.modificarProveedor, name="modificarprovider"),
    path('modificarpriceproduct/<int:id>',views.modificarPrecioProductos, name="modificarpreprods"),
    path('modificarproductprovider/<int:id>',views.modificarProveedorProductos, name="modificarproveedorprods"),

    #

    # path('')






]
