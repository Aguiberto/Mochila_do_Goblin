import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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