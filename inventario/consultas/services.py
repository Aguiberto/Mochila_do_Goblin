from rest_framework.exceptions import ValidationError

from .models import ItemMochila


MAX_QUANTIDADE = 2_147_483_647


class MochilaServices:
    @staticmethod
    def atualizar_inventario(usuario_id, item_id, nome_item, quantidade, operacao):
        if operacao == "ADICIONAR":
            item, _ = ItemMochila.objects.get_or_create(
                usuario_id=usuario_id,
                item_id_loja=item_id,
                defaults={"nome_item": nome_item, "quantidade": 0},
            )
            nova_quantidade = item.quantidade + quantidade
            if nova_quantidade > MAX_QUANTIDADE:
                raise ValidationError(
                    "A quantidade total deste item excede o limite permitido."
                )

            item.nome_item = nome_item
            item.quantidade = nova_quantidade
            item.save(update_fields=["nome_item", "quantidade"])
            return f"{quantidade}x {nome_item} adicionado(s) à mochila!"

        item = (
            ItemMochila.objects.select_for_update()
            .filter(usuario_id=usuario_id, item_id_loja=item_id)
            .first()
        )
        quantidade_disponivel = item.quantidade if item else 0
        if quantidade_disponivel < quantidade:
            raise ValidationError(
                f"Aventureiro possui apenas {quantidade_disponivel} "
                "unidade(s) deste item."
            )

        item.quantidade -= quantidade
        item.nome_item = nome_item
        item.save(update_fields=["nome_item", "quantidade"])
        return f"{quantidade}x {nome_item} removido(s) da mochila!"
