from openapi_spec_validator import validate_spec

autofix_api = {
    "openapi": "3.0.3",
    "info": {
        "title": "AutoFix API",
        "description": "API para consulta do catálogo de serviços e gerenciamento de ordens de serviço da AutoFix.",
        "version": "1.0.0",
    },
    "servers": [{"url": "https://api.autofix.example.com", "description": "Servidor da API AutoFix"}],
    "tags": [
        {"name": "Serviços", "description": "Operações públicas de consulta do catálogo."},
        {"name": "Ordens de Serviço", "description": "Operações autenticadas de ordens de serviço."},
    ],
    "paths": {
        "/servicos": {
            "get": {
                "tags": ["Serviços"],
                "summary": "Lista os serviços de manutenção",
                "description": "Consulta pública ao catálogo de serviços oferecidos pela AutoFix.",
                "security": [],
                "responses": {
                    "200": {
                        "description": "Lista retornada com sucesso.",
                        "content": {"application/json": {
                            "schema": {"type": "array", "items": {"$ref": "#/components/schemas/Servico"}},
                            "example": [{"id": 1, "nome": "Troca de óleo", "descricao": "Troca do óleo do motor.", "preco": 180.0, "duracao_estimada": 40, "categoria": "troca_de_oleo"}]
                        }}
                    }
                },
            }
        },
        "/servicos/{servico_id}": {
            "get": {
                "tags": ["Serviços"],
                "summary": "Consulta um serviço pelo identificador",
                "description": "Retorna os dados de um serviço específico do catálogo.",
                "security": [],
                "parameters": [{"name": "servico_id", "in": "path", "required": True, "description": "Identificador único do serviço.", "schema": {"type": "integer", "example": 1}}],
                "responses": {
                    "200": {"description": "Serviço encontrado.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Servico"}}}},
                    "404": {"description": "Serviço não encontrado.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                },
            }
        },
        "/ordens-servico": {
            "post": {
                "tags": ["Ordens de Serviço"],
                "summary": "Abre uma ordem de serviço",
                "description": "Cria uma ordem para o veículo informado, referenciando serviços do catálogo.",
                "security": [{"bearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {
                        "schema": {"$ref": "#/components/schemas/NovaOrdemDeServico"},
                        "example": {"placa": "ABC1D23", "usuario_id": 561194, "servicos": [1, 3]}
                    }}
                },
                "responses": {
                    "201": {"description": "Ordem aberta com sucesso.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/OrdemDeServico"}}}},
                    "400": {"description": "Dados inválidos.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                    "401": {"description": "Token ausente ou inválido.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                    "404": {"description": "Um ou mais serviços não existem.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                },
            }
        },
        "/ordens-servico/{ordem_id}": {
            "get": {
                "tags": ["Ordens de Serviço"],
                "summary": "Consulta uma ordem de serviço",
                "description": "Consulta uma ordem pelo identificador e deve respeitar a autorização sobre a própria ordem.",
                "security": [{"bearerAuth": []}],
                "parameters": [{"name": "ordem_id", "in": "path", "required": True, "description": "Identificador único da ordem.", "schema": {"type": "integer", "example": 1001}}],
                "responses": {
                    "200": {"description": "Ordem encontrada.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/OrdemDeServico"}}}},
                    "401": {"description": "Token ausente ou inválido.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                    "403": {"description": "Usuário não autorizado.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                    "404": {"description": "Ordem não encontrada.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                },
            },
            "patch": {
                "tags": ["Ordens de Serviço"],
                "summary": "Cancela uma ordem de serviço",
                "description": "Cancela somente uma ordem cujo status atual seja aberta.",
                "security": [{"bearerAuth": []}],
                "parameters": [{"name": "ordem_id", "in": "path", "required": True, "description": "Identificador único da ordem.", "schema": {"type": "integer", "example": 1001}}],
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {
                        "schema": {"$ref": "#/components/schemas/CancelamentoOrdem"},
                        "example": {"status": "cancelada"}
                    }}
                },
                "responses": {
                    "200": {"description": "Ordem cancelada com sucesso.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/OrdemDeServico"}}}},
                    "400": {"description": "Operação inválida.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                    "401": {"description": "Token ausente ou inválido.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                    "403": {"description": "Usuário não autorizado.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                    "404": {"description": "Ordem não encontrada.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                    "409": {"description": "A ordem não está aberta e não pode ser cancelada.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Erro"}}}},
                },
            },
        },
    },
    "components": {
        "schemas": {
            "Servico": {
                "type": "object",
                "description": "Serviço de manutenção oferecido pela AutoFix.",
                "required": ["id", "nome", "descricao", "preco", "duracao_estimada", "categoria"],
                "properties": {
                    "id": {"type": "integer", "description": "Identificador único.", "example": 1},
                    "nome": {"type": "string", "description": "Nome do serviço.", "example": "Troca de óleo"},
                    "descricao": {"type": "string", "description": "Descrição do serviço.", "example": "Troca do óleo do motor."},
                    "preco": {"type": "number", "format": "double", "description": "Preço atual.", "example": 180.0},
                    "duracao_estimada": {"type": "integer", "description": "Duração estimada em minutos.", "example": 40},
                    "categoria": {"type": "string", "description": "Categoria do serviço.", "enum": ["troca_de_oleo", "alinhamento", "revisao", "freios", "outro"], "example": "troca_de_oleo"},
                },
            },
            "OrdemDeServico": {
                "type": "object",
                "description": "Ordem de serviço aberta para um veículo.",
                "required": ["id", "placa", "usuario_id", "servicos", "status", "data_abertura"],
                "properties": {
                    "id": {"type": "integer", "description": "Identificador único.", "example": 1001},
                    "placa": {"type": "string", "description": "Placa do veículo.", "example": "ABC1D23"},
                    "usuario_id": {"type": "integer", "description": "Usuário que abriu a ordem.", "example": 561194},
                    "servicos": {"type": "array", "description": "IDs dos serviços solicitados no catálogo.", "items": {"type": "integer"}, "example": [1, 3]},
                    "status": {"type": "string", "description": "Status atual da ordem.", "enum": ["aberta", "em_andamento", "concluida", "cancelada"], "example": "aberta"},
                    "data_abertura": {"type": "string", "format": "date-time", "description": "Data e hora de abertura.", "example": "2026-09-24T14:00:00"},
                },
            },
            "NovaOrdemDeServico": {
                "type": "object",
                "description": "Dados necessários para abrir uma ordem.",
                "required": ["placa", "usuario_id", "servicos"],
                "properties": {
                    "placa": {"type": "string", "description": "Placa do veículo.", "example": "ABC1D23"},
                    "usuario_id": {"type": "integer", "description": "Usuário responsável.", "example": 561194},
                    "servicos": {"type": "array", "description": "IDs dos serviços escolhidos.", "items": {"type": "integer"}, "example": [1, 3]},
                },
            },
            "CancelamentoOrdem": {
                "type": "object",
                "description": "Status usado para cancelar uma ordem aberta.",
                "required": ["status"],
                "properties": {"status": {"type": "string", "enum": ["cancelada"], "description": "Status de cancelamento.", "example": "cancelada"}},
            },
            "Erro": {
                "type": "object",
                "description": "Formato padronizado de erro.",
                "required": ["codigo", "mensagem"],
                "properties": {
                    "codigo": {"type": "integer", "description": "Código HTTP.", "example": 404},
                    "mensagem": {"type": "string", "description": "Descrição do erro.", "example": "Ordem de serviço não encontrada."},
                },
            },
        },
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "description": "Token de acesso para operações autenticadas.",
            }
        },
    },
}

if __name__ == "__main__":
    validate_spec(autofix_api)
    print("Contrato válido!")
