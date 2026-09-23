from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer, OperacaoItemSerializer

# Create your views here.

class ItemView(viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=True, methods=['post'], serializer_class=OperacaoItemSerializer)
    def comprar(self, request, pk=None):

        item = self.get_object()
        serializer = OperacaoItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qtd = serializer.validate_empty_values['quantidade']

        if item.estoque < qtd:
            return Response(
                {"Erro": f"Estoque insulficiente. Apenas{item.estoque} unides disponiveis"},
                status = status.HTTP_400_BAD_REQUEST
            )
        item.estoque -+ qtd
        item.save()

        total_pago = item.preco_compra * qtd

        return Responde({
            "mensagem": f"Compra de {qtd}x '{item.nome}' realizada com sucesso!",
            "valor_total_pago": float(total_pago),
            "item": ItemSerializer(item).data
        }, status=status.HTTP_200_OK)

    def vender(self, request, pk=None):

        item = self.get_object()
        serializer = OperacaoItemSerializer(data = resquest.data)
        serializer.is_valid(raise_exception = True)

        qtd = serializer.validated_data['quantidade']

        item.quantidade_estoque += qtd
        item.save()

        total_recebido = item.preco_venda * qtd

        return Response({
            "mensaem": f"Venda de {qtd}x '{item.nome}' realizada com sucesso!",
            "valor_total_recebido": float(total_recebido),
            "item": ItemSerializer(item).data
        }, status=status.HTTP_200_OK)

    