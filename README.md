# AutoFix - Contrato e Arquitetura

## Sobre o projeto

A AutoFix é uma rede de oficinas mecânicas para carros e motos. O projeto consiste na definição de um contrato de API REST para consulta do catálogo de serviços e gerenciamento de ordens de serviço.

A API possui endpoints públicos para consulta dos serviços e endpoints autenticados para abertura, consulta e cancelamento de ordens de serviço.

A arquitetura separa o **Catálogo de Serviços** do **Serviço de Ordens de Serviço**, estabelecendo responsabilidades e fronteiras independentes.

## Links

- [Documentação](https://docs.google.com/document/d/1GHMxOEjR8SpMjYrKcOpgKDxkH9dkHgxbHjT1KGJVvDI/edit?usp=sharing)
- [Diagrama da Arquitetura](https://www.figma.com/board/0TqvNS8OBYyLad1Io0QhEw/autofix_diagram?node-id=0-1&t=rLfCm0Yk9l5c033q-1)

## Como validar

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute o contrato:

```bash
python autofix_api.py
```

Se estiver tudo correto, será exibido:

```text
Contrato válido!
```
