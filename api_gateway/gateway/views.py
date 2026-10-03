import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .schema import (
    AtualizarMochilaRequestSerializer,
    AuthenticationErrorResponseSerializer,
    CompraResponseSerializer,
    ErroResponseSerializer,
    ItemMochilaResponseSerializer,
    MensagemResponseSerializer,
    OperacaoLojaRequestSerializer,
    TokenObtainRequestSerializer,
    TokenPairResponseSerializer,
    TokenRefreshRequestSerializer,
    TokenRefreshResponseSerializer,
    ValidationErrorResponseSerializer,
    VendaResponseSerializer,
)

NEGOCIAR_SERVICE_URL = "http://localhost:8001"
MOCHILA_SERVICE_URL = "http://localhost:8002"


class ProxyNegociarView(APIView):
    """
    Redireciona a requisição para o serviço de negociação (:8001)
    """
    authentication_classes = []
    permission_classes = []  # A validação da autenticação fica a cargo do serviço :8001

    def get(self, request, path=""):
        url = f"{NEGOCIAR_SERVICE_URL}/api/v1/{path}"
        headers = {'Authorization': request.headers.get('Authorization', '')}

        try:
            # Correção: usa a biblioteca requests.get e não o request do Django
            res = requests.get(url, headers=headers, params=request.query_params)
            return Response(res.json(), status=res.status_code)
        except requests.exceptions.RequestException:
            return Response({"erro": "Serviço 'Negociar' indisponível."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def post(self, request, path=""):
        url = f"{NEGOCIAR_SERVICE_URL}/api/v1/{path}"
        headers = {'Authorization': request.headers.get('Authorization', '')}

        try:
            # Correção: usa requests.post
            res = requests.post(url, headers=headers, json=request.data)
            return Response(res.json(), status=res.status_code)
        except requests.exceptions.RequestException:
            return Response({"erro": "Serviço 'Negociar' indisponível."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ProxyInventario(APIView):
    """
    Redireciona a requisição para o serviço da mochila (:8002)
    """
    authentication_classes = []
    permission_classes = []  # A validação do JWT fica a cargo do serviço :8002

    def get(self, request, path=""):
        url = f"{MOCHILA_SERVICE_URL}/api/v1/{path}"
        headers = {'Authorization': request.headers.get('Authorization', '')}

        try:
            # Correção: usa requests.get e corrige o typo 'parms' -> 'params'
            res = requests.get(url, headers=headers, params=request.query_params)
            return Response(res.json(), status=res.status_code)
        except requests.exceptions.RequestException:
            return Response({"erro": "Serviço 'Ver Mochila' indisponível."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def post(self, request, path=""):
        url = f"{MOCHILA_SERVICE_URL}/api/v1/{path}"
        headers = {'Authorization': request.headers.get('Authorization', '')}

        try:
            res = requests.post(url, headers=headers, json=request.data)
            return Response(res.json(), status=res.status_code)
        except requests.exceptions.RequestException:
            return Response({"erro": "Serviço 'Ver Mochila' indisponível."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ProxyTokenView(ProxyNegociarView):
    http_method_names = ["post", "options"]
    serializer_class = TokenObtainRequestSerializer

    @extend_schema(
        operation_id="obter_tokens",
        summary="Obter tokens de acesso e refresh",
        request=TokenObtainRequestSerializer,
        responses={
            200: TokenPairResponseSerializer,
            401: AuthenticationErrorResponseSerializer,
        },
        auth=[],
    )
    def post(self, request):
        return super().post(request, path="token/")


class ProxyTokenRefreshView(ProxyNegociarView):
    http_method_names = ["post", "options"]
    serializer_class = TokenRefreshRequestSerializer

    @extend_schema(
        operation_id="renovar_access_token",
        summary="Renovar token de acesso",
        request=TokenRefreshRequestSerializer,
        responses={
            200: TokenRefreshResponseSerializer,
            401: AuthenticationErrorResponseSerializer,
        },
        auth=[],
    )
    def post(self, request):
        return super().post(request, path="token/refresh/")


class ProxyCompraView(ProxyNegociarView):
    http_method_names = ["post", "options"]
    serializer_class = OperacaoLojaRequestSerializer

    @extend_schema(
        operation_id="comprar_item",
        summary="Comprar item na loja",
        request=OperacaoLojaRequestSerializer,
        responses={
            200: CompraResponseSerializer,
            400: ValidationErrorResponseSerializer,
            401: AuthenticationErrorResponseSerializer,
            503: ErroResponseSerializer,
        },
    )
    def post(self, request):
        return super().post(request, path="comprar/")


class ProxyVendaView(ProxyNegociarView):
    http_method_names = ["post", "options"]
    serializer_class = OperacaoLojaRequestSerializer

    @extend_schema(
        operation_id="vender_item",
        summary="Vender item para a loja",
        request=OperacaoLojaRequestSerializer,
        responses={
            200: VendaResponseSerializer,
            400: ValidationErrorResponseSerializer,
            401: AuthenticationErrorResponseSerializer,
            503: ErroResponseSerializer,
        },
    )
    def post(self, request):
        return super().post(request, path="venda/")


class ProxyConsultarMochilaView(ProxyInventario):
    http_method_names = ["get", "options"]
    serializer_class = ItemMochilaResponseSerializer

    @extend_schema(
        operation_id="consultar_mochila",
        summary="Consultar mochila do usuário autenticado",
        responses={
            200: ItemMochilaResponseSerializer(many=True),
            401: AuthenticationErrorResponseSerializer,
            503: ErroResponseSerializer,
        },
    )
    def get(self, request):
        return super().get(request, path="")


class ProxyAtualizarMochilaView(ProxyInventario):
    http_method_names = ["post", "options"]
    serializer_class = AtualizarMochilaRequestSerializer

    @extend_schema(
        operation_id="atualizar_mochila",
        summary="Adicionar ou remover itens da mochila",
        request=AtualizarMochilaRequestSerializer,
        responses={
            200: MensagemResponseSerializer,
            400: ValidationErrorResponseSerializer,
            401: AuthenticationErrorResponseSerializer,
            503: ErroResponseSerializer,
        },
    )
    def post(self, request):
        return super().post(request, path="atualizar/")