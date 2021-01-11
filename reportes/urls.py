from django.urls import path

from reportes.views import *

urlpatterns = [
    # reports
    path('venta/', ReportSaleView.as_view(), name='sale_report'),
    path('producto/', ReportProductView, name='producto_report'),
]