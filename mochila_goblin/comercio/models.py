from django.db import models
from decimal import Decimal

# Create your models here.

class Item(models.Model):

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True help_text="Descrição do item")
    estoque = models.PositiveBigIntegerField(default=0)
    preco_compra = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Valor pago para compra o item")


    @property
    def preco_venda(self) -> Decimal:

        '''
        O valor do item vai 10% na sua venda
        '''

        fator = Decimal("0.90")
        return (self.preco_compra * fator).quantize(Decimal("0.01"))    

    def __str__(self):
            return f"Nome: {self.nome} | Estoque: {self.estoque}"