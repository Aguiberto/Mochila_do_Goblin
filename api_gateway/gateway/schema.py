from rest_framework import serializers


class TokenObtainRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class TokenPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenRefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class OperacaoLojaRequestSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1, default=1)


class CompraResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField()
    saldo = serializers.DecimalField(max_digits=12, decimal_places=2)
    estoque_goblin = serializers.IntegerField()


class VendaResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField()
    moedas_recebidas = serializers.DecimalField(max_digits=10, decimal_places=2)
    saldo = serializers.DecimalField(max_digits=12, decimal_places=2)
    estoque_goblin = serializers.IntegerField()


class ErroResponseSerializer(serializers.Serializer):
    erro = serializers.CharField()


class AuthenticationErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField(required=False)


class ValidationErrorResponseSerializer(serializers.Serializer):
    detail = serializers.JSONField(required=False)


class ItemMochilaResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    item_id_loja = serializers.IntegerField()
    nome_item = serializers.CharField()
    quantidade = serializers.IntegerField()


class AtualizarMochilaRequestSerializer(serializers.Serializer):
    OPERACAO_CHOICES = [
        ("ADICIONAR", "Adicionar"),
        ("REMOVER", "Remover"),
    ]

    item_id = serializers.IntegerField(min_value=1)
    nome_item = serializers.CharField(max_length=100)
    quantidade = serializers.IntegerField(min_value=1, max_value=2_147_483_647)
    operacao = serializers.ChoiceField(choices=OPERACAO_CHOICES)


class MensagemResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField()
