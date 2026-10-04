from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from .models import ItemMochila
from .views import AtualizarMochilaView, ConsultarMochilaView


class MochilaAPITests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.usuario_id = 987654
        self.token = AccessToken()
        self.token["user_id"] = self.usuario_id

    def _auth_header(self):
        return f"Bearer {self.token}"

    def test_lista_somente_itens_do_usuario_do_token(self):
        proprio = ItemMochila.objects.create(
            usuario_id=self.usuario_id,
            item_id_loja=12,
            nome_item="Poção",
            quantidade=3,
        )
        ItemMochila.objects.create(
            usuario_id=self.usuario_id + 1,
            item_id_loja=13,
            nome_item="Escudo",
            quantidade=2,
        )
        request = self.factory.get("/", HTTP_AUTHORIZATION=self._auth_header())

        response = ConsultarMochilaView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], proprio.id)
        self.assertEqual(response.data[0]["item_id_loja"], 12)
        self.assertFalse(User.objects.filter(pk=self.usuario_id).exists())

    def test_adiciona_item_do_usuario_do_token(self):
        request = self.factory.post(
            "/atualizar/",
            {
                "item_id": 12,
                "nome_item": "Poção",
                "quantidade": 2,
                "operacao": "ADICIONAR",
            },
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(),
        )

        response = AtualizarMochilaView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        item = ItemMochila.objects.get(
            usuario_id=self.usuario_id,
            item_id_loja=12,
        )
        self.assertEqual(item.quantidade, 2)
        self.assertFalse(User.objects.filter(pk=self.usuario_id).exists())

    def test_remove_item_somente_da_mochila_do_usuario_do_token(self):
        ItemMochila.objects.create(
            usuario_id=self.usuario_id,
            item_id_loja=12,
            nome_item="Poção",
            quantidade=3,
        )
        outro_usuario = ItemMochila.objects.create(
            usuario_id=self.usuario_id + 1,
            item_id_loja=12,
            nome_item="Poção",
            quantidade=4,
        )
        request = self.factory.post(
            "/atualizar/",
            {
                "item_id": 12,
                "nome_item": "Poção",
                "quantidade": 2,
                "operacao": "REMOVER",
            },
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(),
        )

        response = AtualizarMochilaView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            ItemMochila.objects.get(
                usuario_id=self.usuario_id,
                item_id_loja=12,
            ).quantidade,
            1,
        )
        outro_usuario.refresh_from_db()
        self.assertEqual(outro_usuario.quantidade, 4)

    def test_rejeita_remocao_acima_da_quantidade_disponivel(self):
        ItemMochila.objects.create(
            usuario_id=self.usuario_id,
            item_id_loja=12,
            nome_item="Poção",
            quantidade=1,
        )
        request = self.factory.post(
            "/atualizar/",
            {
                "item_id": 12,
                "nome_item": "Poção",
                "quantidade": 2,
                "operacao": "REMOVER",
            },
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(),
        )

        response = AtualizarMochilaView.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            ItemMochila.objects.get(
                usuario_id=self.usuario_id,
                item_id_loja=12,
            ).quantidade,
            1,
        )

    def test_rejeita_quantidade_zero_operacao_invalida_e_token_invalido(self):
        payload = {
            "item_id": 12,
            "nome_item": "Poção",
            "quantidade": 0,
            "operacao": "ADICIONAR",
        }
        request = self.factory.post(
            "/atualizar/",
            payload,
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(),
        )
        response = AtualizarMochilaView.as_view()(request)
        self.assertEqual(response.status_code, 400)

        payload["quantidade"] = 1
        payload["operacao"] = "TROCAR"
        request = self.factory.post(
            "/atualizar/",
            payload,
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(),
        )
        response = AtualizarMochilaView.as_view()(request)
        self.assertEqual(response.status_code, 400)

        request = self.factory.get("/", HTTP_AUTHORIZATION="Bearer token.invalido")
        response = ConsultarMochilaView.as_view()(request)
        self.assertEqual(response.status_code, 401)


class MochilaURLTests(TestCase):
    def test_rotas_de_consulta_e_atualizacao_resolvem(self):
        consulta = resolve("/api/v1/")
        atualizacao = resolve("/api/v1/atualizar/")

        self.assertEqual(consulta.url_name, "mochila-consultar")
        self.assertIs(consulta.func.view_class, ConsultarMochilaView)
        self.assertEqual(atualizacao.url_name, "mochila-atualizar")
        self.assertIs(atualizacao.func.view_class, AtualizarMochilaView)

    def test_tela_de_inventario_abre_sem_autenticacao(self):
        response = self.client.get("/api/v1/tela/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mochila do Aventureiro")
        self.assertContains(response, "/api/v1/mochila/")
