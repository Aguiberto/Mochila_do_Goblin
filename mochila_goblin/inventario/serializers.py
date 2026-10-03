from rest_framework import serializers
from .models import ItemMochila


class ItemMochilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMochila
        fields = ['id', 'item_id_loja', 'nome_item', 'quantidade']


class AtualizarMochilaSerializer(serializers.Serializer):
    OPERACAO_CHOICES = [
        ('ADICIONAR', 'Adicionar'),
        ('REMOVER', 'Remover'),
    ]

    item_id = serializers.IntegerField()
    nome_item = serializers.CharField(max_length=100)
    quantidade = serializers.IntegerField(min_value=1)
    operacao = serializers.ChoiceField(choices=OPERACAO_CHOICES)