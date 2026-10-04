from django.db import models


class ItemMochila(models.Model):
    """
    Guarda a quantidade de um item específico no inventário de um Aventureiro.
    """
    usuario_id = models.PositiveBigIntegerField(db_index=True)
    item_id_loja = models.IntegerField(help_text="ID do item no catálogo da loja")
    nome_item = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('usuario_id', 'item_id_loja')

    def __str__(self):
        return f"{self.quantidade}x {self.nome_item} (usuário {self.usuario_id})"
