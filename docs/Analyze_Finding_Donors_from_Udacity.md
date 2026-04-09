# Analise Tecnica - Finding Donors from Udacity

**Escopo:** revisao tecnica do notebook `notebooks/finding_donors.ipynb`  
**Papel assumido:** cientista de dados senior / mentor tecnico  
**Contexto:** projeto didatico da Udacity para demonstrar o workflow de machine learning com a API do scikit-learn em um problema de classificacao binaria desbalanceada.

---

## Parte 1. O que foi feito, por que foi feito e quais foram os resultados

### 1. Objetivo do projeto

O objetivo primario esta bem definido: criar um modelo de classificacao binaria para ajudar a CharityML a identificar perfis com renda anual acima de `50K`. Em termos de negocio, isso significa priorizar contatos com maior chance de retorno, reduzindo custo de campanha e evitando envio de cartas para pessoas com baixa probabilidade de doacao.

O notebook escolhe corretamente o criterio de sucesso principal como `F-beta` com `beta = 0.5`. Essa escolha faz sentido porque o problema valoriza mais precision do que recall: um falso positivo representa custo operacional sem retorno esperado.

### 2. Exploracao dos dados

**O que foi feito**

- Leitura do dataset `census.csv`.
- Contagem total de registros.
- Separacao da classe alvo em `<=50K` e `>50K`.
- Visualizacao da distribuicao da variavel alvo.

**Por que isso foi feito**

Antes de qualquer modelo, era necessario entender o desbalanceamento da classe e confirmar a natureza do problema. Isso orienta a escolha da metrica, da estrategia de validacao e do baseline.

**Resultados relevantes**

| Item | Valor |
|---|---:|
| Total de registros | 45.222 |
| `>50K` | 11.208 |
| `<=50K` | 34.014 |
| Percentual `>50K` | 24,78% |

**Leitura tecnica**

O dataset e desbalanceado. Um modelo ingenuo que sempre preve `<=50K` teria alta accuracy aparente, mas seria inutil para o objetivo de negocio. O notebook reconhece isso e usa um naive predictor para estabelecer uma referencia realista.

### 3. Preprocessamento

**O que foi feito**

- Separacao entre `income_raw` e `features_raw`.
- Aplicacao de transformacao logaritmica em `capital-gain` e `capital-loss` com `np.log(x + 1)`.
- Normalizacao com `MinMaxScaler` nas features numericas.
- One-hot encoding com `pd.get_dummies()`.
- Conversao do alvo para binario (`<=50K -> 0`, `>50K -> 1`).
- Split treino/teste com `stratify=income`.

**Por que isso foi feito**

- `capital-gain` e `capital-loss` sao fortemente assimetricas; o log reduz o impacto de outliers.
- Modelos supervisionados da biblioteca funcionam melhor com entradas numericas e escaladas.
- `pd.get_dummies()` transforma categorias em variaveis numericas sem impor ordem artificial.
- `stratify=income` preserva a proporcao das classes no treino e no teste.

**Resultados relevantes**

| Item | Valor |
|---|---:|
| Total de features apos one-hot | 103 |
| Amostras de treino | 36.177 |
| Amostras de teste | 9.045 |

**Ponto tecnico importante**

Ha um risco real de **data leakage** aqui. O notebook ajusta o `MinMaxScaler` antes do split e cria o one-hot encoding no dataset completo antes de separar treino e teste. Isso significa que informacoes estatisticas do conjunto inteiro podem influenciar o preprocessing. O efeito pode nao ser enorme neste caso, mas metodologicamente o ideal e encapsular tudo em um `Pipeline` com `ColumnTransformer`, ajustando apenas no treino.

### 4. Baseline ingenuo

**O que foi feito**

O notebook construiu um baseline que sempre prediz `>50K`.

**Por que isso foi feito**

Para verificar se o modelo final realmente aprende alguma coisa ou apenas repete a classe majoritaria/minoritaria de forma simplista.

**Resultados relevantes**

| Metrica | Valor |
|---|---:|
| Accuracy | 0,2478 |
| F-score (`beta=0.5`) | 0,2917 |

**Leitura tecnica**

Esse baseline e fraco, mas extremamente util como referencial. Ele mostra que o problema nao pode ser resolvido com um chute constante e ajuda a medir o ganho real dos modelos supervisionados.

### 5. Comparacao de modelos

**O que foi feito**

O notebook comparou tres algoritmos:

- `LogisticRegression`
- `RandomForestClassifier`
- `GradientBoostingClassifier`

As comparacoes foram feitas com amostras de 1%, 10% e 100% do treino.

**Por que isso foi feito**

Essa e uma forma simples de observar:

- comportamento com poucos dados;
- custo de treinamento;
- tendencia de generalizacao;
- sensibilidade a volume de amostra.

**Leitura tecnica**

A escolha dos tres modelos e coerente para o problema:

- `LogisticRegression` funciona como baseline interpretavel.
- `RandomForestClassifier` lida bem com relacoes nao lineares e interacoes.
- `GradientBoostingClassifier` costuma performar muito bem em dados tabulares.

**Limite da abordagem**

O notebook nao faz uma avaliacao estatistica mais robusta da variabilidade do modelo. Ha um unico split treino/teste e uma visualizacao de performance por amostra, mas nao ha uma analise explicita de:

- variancia entre folds;
- dispersao de metricas;
- estabilidade entre seeds diferentes;
- evidencia formal de underfitting ou overfitting.

Ou seja, o notebook mostra desempenho, mas nao fecha completamente o diagnostico de generalizacao.

### 6. Tuning do modelo final

**O que foi feito**

O notebook escolheu `GradientBoostingClassifier` e fez `GridSearchCV` com:

- `n_estimators`
- `learning_rate`
- `max_depth`

usando `make_scorer(fbeta_score, beta=0.5)` e `cv=5`.

**Por que isso foi feito**

Esse e o passo correto para otimizar o modelo de acordo com a metrica de negocio, e nao por accuracy pura.

**Resultados relevantes**

| Modelo | Accuracy | F-score |
|---|---:|---:|
| Nao otimizado | 0,8639 | 0,7461 |
| Otimizado | 0,8719 | 0,7581 |

**Leitura tecnica**

O ganho foi modesto, mas real. O modelo otimizado ficou melhor no conjunto de teste e manteve o foco em precision, que e exatamente o que o problema pede.

### 7. Importancia de features e selecao de variaveis

**O que foi feito**

O notebook treinou um `RandomForestClassifier` para extrair `feature_importances_`, visualizou as cinco features mais relevantes e depois re-treinou o modelo final usando apenas essas cinco variaveis.

**Por que isso foi feito**

Esse passo ajuda a responder duas perguntas:

- quais variaveis mais explicam a classe alvo;
- quanto performance se perde ao reduzir o espaco de features.

**Resultados relevantes**

Top 5 features encontradas:

1. `age`
2. `hours-per-week`
3. `capital-gain`
4. `marital-status__Married-civ-spouse`
5. `education-num`

Modelo final com features reduzidas:

| Modelo | Accuracy | F-score |
|---|---:|---:|
| Full model | 0,8719 | 0,7581 |
| Reduced model | 0,8526 | 0,7172 |

**Leitura tecnica**

O conjunto reduzido perdeu desempenho. Isso confirma que as variaveis restantes no modelo completo ainda carregam sinal util. Para um cenario com restricao forte de custo ou latencia, o modelo reduzido ainda seria aceitavel, mas nao e a melhor opcao se o objetivo principal for performance.

**Nuance tecnica**

O ranking de importancia veio de um modelo diferente do final (`RandomForestClassifier` em vez de `GradientBoostingClassifier`). Isso e aceitavel como exploracao, mas para uma defesa tecnica mais rigorosa seria melhor confirmar a importancia com o proprio modelo final ou com permutation importance.

---

## 2. As perguntas do notebook foram respondidas?

| Questao | Status | Observacao tecnica |
|---|---|---|
| Q1 - Naive predictor | Sim | A resposta esta no codigo e os resultados sao consistentes com o desbalanceamento. |
| Q2 - Model application | Parcialmente | O conteudo esta bem escrito, mas faltam referencias/citacoes formais, que a pergunta pede explicitamente. |
| Q3 - Escolha do melhor modelo | Sim | A justificativa e coerente com o F-score e o custo computacional. |
| Q4 - Explicacao leiga do modelo | Sim | A resposta e clara e adequada para nao tecnicos. |
| Q5 - Avaliacao final | Parcialmente | As metricas estao preenchidas, mas a discussao em texto nao aparece completa. |
| Q6 - Intuicao das features | Sim | A resposta esta presente, embora com texto editorial desnecessario no inicio. |
| Q7 - Feature importance | Sim | A comparacao com Q6 foi feita corretamente. |
| Q8 - Feature selection | Sim | A comparacao entre modelo completo e reduzido foi concluida. |

**Conclusao dessa verificacao**

As questoes substantivas foram respondidas, mas o notebook ainda precisa de limpeza editorial. O principal ponto em aberto e a ausencia de uma discussao textual clara em Q5 e a falta de referencias em Q2.

---

## 3. Fluxo tecnico recomendado com scikit-learn

### Objetivo primario

Construir um classificador que estime a probabilidade de uma pessoa ganhar mais de `50K` ao ano, para que a CharityML priorize os contatos com maior chance de retorno.

### Como o modelo final responde a pergunta?

O modelo nao diz "essa pessoa vai doar". Ele ordena os casos por probabilidade de pertencer ao grupo `>50K`. Na pratica, a CharityML pode usar esse score para priorizar campanhas e ajustar o limiar de decisao conforme custo e retorno.

### Como explicar para uma pessoa nao tecnica

O modelo aprende com exemplos antigos. Ele observa combinacoes de sinais como idade, horas trabalhadas, escolaridade, estado civil e ganhos de capital, e identifica padroes associados a maior renda. Depois, quando ve uma nova pessoa, ele compara esse perfil com o que aprendeu e estima quao provavel e que ela esteja no grupo de maior renda.

### Como validar se funciona no mundo real

- Verificar `F0.5` no teste final, porque ele favorece precision.
- Comparar contra baseline e contra modelo nao otimizado.
- Usar cross-validation para medir variabilidade.
- Avaliar a matriz de confusao e o custo de falsos positivos.
- Testar estabilidade em novas amostras ou novos periodos.
- Fazer checagens de fairness se variaveis sensiveis entrarem na decisao.

### Workflow recomendado

1. Definir a metrica de negocio.
2. Separar treino, validacao e teste com estratificacao.
3. Encapsular preprocessing em `Pipeline` e `ColumnTransformer`.
4. Treinar baseline.
5. Comparar candidatos com `cross_val_score` ou `GridSearchCV`.
6. Diagnosticar underfitting/overfitting pelo gap entre treino e validacao.
7. Selecionar o melhor modelo com base em `F0.5`.
8. Avaliar no teste uma unica vez.
9. Interpretar features ou importancias.
10. Monitorar o modelo apos uso.

### Exemplo de arquitetura com API do scikit-learn

```python
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, FunctionTransformer
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import make_scorer, fbeta_score
from sklearn.ensemble import GradientBoostingClassifier

skewed_features = ["capital-gain", "capital-loss"]
other_numeric_features = ["age", "education-num", "hours-per-week"]
categorical_features = [
    "workclass", "education_level", "marital-status", "occupation",
    "relationship", "race", "sex", "native-country"
]

preprocess = ColumnTransformer([
    ("skewed_num", Pipeline([
        ("log", FunctionTransformer(np.log1p, validate=False)),
        ("scaler", MinMaxScaler()),
    ]), skewed_features),
    ("num", MinMaxScaler(), other_numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
])

pipe = Pipeline([
    ("preprocess", preprocess),
    ("clf", GradientBoostingClassifier(random_state=42)),
])

param_grid = {
    "clf__n_estimators": [100, 200, 300],
    "clf__learning_rate": [0.05, 0.1, 0.2],
    "clf__max_depth": [2, 3, 4],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scorer = make_scorer(fbeta_score, beta=0.5)

search = GridSearchCV(pipe, param_grid=param_grid, scoring=scorer, cv=cv, n_jobs=-1)
search.fit(X_train, y_train)
```

### Como ler underfitting e overfitting nesse fluxo

- Se o score de treino for alto e o de validacao for bem menor, ha overfitting.
- Se ambos forem baixos, ha underfitting.
- Se treino, validacao e teste ficarem proximos, ha melhor indicio de generalizacao.

### Onde o notebook original simplifica demais

- Faz preprocessing fora de um pipeline.
- Usa um unico split como principal evidenca de performance.
- Nao discute variacao entre folds.
- Nao explicita o diagnostico de underfitting/overfitting.
- Nao formaliza o risco de leakage.

---

## 4. Conclusao executiva

O notebook esta tecnicamente correto na maior parte do fluxo e cumpre a proposta didatica da Udacity. Ele mostra bem o caminho padrao de um projeto supervisionado com scikit-learn: explorar, preprocessar, baseline, comparar modelos, tunar e interpretar features.

Os pontos mais fortes sao:

- boa definicao do problema de negocio;
- uso correto de `F0.5`;
- comparacao de modelos adequada;
- tuning com `GridSearchCV`;
- interpretacao por importancia de features;
- checagem de reducao de dimensionalidade.

Os principais pontos a melhorar sao:

- encapsular preprocessing em `Pipeline`;
- evitar data leakage;
- explicitar cross-validation e variabilidade;
- separar melhor analise tecnica e texto editorial;
- completar a justificativa com referencias em Q2 e narrativa em Q5.

Se a meta for usar isso como material de portifolio senior, o notebook ja tem a base certa, mas ainda vale uma refatoracao para deixa-lo mais rigoroso, reproducivel e defensavel tecnicamente.
