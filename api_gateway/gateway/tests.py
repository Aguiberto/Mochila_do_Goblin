from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory

from .views import ProxyInventario, ProxyNegociarView


class ProxyAuthenticationTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.authorization = "Bearer invalid-but-forwarded"

    @patch("gateway.views.requests.get")
    def test_proxy_negociar_encaminha_header_e_status_do_servico(self, mock_get):
        response_remoto = Mock()
        response_remoto.json.return_value = {"detail": "Token inválido."}
        response_remoto.status_code = 401
        mock_get.return_value = response_remoto

        request = self.factory.get(
            "/api/v1/loja/itens/",
            HTTP_AUTHORIZATION=self.authorization,
        )
        response = ProxyNegociarView.as_view()(request, path="loja/itens/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Token inválido."})
        self.assertEqual(
            mock_get.call_args.kwargs["headers"]["Authorization"],
            self.authorization,
        )

    @patch("gateway.views.requests.get")
    def test_proxy_inventario_encaminha_header_e_status_do_servico(self, mock_get):
        response_remoto = Mock()
        response_remoto.json.return_value = {"detail": "Token inválido."}
        response_remoto.status_code = 401
        mock_get.return_value = response_remoto

        request = self.factory.get(
            "/api/v1/mochila/",
            HTTP_AUTHORIZATION=self.authorization,
        )
        response = ProxyInventario.as_view()(request, path="")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Token inválido."})
        self.assertEqual(
            mock_get.call_args.kwargs["headers"]["Authorization"],
            self.authorization,
        )
