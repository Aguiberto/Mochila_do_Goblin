from rest_framework import serializers
from . models import Item

class ItemSerializer(serializers.ModelSerializer):

    preco_venda = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Item
        fields = [
            'id',
            'nome',
            'descricao'
            'estoque'
            'preco_venda'
        ]

class OperacaoItemSerializer(serializers.Serializer):
    '''
    Serializer para receber a quantidade nas operações de compra/venda"
    '''

    quantidade = serializers.IntegerField(min_value=1, default=1)
    