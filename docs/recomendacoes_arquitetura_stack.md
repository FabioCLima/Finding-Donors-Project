# Recomendacoes de Arquitetura e Stack

## Contexto

Este documento consolida recomendacoes para evoluir o projeto de ML + FastAPI para um padrao mais profissional, escalavel e facil de manter.

## Diagnostico do Estado Atual

### Pontos fortes

- Ja existe separacao basica de logica de ML em `ml/data.py` e `ml/model.py`.
- A API com FastAPI esta funcional e inclui schema Pydantic.
- O projeto usa DVC para versionar dados e artefatos de modelo.
- Ha pipeline de CI com lint e testes.

### Oportunidades de melhoria

- Estrutura ainda esta "flat" (arquivos-chave na raiz), o que dificulta crescimento.
- Falta separacao clara entre camadas de API, dominio ML, configuracao e infraestrutura.
- Dependencias estao em mais de uma fonte (`pyproject.toml` e `requirements.txt`), gerando risco de inconsistencias.
- Observabilidade ainda limitada (sem padrao de logs estruturados, traces e metricas operacionais).

## Folders Necessarios (Base Profissional)

Para uma estrutura de projeto robusta, recomenda-se adotar no minimo:

- `src/`: codigo-fonte principal.
- `src/api/`: rotas, schemas e dependencias da API.
- `src/ml/`: treino, inferencia, avaliacao e engenharia de features.
- `src/core/`: configuracao global, logging, exceptions e utilitarios comuns.
- `tests/`: testes unitarios, integracao e ponta-a-ponta.
- `configs/`: arquivos de configuracao (`train.yaml`, `api.yaml`, `logging.yaml`).
- `data/`: dados em camadas (`raw`, `interim`, `processed`), versionados com DVC.
- `models/` ou `artifacts/`: artefatos locais de modelo e transformadores.
- `scripts/`: entrypoints de treino, avaliacao e tarefas operacionais.
- `notebooks/`: exploracao e prototipagem.
- `docs/`: documentacao tecnica, arquitetura, runbooks e model card.
- `docker/`: conteinerizacao e arquivos de deploy local.
- `.github/workflows/`: CI/CD.

## Arquitetura Recomendada

Estrutura alvo sugerida:

```text
.
├── src/
│   ├── api/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── dependencies.py
│   ├── ml/
│   │   ├── features/
│   │   ├── training/
│   │   ├── inference/
│   │   ├── evaluation/
│   │   └── registry/
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── configs/
│   ├── train.yaml
│   ├── api.yaml
│   └── logging.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── models/
├── scripts/
├── notebooks/
├── docs/
├── docker/
├── pyproject.toml
└── uv.lock
```

## Stack de Bibliotecas Moderna (Recomendada)

### API e validacao

- `fastapi`
- `uvicorn[standard]`
- `pydantic` (v2)
- `pydantic-settings` (configuracao por ambiente)

### Logging e observabilidade

- `loguru` (logs estruturados e ergonomia)
- Opcional para padrao corporativo: `structlog` + `logging` nativo
- `prometheus-client` (metricas)
- `opentelemetry` (tracing distribuido)
- `sentry-sdk` (monitoramento de erros em producao)

### Ciencia de dados e ML

- `numpy`
- `pandas`
- `scikit-learn`
- `joblib`

### Experiment tracking e ciclo de vida de modelo

- `mlflow` (tracking, registry e reproducibilidade)
- Alternativa: `wandb`
- `dvc` para dados e artefatos grandes

### Qualidade de codigo e testes

- `ruff` (lint + format)
- `pytest`
- `pytest-cov`
- `mypy` (tipagem estatica)
- `pre-commit`

### Infra e runtime

- `uv` para gestao de dependencias/ambiente
- `docker` e `docker compose`
- `gunicorn` (quando aplicavel para deploy com workers)

## Recomendacoes Praticas de Curto Prazo

1. Migrar para layout `src/` sem mudar comportamento funcional.
2. Unificar gestao de dependencias em uma unica fonte (`pyproject.toml` + `uv.lock`).
3. Criar `src/core/config.py` com `BaseSettings` para centralizar variaveis de ambiente.
4. Implementar `src/core/logging.py` com `loguru` e formato JSON para observabilidade.
5. Separar endpoints em `src/api/routers/` e schemas em `src/api/schemas/`.
6. Mover testes para `tests/unit/` e criar base para `tests/integration/`.
7. Externalizar hiperparametros e paths para `configs/train.yaml`.
8. Padronizar relatorios de metricas em `reports/metrics/` (JSON/CSV versionavel).

## Roadmap Sugerido (Fases)

### Fase 1 - Estruturacao (baixo risco)

- Reorganizar pastas para `src/`, `tests/`, `configs/`, `scripts/`.
- Ajustar imports e entrypoints.

### Fase 2 - Governanca tecnica

- Padronizar dependencias e atualizar CI.
- Adicionar tipagem estatica (`mypy`) e cobertura minima de testes.

### Fase 3 - Operacao e observabilidade

- Introduzir logging estruturado, metricas e tracing.
- Definir padrao de monitoramento para API e modelo.

### Fase 4 - MLOps avancado

- Integrar `mlflow` para tracking e model registry.
- Formalizar pipeline de treino/avaliacao/publicacao.

## Resultado Esperado

Com essas mudancas, o projeto tende a ganhar:

- maior manutenibilidade;
- onboarding mais rapido para novos colaboradores;
- melhor confiabilidade em producao;
- reproducibilidade de experimentos;
- base tecnica solida para escalar para novos modelos e endpoints.
