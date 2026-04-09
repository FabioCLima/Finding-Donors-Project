# Finding Donors for CharityML — Planejamento de Projeto

> **Objetivo:** Cumprir a rubrica da Udacity e construir um projeto de portfólio sênior, estruturado para o GitHub.

---

## 1. Visão Geral do Problema

**Contexto de negócio:** A CharityML precisa identificar, entre ~15 milhões de californianos, aqueles com maior probabilidade de doação (renda > $50K), minimizando o custo de envio de cartas.

**Tipo de problema:** Classificação binária supervisionada.

**Métrica principal:** F-beta score com **β = 0.5** (maior peso para Precision — preferimos não desperdiçar cartas a perder alguns doadores).

**Entregáveis obrigatórios (Udacity):**
- `finding_donors.ipynb` — notebook completo com todas as células executadas
- `report.html` — exportação HTML do notebook

**Entregáveis de portfólio (GitHub):**
- Scripts Python modulares organizados por responsabilidade
- `README.md` profissional com contexto, instruções e resultados
- Este documento de planejamento

---

## 2. Estrutura de Repositório Proposta

```
finding_donors/
│
├── finding_donors.ipynb        # Entregável Udacity (narrativa completa)
├── report.html                 # Exportação HTML do notebook
│
├── data/
│   └── census.csv              # Dataset original (não modificar)
│
├── src/                        # Scripts modulares (portfólio sênior)
│   ├── data_preparation.py     # Carregamento, limpeza, encoding, split
│   ├── evaluation.py           # Métricas, naive predictor, train_predict()
│   ├── model_selection.py      # Treinamento e comparação dos 3 modelos
│   ├── tuning.py               # GridSearchCV e otimização
│   └── feature_importance.py   # Importância de features e modelo reduzido
│
├── visuals.py                  # Fornecido pela Udacity — NÃO MODIFICAR
├── requirements.txt            # Dependências do projeto
├── README.md                   # Documentação do repositório
└── Finding_Donors_Project.md   # Este documento de planejamento
```

---

## 3. Checklist da Rubrica — Etapa por Etapa

### 3.1 Exploring the Data

| Critério | O que fazer | Arquivo |
|---|---|---|
| Estatísticas do dataset | Total de registros, features, distribuição do target | `data_preparation.py` + notebook |
| Identificar desbalanceamento | % de `>50K` vs `<=50K` | notebook (Q1) |

**Perguntas obrigatórias no notebook:**
- **Q1:** Quantos registros têm renda `>50K`? Quantos `<=50K`? Qual a proporção?

---

### 3.2 Preparing the Data

| Critério | O que fazer | Arquivo |
|---|---|---|
| Transformar features categóricas | One-hot encoding com `pd.get_dummies()` | `data_preparation.py` |
| Normalizar features numéricas | `sklearn.preprocessing.MinMaxScaler` | `data_preparation.py` |
| Train/test split | 80/20, `random_state=42` | `data_preparation.py` |

---

### 3.3 Evaluating Model Performance

| Critério | O que fazer | Arquivo |
|---|---|---|
| Naive Predictor Baseline | Classificar todos como `>50K`, calcular accuracy e F-beta | `evaluation.py` |
| Implementar `train_predict()` | Função que treina, cronometra e avalia qualquer modelo | `evaluation.py` |
| Escolher 3 algoritmos | Justificativa documentada (ver seção 4) | notebook (Q2) |
| Tabela comparativa | Tempo, acurácia e F-beta em treino e teste | notebook |

**Perguntas obrigatórias:**
- **Q2:** Por que você escolheu esses 3 algoritmos? Características do dado, vantagens/desvantagens.

---

### 3.4 Improving Results

| Critério | O que fazer | Arquivo |
|---|---|---|
| **Q3: Escolha do melhor modelo** | Justificar com base em custo computacional, F-beta e características dos dados | notebook |
| **Q4: Explicar em linguagem leiga** | Explicar o modelo escolhido sem jargão técnico | notebook |
| **Model Tuning** | `GridSearchCV` com ≥ 1 parâmetro e ≥ 3 valores cada | `tuning.py` + notebook |
| **Q5: Avaliação final** | Tabela accuracy + F1: modelo otimizado vs não-otimizado | notebook |

**Dica sênior para Q3:** Considere o trade-off entre interpretabilidade, F-beta no conjunto de teste e tempo de inferência — não só a melhor métrica.

---

### 3.5 Feature Importance

| Critério | O que fazer | Arquivo |
|---|---|---|
| **Q6: Top 5 features (intuição)** | Antes de rodar o modelo, rankear as 5 features mais relevantes com justificativa | notebook |
| **Q7: Extrair `feature_importances_`** | Implementar modelo com `.feature_importances_`, comparar com Q6 | `feature_importance.py` + notebook |
| **Q8: Modelo reduzido** | Retreinar com apenas top 5 features, comparar F-beta com modelo completo | `feature_importance.py` + notebook |

---

## 4. Escolha dos 3 Algoritmos — Guia de Raciocínio Sênior

A rubrica exige **justificativa**, não só nomes. Pense assim:

| Critério | Pergunta a responder |
|---|---|
| Escala dos dados | O algoritmo escala bem com ~32K linhas e ~100 features (após encoding)? |
| Tipo de features | Lida bem com features binárias (one-hot) + contínuas? |
| Interpretabilidade | O cliente consegue entender a decisão? |
| Custo computacional | Treino rápido o suficiente para GridSearch? |

**Algoritmos recomendados para justificativa sólida:**

1. **Random Forest** — robusto, lida bem com features mistas, tem `feature_importances_` nativo → candidato natural ao modelo final
2. **Gradient Boosting (GBM)** — geralmente melhor F-beta, mas mais lento; bom para comparação
3. **Logistic Regression** — baseline interpretável, rápido, bom ponto de referência

> ⚠️ Evite SVM com kernel RBF — muito lento para GridSearch nesse dataset.

---

## 5. Roteiro de Desenvolvimento — Ordem de Execução

```
Fase 1 — Setup e EDA
  [ ] Criar estrutura de pastas e repositório Git
  [ ] Instalar dependências (requirements.txt)
  [ ] Carregar census.csv e inspecionar: shape, dtypes, nulos, distribuição do target
  [ ] Responder Q1 no notebook

Fase 2 — Preparação dos Dados
  [ ] Separar features numéricas e categóricas
  [ ] Aplicar one-hot encoding
  [ ] Normalizar features numéricas
  [ ] Train/test split (80/20, random_state=42)
  [ ] Extrair código para src/data_preparation.py

Fase 3 — Baseline e Avaliação
  [ ] Implementar Naive Predictor
  [ ] Implementar função train_predict()
  [ ] Calcular métricas do Naive Predictor
  [ ] Extrair para src/evaluation.py

Fase 4 — Treinamento dos 3 Modelos
  [ ] Treinar Random Forest, GBM e Logistic Regression
  [ ] Gerar tabela comparativa
  [ ] Responder Q2 (justificativa), Q3 (melhor modelo), Q4 (explicação leiga)
  [ ] Extrair para src/model_selection.py

Fase 5 — Tuning
  [ ] GridSearchCV no modelo escolhido (≥ 1 param, ≥ 3 valores)
  [ ] Comparar otimizado vs não-otimizado
  [ ] Responder Q5
  [ ] Extrair para src/tuning.py

Fase 6 — Feature Importance
  [ ] Responder Q6 (intuição própria antes de rodar)
  [ ] Extrair feature_importances_ e plotar
  [ ] Retreinar com top 5 features
  [ ] Responder Q7 e Q8
  [ ] Extrair para src/feature_importance.py

Fase 7 — Finalização
  [ ] Revisar todas as células do notebook (limpar outputs desnecessários)
  [ ] Exportar report.html
  [ ] Escrever README.md profissional
  [ ] Commit final e push para GitHub
```

---

## 6. requirements.txt

```
numpy>=1.24
pandas>=2.0
scikit-learn>=1.3
matplotlib>=3.7
seaborn>=0.12
jupyter>=1.0
ipykernel>=6.0
```

---

## 7. Template de README.md para GitHub

```markdown
# Finding Donors for CharityML

## Problem Statement
Binary classification task to identify potential donors (income > $50K) 
from the UCI Census dataset. Developed as part of Udacity's Machine Learning 
Engineer Nanodegree — Supervised Learning module.

## Approach
- Exploratory Data Analysis with target distribution analysis
- Feature engineering: one-hot encoding + MinMax normalization
- Comparison of 3 supervised learners: Random Forest, Gradient Boosting, 
  Logistic Regression
- Hyperparameter tuning via GridSearchCV
- Feature importance analysis with reduced model evaluation

## Key Results
| Model | Accuracy | F-beta (β=0.5) |
|---|---|---|
| Naive Predictor | — | — |
| Best Unoptimized | — | — |
| Best Optimized | — | — |

*(Fill after execution)*

## Project Structure
...

## How to Run
...
```

---

## 8. Decisões de Design — Mentalidade Sênior

| Decisão | Justificativa |
|---|---|
| Scripts em `src/` além do notebook | Demonstra capacidade de modularização e código reutilizável |
| `random_state=42` em todos os pontos aleatórios | Reprodutibilidade total |
| `GridSearchCV` com `cv=5` | Balanço entre variância da estimativa e tempo de execução |
| F-beta β=0.5 como critério de seleção | Alinhado ao objetivo de negócio (minimizar envios desnecessários) |
| Responder Q6 antes de rodar o modelo | Demonstra raciocínio analítico independente de ferramentas |

---

*Documento criado como guia de planejamento para execução do projeto Finding Donors for CharityML.*
