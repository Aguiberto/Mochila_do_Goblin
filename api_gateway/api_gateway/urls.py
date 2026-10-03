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

    # Rotas proxy para os Microserviços
    #path('api/v1/loja/<path:path>', ProxyNegociarView.as_view(), name = 'proxy_negociar' ),
    #path('api/v1/mochila<path:path>',ProxyVerMochila.as_view(),name = 'proxy_mochila'),
    
    
    # Repassa pedidos de LOGIN para o Negociar Service(mochila_goblin)  (:8001)
    path('api/v1/<path:path>', ProxyNegociarView.as_view(), name='proxy_auth'),

    # Repassa LOJA para o Negociar Service(mochila_goblin) (:8001)
    path('api/v1/loja/<path:path>', ProxyNegociarView.as_view(), name='proxy_negociar'),

    # Repassa MOCHILA para o Ver o Inventario (:8002) 
    path('api/v1/mochila/<path:path>', ProxyInventario.as_view(), name='proxy_inventario'),

]
