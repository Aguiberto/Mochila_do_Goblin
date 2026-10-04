from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

# Create your models here.

class Aventureiro(models.Model):

    usuario = models.OneToOneField(User, on_delete = models.CASCADE, related_name='aventureiro')
    moedas_draconicas = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("1000.00"),
    )

    def __str__(self):
        return f"Nome: {self.usuario} | Saldo:{self.moedas_draconicas}"

class Item(models.Model):

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True, help_text="Descrição do item")
    estoque = models.PositiveBigIntegerField(default=0)
    preco_compra = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Valor pago para compra o item")
    preco_venda = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Valor da         item = models.ForeignKey(Item, on_delete=models.PROTECT)venda do item")


    @property
    def preco_venda(self) -> Decimal:

        '''
        O valor do item vai 10% na sua venda
        '''
        if self.preco_compra is None:
            return Decimal("0.00")

        fator = Decimal("0.90") 
        return (self.preco_compra * fator).quantize(Decimal("0.01"))    

    def __str__(self):
        return f"Nome: {self.nome} | Estoque: {self.estoque}"


class Transacao(models.Model):

    CHOICES = [
        ('COMPRA',  'Compra'),
        ('VENDA', 'Venda'),
    ]

    aventureiro = models.ForeignKey(Aventureiro, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=6, choices=CHOICES)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"TIPO: {self.tipo} | ITEM: {self.item.nome} | ESTOQUE: {self.quantidade}"
