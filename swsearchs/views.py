# views.py
from django.shortcuts import render, redirect
from django.db import connection
import os
from .models import imovel

def index(request):

    arquivo_carregado = False  # Definindo a variável antes do bloco condicional

    # Se o formulário for submetido
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Salvar o arquivo temporariamente no servidor
        caminho_arquivo = 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/temporario.csv'
        with open(caminho_arquivo, 'wb+') as destino:
            for chunk in csv_file.chunks():
                destino.write(chunk)
        
        # Carregar os dados do arquivo CSV na tabela MySQL usando o Django ORM
        with connection.cursor() as cursor:
            cursor.execute(f"""
                LOAD DATA INFILE '{caminho_arquivo}'
                REPLACE INTO TABLE imovel
                FIELDS TERMINATED BY ',' 
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 LINES;  -- Ignora a primeira linha se ela for cabeçalho
            """)
        
        # Remover o arquivo temporário após carregar os dados
        os.remove(caminho_arquivo)
        
        # Redirecionar para a página de pesquisa após o carregamento bem-sucedido
        return redirect('pesquisar_imoveis')

    # Renderizar o template com a variável arquivo_carregado
    return render(request, 'index.html', {'arquivo_carregado': arquivo_carregado})

def pesquisar_imoveis(request):
    selected_filter = request.GET.get('filter', 'id')  # Padrão para 'id' se não especificado
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET.get('q')
        filter_field = request.GET.get('filter')  # Obter o filtro selecionado pelo usuário

        # Construir a query de filtro dinâmica com base no campo selecionado
        filter_query = {f'{filter_field}__icontains': query}

        # Aplicar o filtro
        imoveis = imovel.objects.filter(**filter_query)

    else:
        imoveis = imovel.objects.all()

    return render(request, 'pesquisar_imoveis.html', {'imoveis': imoveis, 'selected_filter': selected_filter})