# Finding Donors for CharityML

## Guia Didatico do Projeto

Este documento e uma versao em portugues, mais explicativa e mais amigavel do README original do projeto `Finding Donors for CharityML`.

O objetivo aqui e ajudar voce a entender:
- qual problema estamos tentando resolver;
- quais arquivos sao importantes;
- como executar o projeto;
- o que existe dentro do dataset;
- como comecar a analise sem ficar perdido.

## 1. Visao geral do projeto

Neste projeto, queremos prever se uma pessoa possui renda anual:
- `<=50K`
- `>50K`

Essa previsao e importante porque, no contexto da CharityML, pessoas com renda maior que `50 mil dolares` sao tratadas como perfis com maior potencial de doacao.

Em outras palavras:

**o projeto tenta identificar quais individuos devem ser priorizados em campanhas de captacao.**

Do ponto de vista de ciencia de dados, este e um problema de:
- classificacao supervisionada;
- com duas classes;
- usando dados tabulares do censo.

## 2. Objetivo pratico

A CharityML nao quer apenas "acertar previsoes".

Ela quer usar os dados para tomar uma decisao operacional:

> Para quem vale a pena direcionar esforco e custo de outreach?

Por isso, o projeto nao deve ser visto so como um exercicio tecnico de modelo. Ele tambem e um exercicio de traducao entre:
- problema de negocio;
- preparacao de dados;
- escolha de metricas;
- interpretacao de resultados.

## 3. O que voce vai encontrar no projeto

O material base do projeto inclui:

- `finding_donors.ipynb`
  Notebook principal do exercicio, com explicacoes, perguntas e trechos de codigo para completar.

- `visuals.py`
  Arquivo auxiliar com funcoes de visualizacao usadas no notebook. Em geral, ele deve ser utilizado como suporte e nao como foco principal de alteracao.

- `census.csv`
  Base de dados principal usada para treino e analise.

- `test_census.csv`
  Arquivo de apoio com dados de teste.

## 4. Requisitos para executar

Voce precisa ter instalado:

- Python 3.x
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- Jupyter Notebook ou ambiente compativel com notebooks

O README original recomenda o uso de uma distribuicao como Anaconda, porque ela facilita a instalacao das bibliotecas mais comuns de ciencia de dados.

## 5. Como executar o notebook

A partir da pasta do projeto, voce pode abrir o notebook principal com um dos comandos abaixo:

```bash
ipython notebook finding_donors.ipynb
```

ou

```bash
jupyter notebook finding_donors.ipynb
```

Ao executar, o notebook sera aberto no navegador para que voce possa:
- ler o enunciado;
- completar as celulas de codigo;
- responder as perguntas do projeto;
- testar modelos supervisionados.

## 6. O que o dataset representa

A base utilizada e uma versao modificada do dataset de Census Income, originalmente associado ao artigo:

*"Scaling Up the Accuracy of Naive-Bayes Classifiers: a Decision-Tree Hybrid"*, de Ron Kohavi.

O dataset original esta relacionado ao UCI Machine Learning Repository.

Nesta versao do projeto:
- temos aproximadamente `32 mil` registros, segundo o README original;
- cada registro representa um individuo;
- cada individuo possui `13 features` de entrada;
- a variavel-alvo e `income`.

## 7. Variavel-alvo

A coluna que queremos prever e:

- `income`

Ela possui duas classes:
- `<=50K`
- `>50K`

Na pratica:
- `<=50K` representa individuos com renda anual de ate 50 mil dolares;
- `>50K` representa individuos com renda anual acima de 50 mil dolares.

## 8. Dicionario de dados explicado

Aqui esta uma versao mais didatica das colunas do dataset.

### Variaveis demograficas e de contexto pessoal

- `age`
  Idade da pessoa.

- `sex`
  Sexo registrado no dataset: `Female` ou `Male`.

- `race`
  Grupo racial informado no dataset.

- `native-country`
  Pais de origem da pessoa.

### Variaveis ligadas a educacao

- `education_level`
  Nivel educacional da pessoa, como `Bachelors`, `HS-grad`, `Masters` e outros.

- `education-num`
  Numero de anos de educacao completados.

Observacao importante:

`education_level` e `education-num` carregam informacoes muito relacionadas. Em analise exploratoria, vale observar se existe redundancia entre as duas.

### Variaveis ligadas ao trabalho

- `workclass`
  Tipo de vinculo ou classe de trabalho, como setor privado, governo ou trabalho autonomo.

- `occupation`
  Ocupacao profissional da pessoa.

- `hours-per-week`
  Numero medio de horas trabalhadas por semana.

### Variaveis ligadas ao contexto familiar

- `marital-status`
  Estado civil da pessoa.

- `relationship`
  Relacao familiar ou papel no nucleo familiar, como `Husband`, `Wife`, `Own-child` e outros.

### Variaveis financeiras

- `capital-gain`
  Ganho de capital monetario.

- `capital-loss`
  Perda de capital monetaria.

Essas duas variaveis costumam exigir atencao especial na analise, porque frequentemente apresentam forte assimetria e muitos valores zerados.

## 9. Como comecar a analise de forma mais inteligente

Quem esta comecando muitas vezes abre o notebook e parte direto para:
- fazer varios graficos;
- olhar a distribuicao de todas as colunas;
- testar modelos sem entender bem o problema.

Uma abordagem melhor e esta:

1. Entenda o objetivo de negocio.
2. Identifique a variavel-alvo.
3. Verifique qualidade basica da base.
4. Analise quais variaveis parecem mais relacionadas ao target.
5. Prepare os dados.
6. Treine modelos.
7. Compare resultados com metricas coerentes.
8. Interprete o que o modelo aprendeu.

## 10. Perguntas importantes que este projeto ajuda a responder

Durante a execucao do projeto, voce deve tentar responder perguntas como:

- Qual a proporcao de pessoas com renda `>50K`?
- O dataset esta balanceado ou desbalanceado?
- Quais variaveis parecem mais relevantes para separar as duas classes?
- Quais algoritmos fazem sentido para esse tipo de dado?
- Qual modelo entrega o melhor equilibrio entre desempenho e interpretacao?

## 11. Cuidados importantes

Alguns pontos merecem atencao ao longo do projeto:

- Nao confundir boa performance com boa explicacao de negocio.
- Nao usar muitos graficos sem uma pergunta analitica clara.
- Nao ignorar o impacto de classes desbalanceadas nas metricas.
- Nao esquecer que algumas variaveis podem trazer discussoes sobre vies e uso responsavel.

## 12. Leitura recomendada dos arquivos

Se voce estiver entrando no projeto agora, uma boa ordem de leitura e:

1. Este documento didatico.
2. O README original em [README.md](/home/fabiolima/Desktop/Finding_Donors_Project/cd0025-supervised-learning/starter/README.md).
3. O notebook principal [finding_donors.ipynb](/home/fabiolima/Desktop/Finding_Donors_Project/cd0025-supervised-learning/starter/finding_donors.ipynb).
4. O planejamento em [Finding_Donors_Project.md](/home/fabiolima/Desktop/Finding_Donors_Project/Finding_Donors_Project.md).

## 13. Resumo final

Este projeto e um excelente estudo de caso para praticar:
- entendimento de problema de negocio;
- preparacao de dados tabulares;
- classificacao supervisionada;
- comparacao de modelos;
- interpretacao de variaveis importantes.

Se voce entender bem este fluxo, o notebook deixa de ser apenas um exercicio e passa a ser um exemplo completo de raciocinio analitico aplicado.
