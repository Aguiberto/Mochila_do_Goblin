"""
URL configuration for api_gateway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gateway.views import (
    ProxyAtualizarMochilaView,
    ProxyCompraView,
    ProxyConsultarMochilaView,
    ProxyTokenRefreshView,
    ProxyTokenView,
    ProxyVendaView,
    proxy_tela_inventario,
)


from drf_spectacular.views import(
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [

    path('admin/', admin.site.urls),

    path('inventario/', proxy_tela_inventario, name='inventario-tela'),

    #Endpoints do Swaggeer / OpenAPI 3.0
    path('api/v1/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('api/v1/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/v1/redoc/',SpectacularRedocView.as_view(url_name ='schema'), name ='redoc'),

    # Login e refresh são públicos; a loja valida as credenciais e os tokens.
    path(
        'api/v1/token/',
        ProxyTokenView.as_view(),
        name='proxy_token',
    ),
    path(
        'api/v1/token/refresh/',
        ProxyTokenRefreshView.as_view(),
        name='proxy_token_refresh',
    ),

    # Operações públicas da loja, protegidas pelo access token.
    path('api/v1/loja/comprar/', ProxyCompraView.as_view(), name='proxy_comprar'),
    path('api/v1/loja/venda/', ProxyVendaView.as_view(), name='proxy_venda'),

    # Operações públicas do inventário, protegidas pelo access token.
    path(
        'api/v1/mochila/',
        ProxyConsultarMochilaView.as_view(),
        name='proxy_inventario_root',
    ),
    path(
        'api/v1/mochila/atualizar/',
        ProxyAtualizarMochilaView.as_view(),
        name='proxy_inventario_atualizar',
    ),

]
