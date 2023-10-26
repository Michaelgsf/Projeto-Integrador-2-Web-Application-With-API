from django.shortcuts import render, redirect
from django.contrib import messages
from google.cloud import bigquery
import os
import sqlite3
from django.conf import settings
from .forms import BebidaForm, VendaForm
from .models import Bebidas, Venda
from google.cloud.bigquery import SchemaField

def index(request):
    users = Bebidas.objects.all()
    context = {
        'users': users
    }
    return render(request, 'index.html', context)

def cadastro(request):
    if request.method == 'GET':
        form = BebidaForm()
    else:
        form = BebidaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            if Bebidas.objects.filter(nome=nome).exists():
                messages.error(request, 'Já existe um produto com esse nome.')
            else:
                form.save()
                return redirect('index')
        else:
            messages.error(request, 'Ocorreu um erro no cadastro do produto.')
    context = {'form': form}
    return render(request, 'cadastro.html', context)

def refresh(request, bebida_id):
    bebida = Bebidas.objects.get(pk=bebida_id)
    if request.method == 'POST':
        form = BebidaForm(request.POST, instance=bebida)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BebidaForm(instance=bebida)
    context = {'form': form}
    return render(request, 'cadastro.html', context)

def delete(request, bebida_id):
    bebida = Bebidas.objects.get(pk=bebida_id)
    bebida.delete()
    return redirect('index')

def sell(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            bebida = form.cleaned_data['id_bebida']
            quantidade_vendida = form.cleaned_data['quantidade']
            if quantidade_vendida <= bebida.quantidade:
                bebida.quantidade -= quantidade_vendida
                bebida.save()
                venda = form.save()  # Salve a venda após a atualização da bebida
                # Chame a função para exportar dados para o BigQuery
                return redirect('index')
            else:
                form.add_error('quantidade', 'Quantidade insuficiente em estoque.')
                messages.error(request, 'Quantidade insuficiente em estoque.')
    else:
        form = VendaForm()
    context = {'form': form}
    return render(request, 'vendas.html', context)


def exportar_dados_bigquery(request):
    # Consulta para obter os dados da tabela "Venda"
    vendas = Venda.objects.all()

    # Configurações do BigQuery
    client = bigquery.Client()
    dataset_id = "Vendas"  # Substitua pelo ID do seu conjunto de dados no BigQuery
    table_id = "Venda"    # Substitua pelo ID da sua tabela no BigQuery

    # Defina o conjunto de dados e a tabela
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Crie uma lista de dicionários com os dados
    dados_para_enviar = [
        {"nome": venda.nome, "quantidade": venda.quantidade, "preco": venda.preco}
        for venda in vendas
    ]

    # Defina o esquema da tabela (ajuste o esquema conforme necessário)
    schema = [
        SchemaField("nome", "STRING"),
        SchemaField("quantidade", "INTEGER"),
        SchemaField("preco", "FLOAT"),
        # Adicione campos e tipos de dados conforme necessário
    ]

    # Carregue os dados na tabela
    job_config = bigquery.LoadJobConfig(schema=schema, source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)

    load_job = client.load_table_from_json(dados_para_enviar, table_ref, job_config=job_config)
    load_job.result()  # Aguarda o término do carregamento

    messages.success(request, "Dados enviados com sucesso!")

    return redirect('index')

