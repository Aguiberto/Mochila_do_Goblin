from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



# Create your views here.

class CompraItemView(APIView):

    permission_classes = [IsAuthenticated]    