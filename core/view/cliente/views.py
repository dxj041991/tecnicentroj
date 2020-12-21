from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.forms import ClientForm
from core.models import Cliente


class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente/listar_cliente.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cliente'
        context['create_url'] = reverse_lazy('core:crear_cliente')
        context['list_url'] = reverse_lazy('core:listar_cliente')
        context['entity'] = 'Clientes'
        context['form'] = ClientForm()
        return context

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClientForm
    template_name = 'cliente/crear_Cliente.html'
    success_url = reverse_lazy('core:listar_cliente')
    url_redirect = success_url


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = ClientForm(request.POST)
                print(form)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opcion'
        except Exception as e:
            data['error']= str(e)
        return JsonResponse(data)


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un Cliente'
        context['list_url'] = self.success_url
        context['action'] ='add'


        return context

class ClienteUpdate(UpdateView):
    model = Cliente
    form_class = ClientForm
    template_name = 'cliente/crear_cliente.html'
    success_url = reverse_lazy('core:listar_cliente')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
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
        context['title'] = 'Editar un Cliente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'

        return context


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cliente/delete_cliente.html'
    success_url = reverse_lazy('core:listar_cliente')
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
        context['title'] = 'Eliminación de un Cliente'
        context['entity'] = 'Cliente'
        context['list_url'] = self.success_url
        return context
