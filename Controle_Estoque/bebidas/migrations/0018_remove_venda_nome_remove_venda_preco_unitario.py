# Generated by Django 4.2.6 on 2023-10-29 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bebidas', '0017_alter_venda_id_bebida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='preco_unitario',
        ),
    ]
