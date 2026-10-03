# Mochila do Goblin — 

Este guia descreve como executar o cliente em um computador e os três serviços
(gateway, loja e inventário) em outro computador na mesma rede local. O cliente
acessa somente o gateway; a loja e o inventário permanecem internos ao servidor.


## Topologia e portas

| Serviço | Porta | Interface de escuta | Acesso |
| --- | ---: | --- | --- |
| Gateway | 8000 | Todas as interfaces (`0.0.0.0`) | Computadores da rede local |
| Loja (`mochila_goblin`) | 8001 | Somente local (`127.0.0.1`) | Gateway e serviços no servidor |
| Inventário | 8002 | Somente local (`127.0.0.1`) | Gateway e serviços no servidor |

O gateway encaminha as rotas da loja para `localhost:8001` e as rotas do
inventário para `localhost:8002`. A loja também chama o inventário em
`localhost:8002` ao efetuar uma compra ou venda. Esses endereços funcionam
porque os três processos rodam no mesmo servidor.

## 1. Preparar o servidor

Copie ou clone o projeto para o servidor. Na raiz `Mochila_do_Goblin/`, crie o
ambiente virtual e instale as dependências:

```bash
cd /caminho/para/Mochila_do_Goblin
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

Os demais comandos deste guia assumem que o ambiente virtual `venv` está nessa
raiz.

Gere uma chave para assinar tokens uma única vez:

```bash
openssl rand -hex 32
```

Guarde o resultado num local seguro. Use o **mesmo valor** como
`JWT_SIGNING_KEY` na loja e no inventário. Não o inclua neste README, no código
ou em arquivos versionados. O gateway não precisa dessa chave.

## 2. Aplicar as migrações

As migrações criam as tabelas necessárias nos bancos de dados locais dos
serviços. Execute cada comando no servidor. As configurações da loja e do
inventário exigem `JWT_SIGNING_KEY`, portanto informe a chave em cada terminal:

```bash
cd /caminho/para/Mochila_do_Goblin/mochila_goblin
read -rsp 'JWT_SIGNING_KEY: ' JWT_SIGNING_KEY; echo; export JWT_SIGNING_KEY
../venv/bin/python manage.py migrate
```

```bash
cd /caminho/para/Mochila_do_Goblin/inventario
read -rsp 'JWT_SIGNING_KEY: ' JWT_SIGNING_KEY; echo; export JWT_SIGNING_KEY
../venv/bin/python manage.py migrate
```

O inventário inclui uma migração inicial do modelo da mochila. Confirme que
`migrate` a aplicou sem erros antes de iniciar os serviços.

## 3. Iniciar o inventário

Em um terminal no servidor:

```bash
cd /caminho/para/Mochila_do_Goblin/inventario
read -rsp 'JWT_SIGNING_KEY: ' JWT_SIGNING_KEY; echo; export JWT_SIGNING_KEY
../venv/bin/python manage.py runserver 127.0.0.1:8002
```

Informe a mesma chave usada na loja. Mantenha esse terminal aberto enquanto o
serviço estiver em execução.

## 4. Iniciar a loja

Em outro terminal no servidor:

```bash
cd /caminho/para/Mochila_do_Goblin/mochila_goblin
read -rsp 'JWT_SIGNING_KEY: ' JWT_SIGNING_KEY; echo; export JWT_SIGNING_KEY
../venv/bin/python manage.py runserver 127.0.0.1:8001
```

Informe exatamente a mesma chave usada no inventário. Mantenha esse terminal
aberto também.

## 5. Iniciar o gateway para a rede local

Descubra o endereço IP do servidor na rede:

```bash
hostname -I
```

Escolha o IP que os computadores clientes podem alcançar (por exemplo,
`192.168.1.50`) e permita-o em `DJANGO_ALLOWED_HOSTS`. Em um terceiro terminal:

```bash
cd /caminho/para/Mochila_do_Goblin/api_gateway
DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1,192.168.1.50' \
  ../venv/bin/python manage.py runserver 0.0.0.0:8000
```

Substitua `192.168.1.50` pelo endereço real do servidor. O endereço precisa
estar em `DJANGO_ALLOWED_HOSTS`, caso contrário o Django pode responder
`400 Bad Request`. `0.0.0.0` faz o gateway escutar nas interfaces de rede; não
significa que esse endereço seja usado pelo cliente.

As variáveis de ambiente valem para o terminal e os processos iniciados por
ele. Ao reiniciar a loja ou o inventário, informe novamente a chave no
respectivo terminal.

## 6. Acessar pelo cliente


No computador cliente, configure o endereço-base da aplicação para o IP do
servidor e a porta do gateway, por exemplo:

```text
http://192.168.1.50:8000
```

## 7. Documentação

Para abrir a documentação Swagger das rotas públicas, acesse:

```text
http://192.168.1.50:8000/api/v1/docs/
```

Substitua `192.168.1.50` pelo endereço IP real do servidor.

Para autenticação, o endpoint do emissor está em:

```text
POST http://192.168.1.50:8000/api/v1/token/
```

Para renovar tokens, use:

```text
POST http://192.168.1.50:8000/api/v1/token/refresh/
```

As chamadas da loja e do inventário também devem passar pelo gateway. 