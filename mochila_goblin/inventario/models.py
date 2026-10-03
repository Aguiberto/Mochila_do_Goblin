from django.contrib.auth.models import User
from django.db import models


class ItemMochila(models.Model):
    """
    Guarda a quantidade de um item específico no inventário de um Aventureiro.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mochila')
    item_id_loja = models.IntegerField(help_text="ID do item no catálogo da loja")
    nome_item = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('usuario', 'item_id_loja')

    def __str__(self):
        return f"{self.quantidade}x {self.nome_item} ({self.usuario.username})"