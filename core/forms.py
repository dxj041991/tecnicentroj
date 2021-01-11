from datetime import datetime

from django.forms import *

from core.models import Producto, Cliente, Vehiculo, Venta, servicio


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
             form.field.widget.attrs['class'] = 'form-control'
             form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',

                }
            ),


        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



class ServicioForm(ModelForm):


    class Meta:
        model = servicio
        fields = '__all__'
        widgets = {
            'veh': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'descr': Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),


        }



class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
             form.field.widget.attrs['class'] = 'form-control'
             form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['Cedula'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'Cedula': NumberInput(
                attrs={
                    'placeholder': 'Ingrese La cedula/ruc',
                    'maxlength': '13',
                }
            ),
            'NombreCliente': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre y apellido del cliente',

                }
            ),
            'Correo_electronico': TextInput(
                attrs={
                    'placeholder': 'Ingrese el correo electronico',

                }
            ),
            'Telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero de telefono',
                    'maxlength': '10',

                }
            ),
            'Direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion',
                    'maxlength': '50',

                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class VehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
             form.field.widget.attrs['class'] = 'form-control'
             form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['client'].widget.attrs['autofocus'] = True

    class Meta:
        model = Vehiculo
        fields = '__all__'
        widgets = {

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(Form):
    cliente = ModelChoiceField(queryset=Cliente.objects.all(), widget=Select(attrs={
        'class': 'form-control select2'
    }))

    vehiculo = ModelChoiceField(queryset=Vehiculo.objects.none(), widget=Select(attrs={
        'class': 'form-control select2'
    }))

    #search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    #}))

    search = ModelChoiceField(queryset=Vehiculo.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

class VentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'fecha': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }
