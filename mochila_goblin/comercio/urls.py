from django.urls import path
from .views import CompraItemView,VendaItemView


urlpatterns = [
    path('comprar/',CompraItemView.as_view(), name='comprar'),
    path('venda/', VendaItemView.as_view(), name='venda'),
]