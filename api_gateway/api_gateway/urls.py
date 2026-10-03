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
from django.urls import path, include
from gateway.views import ProxyNegociarView, ProxyInventario


from drf_spectacular.views import(
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [

    path('admin/', admin.site.urls),


    #Endpoints do Swaggeer / OpenAPI 3.0
    path('api/v1/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('api/v1/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/v1/redoc/',SpectacularRedocView.as_view(url_name ='schema'), name ='redoc'),

    # Encaminha chamadas da loja, como comprar/ e venda/, ao serviço mochila_goblin.
    path('api/v1/loja/<path:path>', ProxyNegociarView.as_view(), name='proxy_negociar'),

    # Encaminha a consulta da mochila. Como não há caminho adicional, passa path=""
    # para que o inventário receba a rota interna /api/v1/.
    path(
        'api/v1/mochila/',
        ProxyInventario.as_view(),
        {'path': ''},
        name='proxy_inventario_root',
    ),

    # Encaminha operações da mochila, como atualizar/, ao serviço de inventário.
    path('api/v1/mochila/<path:path>', ProxyInventario.as_view(), name='proxy_inventario'),

    # Proxy genérico para login, refresh e demais endpoints do emissor.
    # Deve ficar por último para não capturar antes as rotas específicas acima.
    path('api/v1/<path:path>', ProxyNegociarView.as_view(), name='proxy_auth'),

]
