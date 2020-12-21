from django.db import models
from datetime import  datetime
# Create your models here.
from django.forms import model_to_dict


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    Cedula = models.CharField(max_length=13, blank=False, null=False, unique=True)
    NombreCliente = models.CharField(max_length=30, blank=False, null=False)
    Correo_electronico = models.CharField(max_length=30, blank=True, null=True)
    Telefono = models.CharField(max_length=10, blank=False, null=False)
    Direccion = models.CharField(max_length=50, blank=False, null=False)
    Estado = models.BooleanField(default=True)

    def __str__(self):
        return self.Cedula

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    client= models.ForeignKey(Cliente, on_delete=Cliente)
    placa = models.CharField(max_length=10, blank=False, null=False)
    modelo = models.CharField(max_length=30, blank=False, null=False)


    def __str__(self):
        return self.placa

    def toJSON(self):
        item = model_to_dict(self)
        item['client'] = self.client.toJSON()
        return item


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    precioVenta = models.DecimalField(max_digits=10, decimal_places=2)
    precioCompra = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(blank=False, null=False)
    #imagen = models.ImageField(null=True, blank=True)
    observaciones = models.TextField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['precioVenta'] = format(self.precioVenta, '.2f')
        return item

class servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    veh = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    kilo =models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    descr = models.TextField(max_length=5000, blank=False, null=False)
    fecha = models.DateField(default=datetime.now)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descr

    def toJSON(self):
        item = model_to_dict(self)
        item['veh'] = self.veh.toJSON()
        item['kilo'] = format(self.kilo, '.2f')
        item['descr'] = format(self.descr )
        item['estado'] = format(self.estado)
        return item

class Venta(models.Model):
    cli = models.ForeignKey(Cliente, on_delete= models.CASCADE)
    fecha= models.DateField(default=datetime.now)
    subtotal= models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.NombreCliente

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        return item

class detVenta(models.Model):
    venta= models.ForeignKey(Venta, on_delete=models.CASCADE)
    prod= models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio= models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant= models.IntegerField(default=0)
    subtotal= models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['prod'] = self.prod.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item