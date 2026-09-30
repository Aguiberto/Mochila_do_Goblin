import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

NEGOCIAR_SERVICE_URL = "http://localhost:8001"
MOCHILA_SERVICE_URL = "http://localhost:8002"

class ProxyNegociarView(APIView):

    '''
    Redireciona a requisição para a view de negociar
    1. concatena a cria uma rota para o serviço que o usuário deseja
    2. copia os dados da requisição do usuário (cabeçalho).

    '''
    permission_classes = [IsAuthenticated]

    def get(self,request, path=""):

        # Cria a nova URL para o serviço desejado
        url=f"{NEGOCIAR_SERVICE_URL}/api/v1/loja/{path}"

        # Copia o cabeçalho da requisição (onde fica o token jwt)
        headers = {'Authorization':request.headers.get('Authorization')}

        # resposta que vai ser enviado para o microserviço
        response = request.get(url, headers=headers, params=request.query_params)
        return Response(response.json(), status=response.status_code)

    def post(self,request,path=""):

        # Cria a nova URL para o serviço desejado
        url=f"{NEGOCIAR_SERVICE_URL}/api/v1/loja/{path}"

        # Captura e repassao token JWT
        headers = {'Authorization':request.headers.get('Authorization')}

        # cria a resposta a ser repassada
        response = request.post(url, headers = headers, json=request.data)
        return Response(response.json(), status=response.status_code)

class ProxyVerMochila(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, path=""):

        url = f"{MOCHILA_SERVICE_URL}/api/v1/{path}"
        headers = {"Authorization": request.headers.get('Authorization')}

        response = request.get(url, headers=headers, parms=request.query_params)
        return Response(response.json(),status=response.status_code)
