from django.urls import path

from core.view.producto.views import *
from core.view.cliente.views import *
from core.view.vehiculo.views import *
from core.view.tests.views import *
from core.view.ventas.views import VentaCreateView, VentaListView, SaleInvoicePdfView

app_name = 'core'

urlpatterns = [
    #urls Producto
    path('producto/listar', productoListView.as_view(), name='category_list'),
    path('producto/crear', ProductoCreateView.as_view(), name='crear_producto'),
    path('producto/editar/<int:pk>/', ActualizarProducto.as_view(), name='modifcar_producto'),
    path('producto/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),

    #urls Cliente
    path('cliente/listar', ClienteListView.as_view(), name='listar_cliente'),
    path('cliente/crear', ClienteCreateView.as_view(), name='crear_cliente'),
    path('cliente/editar/<int:pk>/', ClienteUpdate.as_view(), name='modifcar_cliente'),
    path('cliente/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),

    #urls vehiculo
    path('vehiculo/listar', VehiculoListView.as_view(), name='listar_vehiculo'),
    path('vehiculo/crear', VehiculoCreateView.as_view(), name='crear_vehiculo'),
    path('vehiculo/editar/<int:pk>/', VehiculoUpdate.as_view(), name='modifcar_vehiculo'),
    path('vehiculo/eliminar/<int:pk>/', VehiculoDeleteView.as_view(), name='eliminar_vehiculo'),

    #urls test
    path('test/listar', ServicioListView.as_view(), name='listar_servicio'),
    path('test/listar2', ServicioListView1.as_view(), name='listar_servicio1'),
    path('test/editar/<int:pk>/', estadoUpdate.as_view(), name='modificar_estado'),
    path('test/', TestView.as_view(), name='test1'),
    path('test/crear', crearTest, name='test'),
    path('test/invoice/pdf/<int:pk>/', ServicioInvoicePdfView.as_view(), name='servicio_invoice_pdf'),

    #urls ventas
    path('venta/crear', VentaCreateView.as_view(), name='crear_venta'),
    path('venta/listar', VentaListView.as_view(), name='listar_venta'),
    path('venta/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='venta_invoice_pdf'),

#path ('crearCliente/', CrearClientes.as_view(), name = 'crearCliente'),
#path ('listarCliente/', ListadoCLiente.as_view(), name = 'listarCliente'),
#path ('editar_cliente/<int:pk>', ActualizarCliente.as_view(), name = 'editar_cliente'),
#path ('editar_cl/<int:pk>', ActualizarCliente1.as_view(), name = 'editar_cl')
 #path ('listar_autores/', listarAutor, name = 'listar_autores'),


]