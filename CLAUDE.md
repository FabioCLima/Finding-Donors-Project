# Finding Donors for CharityML — Project Instructions

## Objetivo

Classificar indivíduos com renda >50K (potenciais doadores) a partir dos dados do Census Income.
O modelo final deve superar um baseline ingênuo em **F0.5** (precision-heavy), ser salvo como `.joblib` em `models/`, e seguir a metodologia **CRISP-DM** documentada em `notebooks/finding_donors_crispdm.ipynb`.

## Estrutura do Projeto

```
Finding_Donors_Project/
├── CLAUDE.md                # Este arquivo — instruções do projeto
├── pyproject.toml           # Dependências (uv)
├── data/
│   ├── census.csv           # Base de treino (45222 registros, 13 features + income)
│   └── test_census.csv      # Base de teste externa
├── models/                  # Artefatos serializados (.joblib)
├── notebooks/               # Notebooks exploratórios (referência, não execução)
│   └── finding_donors_crispdm.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py            # Constantes, caminhos, listas de features
│   ├── data_loader.py       # Leitura e validação estrutural dos dados
│   ├── features.py          # Feature engineering (capital log/flags, agrupamento)
│   ├── preprocessing.py     # ColumnTransformer, split estratificado
│   ├── train.py             # Catálogo de modelos, CV, seleção do campeão
│   ├── tuning.py            # RandomizedSearchCV do modelo campeão
│   ├── evaluate.py          # Avaliação em holdout, threshold, métricas, auditoria
│   └── pipeline.py          # Orquestrador principal — executa o pipeline completo
├── scripts/
│   └── run_pipeline.py      # Entry point CLI: python scripts/run_pipeline.py
├── docs/                    # Documentação analítica
└── imgs/                    # Imagens e gráficos
```

## Pipeline de ML — Etapas

### 1. `src/config.py` — Configuração centralizada
- `RANDOM_STATE = 42`, `TEST_SIZE = 0.20`, `BETA = 0.5`, `CV_SPLITS = 5`
- `DATA_PATH`, `MODELS_DIR` (com `pathlib.Path`)
- Listas de features:
  - `CORE_NUMERIC`: `["age", "hours-per-week", "capital_gain_log", "capital_loss_log", "capital_gain_flag", "capital_loss_flag"]`
  - `CORE_CATEGORICAL`: `["workclass", "education_level", "marital-status", "occupation", "relationship"]`
  - `SENSITIVE_COLS`: `["sex", "race", "native-country"]`
  - `REDUNDANT_COLS`: `["education-num"]`
  - `NON_PREDICTIVE_COLS`: `["fnlwgt"]`
- `RARE_COUNTRY_MIN_SUPPORT = 50`

### 2. `src/data_loader.py` — Leitura e validação
- Função `load_census(path) -> pd.DataFrame`
- Validação: shape, dtypes, missing values, duplicados
- Criação do target binário: `(income.str.strip() == ">50K").astype(int)`
- Cálculo do `baseline` (taxa da classe positiva)

### 3. `src/features.py` — Feature engineering
- Função `engineer_features(df) -> pd.DataFrame`
- Capital gains/losses: flags binárias + log1p das magnitudes
- Agrupamento de países raros (suporte < 50 → "Other")
- Retorna o DataFrame preparado com as novas colunas

### 4. `src/preprocessing.py` — Preprocessamento e split
- `split_data(df, target_col)` → `X_train, X_test, y_train, y_test` (estratificado)
- `build_preprocessor(numeric_features, categorical_features)` → `ColumnTransformer`
  - `MinMaxScaler` para numéricas
  - `OneHotEncoder(handle_unknown="ignore", sparse_output=False)` para categóricas
- `make_modeling_pipeline(estimator, numeric, categorical)` → `sklearn.pipeline.Pipeline`

### 5. `src/train.py` — Treinamento e seleção
- `get_model_catalog()` → dicionário com todos os modelos candidatos:
  - Benchmarks: `DummyClassifier` (most_frequent e always_positive)
  - Candidatos: `LogisticRegression`, `LogisticRegressionBalanced`, `RandomForestClassifier`, `HistGradientBoostingClassifier`
- `run_cross_validation(catalog, X_train, y_train)` → DataFrame com métricas de CV
- Scoring: `f0_5`, `precision`, `recall`, `accuracy`
- Diagnóstico de generalização (overfitting/underfitting)
- Retorna o `best_model_name` e os pipelines treinados

### 6. `src/tuning.py` — Otimização de hiperparâmetros
- `get_tuning_setup(model_name)` → espaço de busca por família de modelo
- `run_tuning(pipeline, X_train, y_train)` → `RandomizedSearchCV` results + `best_estimator_`
- Cross-validation estratificada com `refit=True`

### 7. `src/evaluate.py` — Avaliação final
- `evaluate_on_holdout(model, X_test, y_test)` → métricas finais
- `threshold_search(model, X_train, y_train)` → threshold ótimo via OOF scores
- `compute_binary_metrics(y_true, y_pred)` → accuracy, precision, recall, F0.5
- Classification report e matriz de confusão
- Auditoria de fairness por subgrupo (sex, race)

### 8. `src/pipeline.py` — Orquestrador
- Função `run_pipeline()` que executa todas as etapas em sequência
- Logging de progresso a cada etapa
- Salva o modelo final como `models/best_model.joblib`
- Salva o preprocessor como `models/preprocessor.joblib`
- Salva metadados (métricas, threshold, features) como `models/metadata.json`

## Convenções

- **Python**: 3.13+, gerenciado com `uv`
- **Dependências**: scikit-learn, pandas, numpy, matplotlib, seaborn, joblib (via sklearn)
- **Idioma do código**: inglês para nomes de funções/variáveis, português nos logs e docstrings
- **Sem variáveis sensíveis** no modelo de produção (sex, race, native-country ficam fora do pipeline principal)
- **Data leakage**: split ANTES de fit do preprocessor — sempre
- **Métrica principal**: F0.5 (precision-weighted, adequada para minimizar falsos positivos em campanhas)
- **Serialização**: `joblib.dump()` para modelos, JSON para metadados

## Comandos

```bash
# Instalar dependências
uv sync

# Executar o pipeline completo
uv run python scripts/run_pipeline.py

# Executar testes (quando implementados)
uv run pytest tests/
```

## Decisões técnicas vindas da EDA

1. **education_level vs education-num**: mapeamento 1:1 → manter apenas `education_level`
2. **Capital gains/losses**: distribuição com massa em zero → criar flags binárias + log1p
3. **fnlwgt**: peso amostral, não preditivo → excluir
4. **native-country**: categorias com suporte < 50 → agrupar como "Other" (apenas na trilha audit)
5. **marital-status + relationship**: sobreposição parcial, manter ambos nesta versão
