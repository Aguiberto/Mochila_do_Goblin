from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from django.shortcuts import render

from .models import ItemMochila
from .serializers import ItemMochilaSerializer, AtualizarMochilaSerializer
from .services import MochilaServices


def tela_inventario(request):
    return render(request, "consultas/inventario.html")


class ConsultarMochilaView(APIView):
    """Listar os itens da mochila do Aventureiro autenticado"""
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ItemMochilaSerializer(many=True))
    def get(self, request):
        itens = ItemMochila.objects.filter(
            usuario_id=request.user.id,
            quantidade__gt=0,
        )
        serializer = ItemMochilaSerializer(itens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AtualizarMochilaView(APIView):
    """Recebe chamadas de COMPRA ou VENDA do Negociar Service"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AtualizarMochilaSerializer,
        responses={
            200: inline_serializer(
                name='AtualizarMochilaResponse',
                fields={'mensagem': serializers.CharField()},
            ),
            400: inline_serializer(
                name='AtualizarMochilaErrorResponse',
                fields={'erro': serializers.CharField()},
            ),
        },
    )
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
                usuario_id=request.user.id,
                item_id=item_id,
                nome_item=nome_item,
                quantidade=qtd,
                operacao=operacao
            )
            return Response({"mensagem": mensagem}, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"erro": e.detail[0] if isinstance(e.detail, list) else str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
