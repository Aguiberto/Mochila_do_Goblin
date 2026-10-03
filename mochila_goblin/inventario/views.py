from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import ItemMochila
from .serializers import ItemMochilaSerializer, AtualizarMochilaSerializer
from .services import MochilaServices


class ConsultarMochilaView(APIView):
    """Listar os itens da mochila do Aventureiro autenticado"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        itens = ItemMochila.objects.filter(usuario=request.user, quantidade__gt=0)
        serializer = ItemMochilaSerializer(itens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AtualizarMochilaView(APIView):
    """Recebe chamadas de COMPRA ou VENDA do Negociar Service"""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = AtualizarMochilaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item_id = serializer.validated_data['item_id']
        nome_item = serializer.validated_data['nome_item']
        qtd = serializer.validated_data['quantidade']
        operacao = serializer.validated_data['operacao']

        try:
            mensagem = MochilaServices.atualizar_inventario(
                usuario=request.user,
                item_id=item_id,
                nome_item=nome_item,
                qtd=qtd,
                operacao=operacao
            )
            return Response({"mensagem": mensagem}, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"erro": e.detail[0] if isinstance(e.detail, list) else str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"erro": "Erro ao atualizar a mochila."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)