from django.urls import path

from .views import AtualizarMochilaView, ConsultarMochilaView


urlpatterns = [
    path("", ConsultarMochilaView.as_view(), name="mochila-consultar"),
    path("atualizar/", AtualizarMochilaView.as_view(), name="mochila-atualizar"),
]
