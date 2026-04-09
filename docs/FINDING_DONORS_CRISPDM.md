# Finding Donors - CRISP-DM

## 1. Visao Geral Executiva

Este projeto aplica o framework CRISP-DM ao conjunto de dados da CharityML com o objetivo de apoiar a priorizacao de potenciais doadores. Em vez de tratar o problema como uma analise puramente estatistica, a proposta foi desenhada como um fluxo analitico completo, partindo da necessidade de negocio ate a avaliacao do modelo e a sua futura utilizacao em inferencia.

A ideia central e simples: identificar pessoas com maior probabilidade de renda acima de `50K` e, a partir disso, priorizar campanhas de captação mais eficientes. Na pratica, isso significa reduzir custo operacional, melhorar a taxa de resposta e concentrar os esforcos de outreach nos perfis mais promissores.

O estudo foi consolidado em um notebook analitico e reproduzivel, com documentacao passo a passo. Este documento sintetiza esse trabalho em uma narrativa unica, adequada para leitura de gestores e stakeholders tecnicos e nao tecnicos.

## 2. Problema de Negocio

A CharityML precisa decidir para quem direcionar campanhas de doacao. Como o orcamento e o tempo sao limitados, nao e viavel abordar toda a base com o mesmo nivel de investimento. O problema, portanto, e de priorizacao: como estimar quem tem maior probabilidade de se tornar doador com base em dados cadastrais e socioeconomicos?

A variavel-alvo utilizada no estudo e a faixa de renda `>50K`, que funciona como proxy de capacidade e propensao de doacao. O objetivo nao e afirmar que renda alta garante doacao, mas sim construir um criterio pratico para ordenacao e segmentacao da base.

## 3. Metodo Aplicado: CRISP-DM

### 3.1 Business Understanding

Nesta etapa foi delimitado o objetivo de negocio, o publico de interesse e o ganho esperado com a aplicacao analitica. A prioridade foi transformar uma necessidade operacional de marketing e captação em um problema de classificacao binaria, com foco em valor pratico para a organizacao.

### 3.2 Data Understanding

A analise exploratoria mostrou um dataset com classes desbalanceadas, o que torna o problema mais realista e mais desafiador. Isso e importante porque um modelo pode parecer bom em acuracia apenas por repetir a classe majoritaria, sem realmente localizar os doadores potenciais.

Tambem foram observados pontos relevantes para a preparacao:

- existe redundancia entre algumas variaveis, como `education-num` e `education`;
- ha variaveis com distribuicao altamente assimetrica, como `capital-gain` e `capital-loss`;
- algumas colunas sao mais adequadas para auditoria analitica do que para uso direto em producao, como atributos sensiveis;
- o conjunto contem categorias raras, principalmente em `native-country`.

Essas observacoes orientaram diretamente as decisoes da etapa seguinte.

### 3.3 Data Preparation

A preparacao dos dados foi estruturada para evitar vazamento de informacao e para deixar o fluxo pronto para machine learning com boas praticas de `scikit-learn`.

As principais decisoes foram:

- separacao treino/teste antes de qualquer ajuste de transformacao;
- uso de `Pipeline` e `ColumnTransformer` para garantir reaplicacao consistente do preprocessamento;
- `OneHotEncoder(handle_unknown="ignore")` para variaveis categoricas;
- `MinMaxScaler` para variaveis numericas quando necessario;
- criacao de indicadores para `capital-gain` e `capital-loss`, combinados com transformacao logaritmica `log1p` quando apropriado;
- remocao de `fnlwgt`, por ter utilidade limitada no objetivo proposto;
- exclusao de `education-num` quando a codificacao de `education` ja capturava a mesma informacao de forma mais apropriada para o fluxo;
- manutencao de duas versoes de base: uma mais segura para producao e outra mais completa para auditoria exploratoria.

O ponto mais importante desta etapa e que o preprocessamento passou a fazer parte do proprio fluxo de modelagem, e nao mais uma transformacao separada e manual. Isso reduz risco de leakage, aumenta rastreabilidade e simplifica manutencao.

### 3.4 Modeling

A modelagem nao foi tratada como uma disputa aleatoria de algoritmos. A selecao dos modelos considerou a natureza do problema, o desbalanceamento de classes e a necessidade de interpretabilidade e generalizacao.

Foram incluidos baselines e modelos mais consistentes com o caso:

- `DummyClassifier(strategy="most_frequent")`, como benchmark minimo;
- um baseline ingenuo de previsao positiva, para comparar o custo de errar menos o recall versus manter alta precisao;
- `LogisticRegression`, por ser um classificador forte, simples e interpretable;
- `LogisticRegression` com tratamento de desbalanceamento;
- `RandomForestClassifier`, por capturar nao linearidades e interacoes;
- `HistGradientBoostingClassifier`, como candidato mais flexivel para o conjunto de dados.

A avaliacao foi feita com `StratifiedKFold` e `cross_validate`, analisando metricas como precisao, recall, `F0.5` e acuracia. Tambem foram usados learning curves para inspecao visual de overfitting e underfitting, alem de leitura de bias e variance como parte da interpretacao do comportamento dos modelos.

### 3.5 Hyperparameter Tuning

Depois de escolher o melhor candidato, o notebook aplica otimização de hiperparametros com `RandomizedSearchCV`. Esta escolha e apropriada porque permite explorar um espaco de busca maior com custo computacional controlado.

Os hiperparametros mais relevantes para esse tipo de problema incluem:

- `learning_rate`, que controla quao rapidamente o modelo aprende;
- profundidade do modelo, que controla complexidade e risco de overfitting;
- parametros de regularizacao e tamanho minimo de folhas, quando aplicavel.

A logica foi:

1. definir um espaco de busca coerente com o modelo vencedor;
2. executar busca aleatoria com validacao cruzada estratificada;
3. comparar o desempenho tuneado com o modelo original;
4. manter apenas o melhor pipeline para a etapa final de avaliacao.

### 3.6 Evaluation

A avaliacao final usa o conjunto de holdout separado desde o inicio. Isso garante uma estimativa mais honesta da capacidade de generalizacao do modelo.

Nesta fase foram feitos:

- calculo de metricas no holdout;
- comparacao com baselines;
- ajuste de threshold para priorizar a estrategia mais alinhada ao negocio;
- matriz de confusao e `classification_report`;
- auditoria inicial por subgrupos para sinalizar possiveis disparidades.

O criterio principal de sucesso nao foi apenas acuracia, mas o equilibrio entre identificar o maior numero possivel de potenciais doadores e manter uma taxa aceitavel de falsos positivos. Em um contexto de campanha, esse equilibrio tem impacto direto em custo e retorno.

## 4. Resultados Analiticos

O projeto mostrou que e possivel ir alem de um baseline ingenuo e construir um fluxo mais robusto para triagem de potenciais doadores. O valor do trabalho nao esta apenas no modelo final, mas no processo:

- as etapas ficaram reproduziveis;
- o risco de leakage foi reduzido;
- a comparacao entre modelos foi documentada;
- a interpretacao do comportamento do modelo ficou mais transparente;
- o tuning foi conduzido de forma controlada;
- a avaliacao final ficou separada da escolha do modelo.

Em termos executivos, o estudo entrega um pipeline que pode ser usado para priorizar campanhas com mais criterio e menor desperdicio de esforco.

## 5. O Que e Inferencia

Inferencia e o uso do modelo treinado em dados novos, ainda nao vistos durante o treinamento. Em termos praticos, e quando o modelo sai do ambiente de estudo e passa a operar sobre novos registros para gerar uma predicao.

No caso deste projeto, a inferencia significa receber um novo perfil cadastral e estimar a probabilidade de aquela pessoa pertencer ao grupo de renda mais alta, usando o pipeline completo de preprocessamento e classificacao.

## 6. Como Este Notebook Pode Ser Usado

O notebook foi construído para servir como base analitica e tambem como ponte para uso futuro em producao. Ele pode ser aproveitado de tres formas:

1. como documento de estudo, para entender a logica da solucao;
2. como referencia tecnica, para reproduzir preprocessamento, modelagem e avaliacao;
3. como embrião de um pipeline de inferencia, desde que empacotado com o mesmo preprocessamento treinado e monitorado em producao.

Depois de escolhido o melhor modelo, o fluxo correto e:

1. otimizar hiperparametros;
2. refinar o threshold, se isso fizer sentido para o objetivo do negocio;
3. validar no holdout apenas uma vez;
4. persistir o pipeline final;
5. implantar a inferencia;
6. monitorar desempenho ao longo do tempo.

## 7. Conclusao

O estudo foi estruturado para responder a pergunta de negocio de forma pratica, rastreavel e tecnicamente solida. A principal contribuicao nao e apenas um classificador, mas um processo completo de analise de dados aplicado ao contexto de captação de doadores.

Para um gestor, a mensagem final e esta: o projeto organiza dados, compara alternativas, escolhe um modelo com criterio, ajusta a solucao e entrega um caminho claro para uso operacional.
