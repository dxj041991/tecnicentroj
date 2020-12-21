from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.forms import ProductForm
from core.models import Producto
from core.mixins import ValidatePermissionRequiredMixin

class productoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    permission_required = 'core.view_producto'
    model = Producto
    template_name = 'productos/listar_producto.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('core:crear_producto')
        context['list_url'] = reverse_lazy('core:category_list')
        context['entity'] = 'Categorias'
        return context

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductForm
    template_name = 'productos/crear_producto.html'
    success_url = reverse_lazy('core:category_list')
    url_redirect = success_url


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = ProductForm(request.POST)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opcion'
        except Exception as e:
            data['error']= str(e)
        return JsonResponse(data)


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un Producto'
        context['list_url'] = self.success_url
        context['action'] ='add'

        return context

class ActualizarProducto(UpdateView):
    model = Producto
    form_class = ProductForm
    template_name = 'productos/crear_producto.html'
    success_url = reverse_lazy('core:category_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar un Producto'
        context['list_url'] = self.success_url
        context['action'] = 'edit'

        return context


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/delete_producto.html'
    success_url = reverse_lazy('core:category_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        return context
