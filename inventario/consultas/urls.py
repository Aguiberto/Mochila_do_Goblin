from django.urls import path

from .views import AtualizarMochilaView, ConsultarMochilaView, tela_inventario


urlpatterns = [
    path("tela/", tela_inventario, name="inventario-tela"),
    path("", ConsultarMochilaView.as_view(), name="mochila-consultar"),
    path("atualizar/", AtualizarMochilaView.as_view(), name="mochila-atualizar"),
]
