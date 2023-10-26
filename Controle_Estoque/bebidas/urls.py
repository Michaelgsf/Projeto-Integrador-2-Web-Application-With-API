from django.urls import path
from . import views

from .views import index, cadastro, refresh, delete, sell, exportar_dados_bigquery

urlpatterns = [
    path('', index, name='index'),
    path('cadastro/', cadastro, name='cadastro'),
    path('vendas/', sell, name='vendas'),
    path('modificar/<int:bebida_id>', refresh, name='modificar'),
    path('deletar/<int:bebida_id>', delete, name='deletar'),
    path('exportar_dados_bigquery/', exportar_dados_bigquery, name='exportar_dados_bigquery'),
    ]
