from django.db import models
from django.utils import timezone

class Bebidas(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    preco_unitario = models.FloatField(default=0.0, verbose_name="Preço Unitário")

    def __str__(self):
        return self.nome

class Venda(models.Model):
    id_venda = models.AutoField(primary_key=True)  # Campo auto-incremental para ID da venda
    produto = models.ForeignKey(Bebidas, on_delete=models.CASCADE, verbose_name="Nome")
    quantidade = models.IntegerField()
    data_venda = models.DateField(default=timezone.now)
    hora_venda = models.TimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Acessando o nome e o preço unitário diretamente do produto relacionado
        self.preco_unitario = self.produto.preco_unitario
        self.nome = self.produto.nome
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda #{self.id_venda} de {self.quantidade} unidades de {self.nome} em {self.data_venda} às {self.hora_venda}"
