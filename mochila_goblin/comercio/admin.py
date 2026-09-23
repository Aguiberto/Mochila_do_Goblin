from django.contrib import admin
from .models import Item

# Register your models here.

@admin.register(Item)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','nome','estoque','preco_compra','preco_venda')
    search_fields = ('nome','descricao')
    list_fields = ('quantidade_estoque',)
    readonly_fields = ('preco_venda',)

