from .models import Transacao
from rest_framework.exceptions import ValidationError
import requests

URL_SERVICO_MOCHILA = "http://localhost:8002/api/v1/atualizar/"

class Services():

    @staticmethod
    def comprar_item(item, qtd_solicitada, aventureiro, auth_header):

        # validação de estoque
        if item.estoque < qtd_solicitada:
            raise ValidationError("Estoque insuficiente, ja vendemos tudo!")

        custo_total = item.preco_venda * qtd_solicitada

        # averiguando se o comprador tem dinheiro suficiente
        if aventureiro.moedas_draconicas < custo_total:
            raise ValidationError(" Moedas insulficiente, vá caçar ou buscar espólios!")

        # Envia o token para o Ver Mochila Service (:8002) saber de quem é a mochila!
        headers = {'Authorization': auth_header}
        payload = {
            'item_id': item.id,
            'nome_item': item.nome,
            'quantidade': qtd_solicitada,
            'operacao': 'ADICIONAR'
        }
        try:
            res = requests.post(URL_SERVICO_MOCHILA, json=payload, headers=headers, timeout=5)
        except requests.exceptions.RequestException:
            raise ValidationError("Serviço 'Ver Mochila' indisponível no momento.")

        if res.status_code != 200:
            try:
                dados_erro = res.json()
            except requests.exceptions.JSONDecodeError:
                dados_erro = {}
            mensagem = dados_erro.get("erro", dados_erro.get("detail", "Não foi possível atualizar a mochila."))
            raise ValidationError(mensagem)
        
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

        return f"Compra realizada com sucesso! Volte sempre!"

    @staticmethod
    def vender_item(item, qtd_solicitada, aventureiro, auth_header):

        # 1. Solicita a remoção do item da mochila (Porta :8002) PRIMEIRO
        payload = {
            'item_id': item.id,
            'nome_item': item.nome,
            'quantidade': qtd_solicitada,
            'operacao': 'REMOVER'
        }
        headers = {'Authorization': auth_header}

        try:
            res = requests.post(URL_SERVICO_MOCHILA, json=payload, headers=headers, timeout=5)
            if res.status_code != 200:
                dados_erro = res.json()
                msg_erro = dados_erro.get("erro", "Você não possui essa quantidade do item na mochila.")
                raise ValidationError(msg_erro)
        except requests.exceptions.RequestException:
            raise ValidationError("Serviço 'Ver Mochila' indisponível no momento.")

        # 2. Calcula o valor a receber (usando o preço de venda do item)
        valor_recebido = item.preco_venda * qtd_solicitada

        # 3. Credita as moedas dracônicas para o aventureiro
        aventureiro.moedas_draconicas += valor_recebido
        aventureiro.save()

        # 4. Devolve o item ao estoque do Goblin
        item.estoque += qtd_solicitada
        item.save()

        # 5. Registra a transação de Venda
        Transacao.objects.create(
            aventureiro=aventureiro,
            item=item,
            quantidade=qtd_solicitada,
            tipo='VENDA',
            valor_total=valor_recebido
        )

        return valor_recebido