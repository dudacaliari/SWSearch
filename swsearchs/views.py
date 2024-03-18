# views.py
from django.shortcuts import render, redirect
from django.db import connection
import os

def index(request):
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
                INTO TABLE imovel
                FIELDS TERMINATED BY ',' 
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 LINES;  -- Ignora a primeira linha se ela for cabeçalho
            """)
        
        # Remover o arquivo temporário após carregar os dados
        os.remove(caminho_arquivo)
    
    return render(request, 'index.html')
