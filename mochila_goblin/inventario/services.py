from rest_framework.exceptions import ValidationError
from .models import ItemMochila


class MochilaServices:

    @staticmethod
    def atualizar_inventario(usuario, item_id, nome_item, qtd, operacao):
        item_mochila, _ = ItemMochila.objects.get_or_create(
            usuario=usuario,
            item_id_loja=item_id,
            defaults={'nome_item': nome_item, 'quantidade': 0}
        )

        if operacao == 'ADICIONAR':
            item_mochila.quantidade += qtd
            item_mochila.save()
            return f"{qtd}x {nome_item} adicionado(s) à mochila!"

        elif operacao == 'REMOVER':
            if item_mochila.quantidade < qtd:
                raise ValidationError(f"Aventureiro possui apenas {item_mochila.quantidade} unidade(s) deste item.")

            item_mochila.quantidade -= qtd
            item_mochila.save()
            return f"{qtd}x {nome_item} removido(s) da mochila!"