from unittest.mock import Mock, patch

from django.test import Client, SimpleTestCase, override_settings
from django.urls import resolve
from rest_framework.test import APIRequestFactory

from .views import (
    ProxyAtualizarMochilaView,
    ProxyCompraView,
    ProxyConsultarMochilaView,
    ProxyInventario,
    ProxyNegociarView,
    ProxyTokenRefreshView,
    ProxyTokenView,
    ProxyVendaView,
    proxy_tela_inventario,
)


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


class PublicRouteMappingTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_rotas_publicas_resolvem_para_o_proxy_correto(self):
        routes = [
            ("/api/v1/token/", ProxyTokenView, "proxy_token"),
            ("/api/v1/token/refresh/", ProxyTokenRefreshView, "proxy_token_refresh"),
            ("/api/v1/loja/comprar/", ProxyCompraView, "proxy_comprar"),
            ("/api/v1/loja/venda/", ProxyVendaView, "proxy_venda"),
            ("/api/v1/mochila/", ProxyConsultarMochilaView, "proxy_inventario_root"),
            ("/api/v1/mochila/atualizar/", ProxyAtualizarMochilaView, "proxy_inventario_atualizar"),
        ]

        for path, expected_view, expected_name in routes:
            with self.subTest(path=path):
                match = resolve(path)
                self.assertEqual(match.url_name, expected_name)
                self.assertIs(match.func.view_class, expected_view)

    @patch("gateway.views.requests.get")
    def test_tela_do_inventario_encaminha_html_do_servico(self, mock_get):
        remote_response = Mock()
        remote_response.content = b"<html>Inventario</html>"
        remote_response.headers = {"Content-Type": "text/html; charset=utf-8"}
        remote_response.status_code = 200
        mock_get.return_value = remote_response

        response = proxy_tela_inventario(self.factory.get("/inventario/"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"<html>Inventario</html>")
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")
        mock_get.assert_called_once_with(
            "http://localhost:8002/api/v1/tela/",
            timeout=5,
        )

    @patch("gateway.views.requests.post")
    def test_compra_e_venda_encaminham_paths_sem_prefixo_publico(self, mock_post):
        remote_response = Mock()
        remote_response.json.return_value = {"ok": True}
        remote_response.status_code = 200
        mock_post.return_value = remote_response

        for public_path, downstream_path in (
            ("/api/v1/loja/comprar/", "comprar/"),
            ("/api/v1/loja/venda/", "venda/"),
        ):
            with self.subTest(path=public_path):
                match = resolve(public_path)
                request = self.factory.post(public_path, {}, format="json")
                response = match.func(request)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    mock_post.call_args.args[0],
                    f"http://localhost:8001/api/v1/{downstream_path}",
                )

    @patch("gateway.views.requests.get")
    def test_consulta_da_mochila_encaminha_para_raiz_interna(self, mock_get):
        remote_response = Mock()
        remote_response.json.return_value = []
        remote_response.status_code = 200
        mock_get.return_value = remote_response

        public_path = "/api/v1/mochila/"
        match = resolve(public_path)
        request = self.factory.get(public_path)
        response = match.func(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            mock_get.call_args.args[0],
            "http://localhost:8002/api/v1/",
        )

    @patch("gateway.views.requests.post")
    def test_atualizacao_da_mochila_nao_duplica_prefixo(self, mock_post):
        remote_response = Mock()
        remote_response.json.return_value = {"mensagem": "ok"}
        remote_response.status_code = 200
        mock_post.return_value = remote_response

        public_path = "/api/v1/mochila/atualizar/"
        match = resolve(public_path)
        request = self.factory.post(public_path, {}, format="json")
        response = match.func(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            mock_post.call_args.args[0],
            "http://localhost:8002/api/v1/atualizar/",
        )


class GatewayOpenAPITests(SimpleTestCase):
    def test_schema_exibe_caminhos_publicos_e_bearer_somente_nas_rotas_protegidas(self):
        from drf_spectacular.generators import SchemaGenerator

        schema = SchemaGenerator().get_schema(request=None, public=True)
        expected_paths = {
            "/api/v1/token/",
            "/api/v1/token/refresh/",
            "/api/v1/loja/comprar/",
            "/api/v1/loja/venda/",
            "/api/v1/mochila/",
            "/api/v1/mochila/atualizar/",
        }

        self.assertEqual(set(schema["paths"]), expected_paths)
        expected_methods = {
            "/api/v1/token/": {"post"},
            "/api/v1/token/refresh/": {"post"},
            "/api/v1/loja/comprar/": {"post"},
            "/api/v1/loja/venda/": {"post"},
            "/api/v1/mochila/": {"get"},
            "/api/v1/mochila/atualizar/": {"post"},
        }
        for path, methods in expected_methods.items():
            with self.subTest(path=path):
                self.assertEqual(set(schema["paths"][path]), methods)
        self.assertNotIn("security", schema["paths"]["/api/v1/token/"]["post"])
        self.assertNotIn(
            "security",
            schema["paths"]["/api/v1/token/refresh/"]["post"],
        )
        for path in expected_paths - {
            "/api/v1/token/",
            "/api/v1/token/refresh/",
        }:
            with self.subTest(path=path):
                self.assertEqual(
                    schema["paths"][path][
                        "get" if path == "/api/v1/mochila/" else "post"
                    ]["security"],
                    [{"BearerAuth": []}],
                )

        purchase_body = schema["paths"]["/api/v1/loja/comprar/"]["post"][
            "requestBody"
        ]["content"]["application/json"]["schema"]
        self.assertEqual(purchase_body["$ref"], "#/components/schemas/OperacaoLojaRequest")
        self.assertEqual(
            schema["components"]["securitySchemes"]["BearerAuth"],
            {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
        )


class AllowedHostTests(SimpleTestCase):
    @override_settings(ALLOWED_HOSTS=["localhost", "127.0.0.1", "192.0.2.10"])
    def test_client_host_is_accepted_and_unknown_host_is_rejected(self):
        client = Client()

        allowed_response = client.get("/", HTTP_HOST="192.0.2.10")
        rejected_response = client.get("/", HTTP_HOST="untrusted.example")

        self.assertEqual(allowed_response.status_code, 404)
        self.assertEqual(rejected_response.status_code, 400)
