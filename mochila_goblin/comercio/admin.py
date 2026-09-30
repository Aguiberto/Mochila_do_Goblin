from django.contrib import admin
from .models import Item, Aventureiro, Transacao

# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','nome','estoque','preco_compra','preco_venda')
    search_fields = ('nome','descricao')
    list_fields = ('quantidade_estoque',)
    readonly_fields = ('preco_venda',)

@admin.register(Aventureiro)
class AventureitoAdmin(admin.ModelAdmin):

    list_display = ('id', 'nome', 'preco_compra', 'preco_venda', 'quantidade')
    list_editable = '(moedas_draconicas)'

@admin.register(Transacao)
class TrasacaoAdmin(admin.ModelAdmin):

    list_display = ('id','aventureito', 'tipo', 'item', 'quantidade', 'valor_total', 'data_hora')
    list_editable = ('data_hora')

