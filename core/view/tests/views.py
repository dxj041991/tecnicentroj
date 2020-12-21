import os

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, request, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from xhtml2pdf import pisa

from core.forms import TestForm, ServicioForm
from core.models import Producto, Vehiculo, Cliente, servicio
from tecnicentro import settings


class TestView(TemplateView):
    template_name = 'tests.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = [{'id':'','text':'----------'}]
                for i in Vehiculo.objects.filter(client_id=request.POST['id']):
                    data.append({'id': i.id_vehiculo, 'text': i.placa})
            elif action == 'autocomplete':
                data = []
                for i in Vehiculo.objects.filter(placa__icontains=request.POST['term'])[0:10]:
                    item = i.toJSON()
                    print(i.placa)
                    item['text'] = i.placa
                    data.append(item)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ORDEN DE TRABAJO'
        context['form'] = TestForm()
        return context

def crearTest(request):


    if request.method == 'POST':
        form =ServicioForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ServicioForm()
        print(form)
    return render(request, 'tests1.html' ,{'form': form})

class ServicioListView(ListView):
    model = servicio
    template_name = 'tests/listar_servicio.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in servicio.objects.filter(estado=False):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Servicios'
        context['create_url'] = reverse_lazy('core:test')
        context['list_url'] = reverse_lazy('core:listar_servicio')
        context['entity'] = 'Servicios'
        context['form'] = ServicioForm()
        return context


class estadoUpdate(UpdateView):
    model = servicio
    form_class = ServicioForm
    template_name = 'tests/cambio_estado.html'
    success_url = reverse_lazy('core:listar_servicio')
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
        data = serializers.serialize('json', self.get_queryset())
        return HttpResponse(data, content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Terminar Servicio'
        context['list_url'] = self.success_url
        context['action'] = 'edit'

        return context

class ServicioListView1(ListView):
    model = servicio
    template_name = 'tests/listar_servicio_imprimir.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in servicio.objects.filter(estado=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Servicios'
        context['create_url'] = reverse_lazy('core:test1')
        context['list_url'] = reverse_lazy('core:listar_servicio_imprimir')
        context['entity'] = 'Servicios'
        context['form'] = ServicioForm()
        return context

class ServicioInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('tests/invoice.html')
            context = {
                'servicio': servicio.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'TECNICENTRO JIMENEZ', 'ruc': '9999999999999', 'address': '24 de Mayo, Macas-Ecuador'},

            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('core:listar_venta'))