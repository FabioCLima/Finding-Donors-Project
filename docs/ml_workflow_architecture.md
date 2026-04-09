# Arquitetura Proposta de Arquivos

Este documento propõe uma arquitetura profissional para transformar o notebook `notebooks/finding_donors_crispdm.ipynb` em um workflow de machine learning organizado, reproduzível e fácil de manter.

## Objetivo

Separar o projeto em camadas claras para:
- leitura e versionamento de dados;
- preparação e transformação;
- treinamento e comparação de modelos;
- avaliação e geração de figuras;
- persistência de artefatos;
- reprodutibilidade e validação.

## Estrutura de Pastas Sugerida

```text
Finding_Donors_Project/
├── data/
│   ├── raw/                     # Dados originais, imutáveis
│   ├── interim/                 # Dados intermediários gerados no fluxo
│   └── processed/               # Dados finais prontos para modelagem
├── notebooks/
│   ├── finding_donors_crispdm.ipynb
│   └── sandbox/                 # Explorações pontuais, fora do fluxo principal
├── src/
│   └── finding_donors/
│       ├── __init__.py
│       ├── config.py            # Caminhos, constantes, seeds, parâmetros globais
│       ├── data/
│       │   ├── __init__.py
│       │   ├── ingest.py        # Leitura, padronização e carregamento
│       │   ├── validate.py      # Validação estrutural e de schema
│       │   └── split.py         # Train/test split e reprodutibilidade
│       ├── features/
│       │   ├── __init__.py
│       │   ├── build_features.py # Engenharia de variáveis
│       │   └── preprocess.py    # Encoding, scaling, transformações
│       ├── models/
│       │   ├── __init__.py
│       │   ├── baseline.py      # Baseline ingênuo
│       │   ├── train.py         # Treino dos modelos candidatos
│       │   ├── tune.py          # Busca de hiperparâmetros
│       │   └── predict.py       # Inferência e carregamento de modelo
│       ├── evaluation/
│       │   ├── __init__.py
│       │   ├── metrics.py       # Accuracy, F-beta, matriz de confusão
│       │   └── report.py        # Relatórios e comparação entre modelos
│       ├── visualization/
│       │   ├── __init__.py
│       │   └── plots.py         # Gráficos com matplotlib/seaborn
│       └── utils/
│           ├── __init__.py
│           ├── logging.py        # Setup de logging
│           └── io.py            # Funções auxiliares de leitura/escrita
├── models/                      # Modelos serializados, ex: .pkl/.joblib
├── figs/                        # Figuras geradas pelo pipeline
├── reports/
│   ├── metrics/                 # Métricas, tabelas e comparativos
│   └── notebooks/               # Exportações do notebook, se necessário
├── configs/
│   ├── base.yaml                # Configuração padrão do projeto
│   ├── model.yaml               # Hiperparâmetros e grids
│   └── paths.yaml               # Caminhos lógicos do projeto
├── tests/
│   ├── test_data_validation.py
│   ├── test_features.py
│   └── test_models.py
├── scripts/
│   ├── run_train.py             # Executa treino end-to-end
│   ├── run_evaluate.py          # Executa avaliação
│   └── run_predict.py           # Inferência local
├── README.md
├── pyproject.toml
└── uv.lock
```

## Como o Notebook Se Conecta a Essa Estrutura

O notebook deve virar uma camada de exploração e narrativa, não o local central da lógica.

Mapeamento sugerido:

- `Business Understanding` -> `docs/` e `configs/`
- `Data Understanding` -> `src/finding_donors/visualization/` e `src/finding_donors/data/validate.py`
- `Data Preparation` -> `src/finding_donors/features/`
- `Modeling` -> `src/finding_donors/models/`
- `Evaluation` -> `src/finding_donors/evaluation/`

Assim, o notebook fica mais leve e passa a consumir funções prontas do pacote `src/`.

## Responsabilidade de Cada Pasta

### `data/`
- `raw/`: arquivos originais, sem alteração manual.
- `interim/`: saídas temporárias, como versões limpas ou amostras.
- `processed/`: dataset final transformado, pronto para treino.

### `src/finding_donors/data/`
- leitura dos dados;
- checagem de colunas e tipos;
- inspeção de nulos e duplicados;
- split treino/teste com seed fixa.

### `src/finding_donors/features/`
- transformações numéricas;
- encoding categórico;
- tratamento de variáveis assimétricas;
- montagem de `X_train`, `X_test`, `y_train`, `y_test`.

### `src/finding_donors/models/`
- baseline;
- treino dos modelos candidatos;
- tuning;
- serialização do melhor estimador.

### `src/finding_donors/evaluation/`
- métricas;
- comparação entre modelos;
- relatórios finais;
- análise de erro.

### `figs/`
- histogramas;
- boxplots;
- matrizes de confusão;
- curvas ou gráficos de importância de features.

### `models/`
- artefatos versionados do treino final;
- exemplo: `gradient_boosting.pkl`, `preprocessor.joblib`.

### `reports/`
- tabelas resumidas;
- exportações em CSV/JSON/HTML;
- resultados consolidados de experimentos.

## Bibliotecas Recomendadas Para Profissionalizar o Projeto

Além da stack atual:

### Essenciais
- `loguru`: logging simples, legível e mais produtivo que `logging` puro.
- `pydantic`: validação forte de schema, configuração e entrada do pipeline.
- `pyyaml` ou `ruamel.yaml`: leitura de arquivos `yaml` de configuração.
- `joblib`: persistência eficiente de pipelines e modelos do scikit-learn.
- `pathlib` e `dataclasses` da biblioteca padrão: organização de caminhos e configurações.

### Muito úteis em projetos de ML
- `scipy`: testes estatísticos, transformações e suporte numérico.
- `imbalanced-learn`: caso o desbalanceamento exija técnicas como `SMOTE` ou `RandomUnderSampler`.
- `mlflow`: rastreamento de experimentos, métricas e artefatos.
- `hydra` ou `omegaconf`: gerenciamento de configuração mais robusto para experimentos.
- `great_expectations`: validação de dados mais formal, útil em pipelines repetíveis.
- `pytest`: testes automatizados para funções de preparação, validação e modelagem.
- `ruff`: lint e formatação rápida.
- `mypy`: checagem de tipos, especialmente útil com `pydantic`.

### Opcional, dependendo da maturidade do projeto
- `optuna`: busca de hiperparâmetros mais flexível que `GridSearchCV`.
- `xgboost` ou `lightgbm`: se o projeto evoluir para comparações com boosting mais forte.
- `seaborn.objects` ou `plotly`: visualizações mais expressivas em análise exploratória.

## Sugestão de Camadas do Pipeline

1. Ingestão
2. Validação
3. Preparação
4. Feature engineering
5. Treinamento
6. Tunagem
7. Avaliação
8. Persistência
9. Inferência

## Convenções Recomendadas

- manter `data/raw` intocável;
- nunca misturar artefatos de treino com dados crus;
- salvar transformadores junto do modelo final;
- versionar configuração, não apenas código;
- registrar seeds e métricas para reprodução;
- separar notebook de produção.

## Mapeamento Prático Para Este Projeto

Com base no notebook atual, os principais blocos seriam:
- leitura do `census.csv` em `data/raw/`;
- limpeza e inspeção em `src/finding_donors/data/`;
- transformação de `capital-gain` e `capital-loss` em `src/finding_donors/features/`;
- comparação entre `LogisticRegression`, `RandomForestClassifier` e `GradientBoostingClassifier` em `src/finding_donors/models/`;
- métricas `accuracy` e `F0.5` em `src/finding_donors/evaluation/`;
- gráficos de suporte e importância de features em `figs/`;
- modelo final persistido em `models/`.

## Resumo Executivo

Se quisermos transformar o notebook em um projeto profissional, a melhor decisão é:
- manter o notebook como camada narrativa;
- mover a lógica para `src/finding_donors/`;
- padronizar entradas, saídas e configurações;
- adicionar logging, validação e testes desde o início.

