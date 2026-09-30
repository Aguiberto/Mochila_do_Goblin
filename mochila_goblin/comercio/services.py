from .models import Transacao
from rest_framework.exceptions import ValidationError

class Services():

    def comprar_item(item, qtd_solicitada, aventureiro):

        # validação de estoque
        if item.estoque < qtd_solicitada:
            raise ValidationError("Estoque insuficiente, ja vendemos tudo!")

        custo_total = item.preco_venda * qtd_solicitada

        # averiguando se o comprador tem dinheiro suficiente
        if aventureiro.moedas_draconicas < custo_total:
            raise ValidationError(" Moedas insulficiente, vá caçar ou buscar espólios!")

        # atualiza o as moedas do aventureiro
        aventureiro.moedas_draconicas -= custo_total
        aventureiro.save()

        # atualiza o estoque do goblin
        item.estoque -= qtd_solicitada
        item.save()

        Transacao.objects.create(
            aventureiro = aventureiro,
            item = item,
            quantidade = qtd_solicitada,
            tipo = 'COMPRA',
            valor_total = custo_total
        )

        return f"Venda realizada com sucesso! Volte sempre!"
    