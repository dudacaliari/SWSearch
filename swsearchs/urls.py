from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('processar-csv/', views.index, name='processar_csv'),
    path('pesquisar/', views.pesquisar_imoveis, name='pesquisar_imoveis'),
]