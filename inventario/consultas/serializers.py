from rest_framework import serializers

from .models import ItemMochila


class ItemMochilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMochila
        fields = ["id", "item_id_loja", "nome_item", "quantidade"]


class AtualizarMochilaSerializer(serializers.Serializer):
    OPERACAO_CHOICES = [
        ("ADICIONAR", "Adicionar"),
        ("REMOVER", "Remover"),
    ]

    item_id = serializers.IntegerField(min_value=1)
    nome_item = serializers.CharField(max_length=100)
    quantidade = serializers.IntegerField(min_value=1, max_value=2_147_483_647)
    operacao = serializers.ChoiceField(choices=OPERACAO_CHOICES)
