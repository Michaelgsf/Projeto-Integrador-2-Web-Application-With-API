# Generated by Django 4.1.1 on 2023-10-24 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bebidas', '0005_venda_preco_alter_bebidas_preco'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='total',
            field=models.FloatField(default=0.0),
        ),
    ]
