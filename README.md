# Mochila do Goblin 

Este guia descreve como executar o cliente em um computador e os três serviços (gateway, loja e inventário) em outro computador na mesma rede local. O cliente acessa somente o gateway; a loja e o inventário permanecem internos ao servidor.


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

Copie ou clone o projeto para a máquina servidora. Na raiz do repositório`Mochila_do_Goblin/`, crie o ambiente virtual e instale as dependências:

```bash
python3 -m venv venv
```

Ative a venv:

Linux:
```bash
source venv/bin/activate
```
Windows
```bash
.\venv\Scripts\Activate.ps1
```
Instale as depêndencias:

```bash
pip install -r requirements.txt
```

Os demais comandos deste guia assumem que o ambiente virtual `venv` está nessa raiz.

Gere uma chave para assinar tokens uma única vez:

Linux
```bash
openssl rand -hex 32
```

Windows
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

 Use o resultado como`JWT_SIGNING_KEY` na loja e no inventário. 

 Abra o terminal de cada microserviço, lembre-se de ativar o venv, rode o comando a seguir inserindo a chave. As configurações da loja e do
inventário exigem `JWT_SIGNING_KEY`, portanto informe a chave em cada terminal:

Linux
 ```bash

read -rsp 'JWT_SIGNING_KEY: ' JWT_SIGNING_KEY; echo; export JWT_SIGNING_KEY

```

Windows
```bash
$JWT_SIGNING_KEY = "insira_sua_chave_entre_as_aspas"

$env:JWT_SIGNING_KEY = $JWT_SIGNING_KEY

echo $env:JWT_SIGNING_KEY


```


## 2. Aplicar as migrações

As migrações criam as tabelas necessárias nos bancos de dados locais dos
serviços. Execute cada terminal dos servidores:

```bash
python manage.py migrate
```

## 3. Iniciar a loja

No terminal de mochila_goblin ative o servidor na porta 8001


```bash
python manage.py runserver 127.0.0.1:8001
```

## 4. Iniciar o inventario

No terminal de inventario ative o servidor na porta 8002

```bash
python manage.py runserver 127.0.0.1:8002
```

## 5. Iniciar o gateway para a rede local

Descubra o endereço IP do servidor na rede:

Linux:
```bash
hostname -I
```

Windows:
```bash
ipconfig
```

Escolha o IP que os computadores clientes podem alcançar (por exemplo,
`192.168.1.50`) e permita-o em `DJANGO_ALLOWED_HOSTS`. No terminal do projeto api_gateway:

!!Entre no terminal de api_gateway!!

Linux
```bash
DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1,192.168.1.50' 
```

Windows:
```bash
$env:DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,192.168.1.72"
```

e depois ative o servidor:

```bash
python manage.py runserver 0.0.0.0:8000
```



Substitua `192.168.1.50` pelo endereço real do servidor. O endereço precisa estar em `DJANGO_ALLOWED_HOSTS`, caso contrário o Django pode responder `400 Bad Request`. `0.0.0.0` faz o gateway escutar nas interfaces de rede; 


## 6. Acessar pelo cliente


No computador cliente, configure o endereço-base da aplicação para o IP do servidor e a porta do gateway, por exemplo:

```text
http://192.168.1.50:8000
```

## 7. Documentação

Para abrir a documentação Swagger das rotas públicas, acesse:

```text
http://192.168.1.50:8000/api/v1/docs/
```

Para autenticação, o endpoint do emissor está em:

```text
POST http://192.168.1.50:8000/api/v1/token/
```

Para renovar tokens, use:

```text
POST http://192.168.1.50:8000/api/v1/token/refresh/
```
