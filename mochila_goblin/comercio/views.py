from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from .serializers import OperacaoSerializer
from .models import Aventureiro, Item
from .services import Services



# Create your views here.

class CompraItemView(APIView):

    '''
    Realiza o processamento da compra de um item
    '''
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=OperacaoSerializer,
        responses={
            200: inline_serializer(
                name='CompraItemResponse',
                fields={
                    'mensagem': serializers.CharField(),
                    'saldo': serializers.DecimalField(max_digits=10, decimal_places=2),
                    'estoque_goblin': serializers.IntegerField(),
                },
            ),
            400: inline_serializer(
                name='CompraItemErrorResponse',
                fields={'erro': serializers.CharField()},
            ),
        },
    )
    @transaction.atomic
    def post(self,request):

        serializer = OperacaoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item_id = serializer.validated_data['item_id']
        qtd_itens = serializer.validated_data['quantidade']

        aventureiro,_ = Aventureiro.objects.get_or_create(usuario=request.user)
        item = get_object_or_404(Item, pk=item_id)
        auth_header = request.headers.get('Authorization')

        try:
            Services.comprar_item(item, qtd_itens, aventureiro, auth_header)
            return Response({"mensagem": "Compra realizada com sucesso!",
                             "saldo": aventureiro.moedas_draconicas,
                             "estoque_goblin": item.estoque},
                             status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"erro": str(e.detail)},status=status.HTTP_400_BAD_REQUEST)
        
        
class VendaItemView(APIView):

    '''
    Realiza o processamento da venda de um item do aventureiro para o goblin
    '''
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=OperacaoSerializer,
        responses={
            200: inline_serializer(
                name='VendaItemResponse',
                fields={
                    'mensagem': serializers.CharField(),
                    'moedas_recebidas': serializers.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                    ),
                    'saldo': serializers.DecimalField(max_digits=10, decimal_places=2),
                    'estoque_goblin': serializers.IntegerField(),
                },
            ),
            400: inline_serializer(
                name='VendaItemErrorResponse',
                fields={'erro': serializers.CharField()},
            ),
        },
    )
    @transaction.atomic
    def post(self, request):

        serializer = OperacaoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item_id = serializer.validated_data['item_id']
        qtd_itens = serializer.validated_data['quantidade']

        aventureiro, _ = Aventureiro.objects.get_or_create(usuario=request.user)
        item = get_object_or_404(Item, pk=item_id)
        auth_header = request.headers.get('Authorization')

        try:
            valor_recebido = Services.vender_item(item, qtd_itens, aventureiro, auth_header)
            return Response({
                "mensagem": "Venda realizada com sucesso!",
                "moedas_recebidas": valor_recebido,
                "saldo": aventureiro.moedas_draconicas,
                "estoque_goblin": item.estoque
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"erro": e.detail[0] if isinstance(e.detail, list) else str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
