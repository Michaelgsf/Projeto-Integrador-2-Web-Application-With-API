# Generated by Django 4.1.1 on 2023-10-24 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bebidas', '0010_venda_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='nome',
            field=models.CharField(max_length=100),
        ),
    ]
