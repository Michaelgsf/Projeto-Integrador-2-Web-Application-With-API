from django.db import models

class Bebidas(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    preco = models.FloatField(default=0.0)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    id_bebida = models.ForeignKey(Bebidas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)  # Atualizado para usar max_length
    quantidade = models.IntegerField()
    preco = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        # Ao salvar a venda, obtenha o preço unitário correspondente da tabela Bebidas
        self.preco = self.id_bebida.preco
        self.nome = self.id_bebida.nome  # O nome será o mesmo da bebida associada
        # Calcule o total com base no preço unitário e na quantidade
        # self.total = self.preco * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda de {self.quantidade} unidades de {self.nome}"
