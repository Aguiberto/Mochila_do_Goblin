from django.urls import path
from .views import CompraItemView


urlpatterns = [
    path('comprar/',CompraItemView.as_view(), name='comprar'),
]