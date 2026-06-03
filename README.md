# Benefício Social — RPA Platform

Plataforma RPA para análise e cadastro de clientes aptos ao benefício social/desconto por baixa renda.

O projeto simula um cenário corporativo onde documentos de renda são analisados, clientes elegíveis são enviados para uma fila de automação e o processo é monitorado com logs, métricas e dashboards.

---

## Objetivo do Projeto

Demonstrar uma solução completa com foco em:

- RPA com Python
- Backend com FastAPI
- Frontend com Angular
- PostgreSQL
- Upload de documentos PDF/PNG
- OCR para análise documental
- Human-in-the-loop
- Fila de automação
- Worker contínuo
- Logs estruturados
- Métricas Prometheus
- Grafana + Loki
- Segurança de credenciais
- Boas práticas de versionamento

---

## Arquitetura

```text
Angular Frontend
      ↓
FastAPI Backend
      ↓
PostgreSQL
      ↓
RPA Queue
      ↓
Continuous Worker
      ↓
Subprocess RPA
      ↓
Logs + Metrics
      ↓
Grafana / Loki / Prometheus

### Stack

## Backend

Python
FastAPI
SQLAlchemy
PostgreSQL
JWT
Bcrypt
Keyring / Windows Credential Manager

## Frontend

Angular
TypeScript
Reactive Forms
AuthGuard
HTTP Interceptor

## RPA

Python Worker
Subprocess
Queue persistida em banco
Execution tracking

## Observabilidade

Prometheus
Grafana
Loki
Promtail
Logs JSON
Execution ID

## IA/OCR

Tesseract OCR
pdfplumber
Pillow
análise determinística de renda
preparação para IA local com RAG/CrewAI

## Funcionalidades
Autenticação
Login com email e senha
Senha armazenada com hash
JWT para autenticação
Rotas protegidas

## Clientes
CRUD de clientes
Validação de email
Máscara de telefone brasileiro
Regra de elegibilidade por renda
Upload de PDF/PNG

## Documentos
Upload seguro
Geração de nome com UUID
Validação por MIME type
Metadados no banco

## OCR
Extração de texto de PDF/PNG
Identificação de renda
Classificação:
    APPROVED
    REJECTED
    INCONCLUSIVE

## Human-in-the-loop
Casos inconclusivos vão para revisão humana
Analista aprova ou reprova
Decisão registrada com motivo
Cliente aprovado entra na fila RPA

## Fila RPA
    Jobs PENDING
    Jobs RUNNING
    Jobs DONE
    Jobs FAILED
    Evita execução duplicada

## Worker

Worker contínuo
Polling configurável
Execução via subprocess
Timeout
Logs e métricas

## Observabilidade
Total de execuções
Sucessos
Falhas
Timeouts
Duração média
P95
Logs da API
Logs do worker
Alerta de execução lenta

## Segurança
Este projeto evita versionar:
    arquivos .env
    senhas
    tokens
    documentos reais
    PDFs reais
    imagens reais
    logs sensíveis
As credenciais podem ser carregadas por:
    variáveis de ambiente
    Windows Credential Manager
    Docker environment variables em ambiente local
Também foram aplicadas práticas de:
    mascaramento de CPF
    mascaramento de telefone
    mascaramento de email
    mascaramento de JWT em logs
    não exposição de senha
    não logging de documentos

## Como Rodar
1. Clonar repositório:
git clone https://github.com/SEU_USUARIO/beneficio-social-rpa.git
cd beneficio-social-rpa

2. Subir ambiente Docker
docker compose up -d --build

3. Criar tabelas
cd backend
python create_tables.py

4. Criar usuário admin
python create_admin.py

5. Executar testes do backend
.venv\Scripts\python.exe -m pytest

6. Rodar frontend
cd ../frontend
npm install
ng serve

## Acessos

API - http://localhost:8000/docs
Frontend - http://localhost:4200
Grafana - http://localhost:3000
Prometheus - http://localhost:9090

Usuário Admin Local
Email: admin@beneficiosocial.local
Senha: Admin@123
Importante: Apenas para ambiente local/dev.

# Fluxo principal
1. Usuário faz login
2. Cadastra cliente
3. Envia documento PDF/PNG
4. Sistema analisa documento via OCR
5. Se aprovado, cliente entra na fila RPA
6. Se reprovado, fica registrado
7. Se inconclusivo, vai para revisão humana
8. Worker processa fila
9. RPA executa via subprocess
10. Logs e métricas são enviados para observabilidade

# Evoluções Futuras
RabbitMQ ou Celery
MinIO/S3 para documentos
Antivírus em arquivos enviados
Hash SHA256 dos documentos
Alembic para migrations
Testes automatizados
CI/CD GitHub Actions
RAG local com Ollama
CrewAI/LangChain
Painel de revisão humana no Angular
Alertas por email/Slack/Teams

👨‍💻 Autor
Gabriel Belmiro 🔗 https://www.linkedin.com/in/gabriel-belmiro/

Desenvolvedor em constante evolução, com foco em fundamentos sólidos, organização de código e crescimento progressivo em arquitetura e boas práticas.