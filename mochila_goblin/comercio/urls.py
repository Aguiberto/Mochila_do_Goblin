from django.urls import path
from .views import CompraItemView,VendaItemView


urlpatterns = [
    path('compra/',CompraItemView.as_view(), name='compra'),
    path('venda/', VendaItemView.as_view(), name='venda'),
]