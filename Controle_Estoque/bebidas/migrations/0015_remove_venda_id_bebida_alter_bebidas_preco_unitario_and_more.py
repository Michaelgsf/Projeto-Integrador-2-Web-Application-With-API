# Generated by Django 4.2.6 on 2023-10-29 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bebidas', '0014_remove_venda_id_venda_id_venda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='id_bebida',
        ),
        migrations.AlterField(
            model_name='bebidas',
            name='preco_unitario',
            field=models.FloatField(default=0.0, verbose_name='Preço Unitário'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='nome',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bebidas.bebidas'),
        ),
    ]
