# Generated by Django 4.1.1 on 2023-10-24 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bebidas', '0009_rename_nome_bebida_venda_id_bebida'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='nome',
            field=models.CharField(default='Valor_Padrao', max_length=100),
        ),
    ]
