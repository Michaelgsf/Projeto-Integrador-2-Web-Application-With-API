from django.shortcuts import render, redirect
from django.contrib import messages
from google.cloud import bigquery

from .forms import BebidaForm, VendaForm
from .models import Bebidas, Venda
from django.conf import settings
import pandas as pd
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
import tempfile


def index(request):
    bebidas = Bebidas.objects.all()
    context = {
        'bebidas': bebidas
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
    produtos_disponiveis = Bebidas.objects.all()
    
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            produto = form.cleaned_data['produto']
            quantidade_vendida = form.cleaned_data['quantidade']
            
            try:
                bebida = Bebidas.objects.get(pk=produto.id)
            except Bebidas.DoesNotExist:
                form.add_error('produto', 'Produto não encontrado.')
                messages.error(request, 'Produto não encontrado.')
                return render(request, 'vendas.html', {'form': form, 'produtos': produtos_disponiveis})
            
            if quantidade_vendida > 0:
                if quantidade_vendida <= bebida.quantidade:
                    data_venda = datetime.now().date()
                    hora_venda = datetime.now().time()
                    
                    bebida.quantidade -= quantidade_vendida
                    bebida.save()
                    
                    venda = Venda(
                        produto=produto,
                        quantidade=quantidade_vendida,
                        data_venda=data_venda,
                        hora_venda=hora_venda
                    )
                    venda.save()
                    
                    messages.success(request, 'Venda registrada com sucesso.')
                    return redirect('index')
                else:
                    form.add_error('quantidade', 'Quantidade insuficiente em estoque.')
                    messages.error(request, 'Quantidade insuficiente em estoque.')
            else:
                form.add_error('quantidade', 'A quantidade deve ser maior que zero.')
                messages.error(request, 'A quantidade deve ser maior que zero.')
    else:
        form = VendaForm()
    return render(request, 'vendas.html', {'form': form, 'produtos': produtos_disponiveis})


def exportar_dados_bigquery(request):
    vendas = Venda.objects.all()

    client = bigquery.Client()
    dataset_id = "Bonde_Bebidas"
    table_id = "Vendas"

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Recupere os IDs de venda já exportados para evitar duplicatas
    vendas_exportadas = set()
    query = f"SELECT id_venda FROM `{dataset_id}.{table_id}`"
    query_job = client.query(query)
    for row in query_job:
        vendas_exportadas.add(row.id_venda)

    data = []
    for venda in vendas:
        if venda.id_venda not in vendas_exportadas:
            data.append({
                "id_venda": venda.id_venda,
                "produto": venda.produto.nome,
                "quantidade": venda.quantidade,
                "data_venda": venda.data_venda.strftime('%Y-%m-%d'),
                "hora_venda": venda.hora_venda.strftime('%H:%M:%S')
            })

    if data:
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            autodetect=True,
        )

        json_data = [json.dumps(item, cls=DjangoJSONEncoder) for item in data]
        json_str = "\n".join(json_data)
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file.write(json_str)
            temp_file.close()
            with open(temp_file.name, "rb") as source_file:
                load_job = client.load_table_from_file(
                    source_file, table_ref, job_config=job_config
                )

        load_job.result()

        messages.success(request, 'Dados exportados com sucesso.')
    else:
        messages.warning(request, 'Não há novos dados para exportar.')

    return redirect('index')