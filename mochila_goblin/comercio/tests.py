from decimal import Decimal
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Aventureiro
from .services import Services


class ComercioMonetaryTypeTests(TestCase):
    @patch("comercio.services.Transacao.objects.create")
    @patch("comercio.services.requests.post")
    def test_compra_e_venda_usam_saldo_decimal(self, mock_post, _mock_transaction):
        mock_post.return_value = Mock(status_code=200)

        usuario = User.objects.create_user(username="aventureiro-teste")
        aventureiro, created = Aventureiro.objects.get_or_create(usuario=usuario)
        item = Mock(
            id=1,
            nome="Poção de teste",
            estoque=5,
            preco_venda=Decimal("9.00"),
        )
        item.save = Mock()

        self.assertTrue(created)
        self.assertIsInstance(aventureiro.moedas_draconicas, Decimal)
        self.assertEqual(aventureiro.moedas_draconicas, Decimal("1000.00"))

        Services.comprar_item(item, 1, aventureiro, "Bearer token-teste")
        aventureiro.refresh_from_db()
        self.assertEqual(aventureiro.moedas_draconicas, Decimal("991.00"))
        self.assertEqual(item.estoque, 4)

        Services.vender_item(item, 1, aventureiro, "Bearer token-teste")
        aventureiro.refresh_from_db()
        self.assertEqual(aventureiro.moedas_draconicas, Decimal("1000.00"))
        self.assertEqual(item.estoque, 5)
