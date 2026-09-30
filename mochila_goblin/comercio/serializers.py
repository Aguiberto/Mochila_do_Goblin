from rest_framework import serializers
from . models import Item, Aventureiro

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

class OperacaoSerializer(serializers.Serializer):

    '''Serializer apenas para enviar os dados de que item 
    e quantidade que o usuário deseja negociar
    '''
   
    item_id = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1, default=1)

class AventureiroSerializer(serializers.ModelSerializer):

    nome = serializers.CharField(source = 'usuario.username', read_only = True)

    class Meta:
        model = Aventureiro
        fields = [
            'id',
            'nome',
            'moedas_draconianas'
        ]