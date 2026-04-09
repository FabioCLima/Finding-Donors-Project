# Revisão Técnica — Finding Donors Notebook (CRISP-DM Template)

**Documento:** `notebooks/finding_donors_version_study.ipynb`  
**Revisor:** Papel de cientista de dados sênior / gestor técnico  
**Escopo:** Seções `01_Business Understanding` e `02_Data Understanding`  
**Objetivo da revisão:** Elevar o notebook ao nível de template público CRISP-DM no GitHub — claro para júniores, rigoroso para sêniores

---

## Sumário executivo

O notebook tem conteúdo técnico de alta qualidade. As análises são corretas, as hipóteses estão bem formuladas e a conexão com o problema de negócio é consistente. Os problemas identificados são principalmente de **ordem de células**, **redundância de conteúdo** e **lacunas de numeração**, que atrapalham a leitura linear e reduzem o valor como template didático.

**Principais problemas:**

| # | Problema | Impacto | Prioridade |
|---|---|---|---|
| 1 | `Cell [01]` solta antes da seção 1 começa | Quebra o fluxo imediato | Alta |
| 2 | Seções 1.3 e 1.4 ausentes (salto numérico) | Confusão de estrutura para leitores | Alta |
| 3 | Dois diagramas Mermaid sobrepostos (células 07/08) | Redundância, confusão de propósito | Alta |
| 4 | Células [17] e [19] duplicam a mesma hipótese H1 | Repetição que desoriento leitores | Alta |
| 5 | Cálculo de `baseline` repetido em cada hipótese | Ruído de código e má prática | Média |
| 6 | Código de conversão `income → target` repetido em H2 | Inconsistência e confusão | Média |
| 7 | Funções auxiliares (2.3) aparecem *depois* da análise | Ilógico para leitura linear | Média |
| 8 | Tabela consolidada (célula 98) com instrução de preenchimento em aberto | Parece inacabado | Média |
| 9 | Célula [100] de "como atualizar o Hypothesis Map" quebra a narrativa | Instrução operacional no meio da análise | Baixa |
| 10 | Matriz de confusão (célula 03) aparece no lugar errado | Dificulta raciocínio progressivo | Alta |

---

## Seção 1 — Business Understanding

### 1.1 Problemas de ordem e estrutura

#### Problema 1 — `Cell [01]` está fora do lugar

A célula com "Premissas já conhecidas do contexto" aparece **antes** da seção 1 começar, logo após a introdução geral. O conteúdo desta célula (tipo de problema, target, métrica principal) é material de abertura do Business Understanding, não uma nota avulsa.

**Impacto:** Um leitor júnior vai achar que isso é um apêndice da introdução e não vai entender que essas premissas são fundamentais para o projeto.

**Recomendação:**
- Integrar o conteúdo desta célula à seção `1.1 Contexto de negócio` (cell [02]) como um bloco destacado (blockquote ou tabela de premissas), **antes** de elaborar o texto.
- Ou criar uma seção numerada explícita: `1.0 Premissas e contexto de entrada` para que fique clara a sua posição no framework.

---

#### Problema 2 — Salto numérico: onde estão as seções 1.3 e 1.4?

O notebook passa de `1.2 Problema analítico` diretamente para `1.5 Critério de sucesso de negócio`. As seções 1.3 e 1.4 simplesmente não existem.

**Impacto:** Em um template CRISP-DM, a numeração sequencial é essencial para que leitores identifiquem o que está faltando ou o que foi abreviado. Um júnior vai procurar 1.3 e se perguntar se pulou uma parte importante.

**Recomendação:** Escolha uma das abordagens:
- **Opção A (simples):** Renumerar as seções existentes de forma contínua (`1.1`, `1.2`, `1.3`, etc.) sem lacunas.
- **Opção B (recomendada para template CRISP-DM):** Criar explicitamente as seções ausentes com marcação de `TODO` ou conteúdo mínimo que indique o que deveria estar ali, como por exemplo:
  - `1.3 Restrições e premissas do projeto` — dados disponíveis, limitações de uso, contexto legal
  - `1.4 Inventário de dados` — overview inicial das fontes antes da EDA formal

O importante é que a numeração nunca salte, especialmente em um template.

---

#### Problema 3 — Matriz de confusão (cell [03]) no lugar errado

A célula [03] — que explica VP, FN, FP, VN, Precision, Recall, F1 e F-beta — aparece **entre** a definição do problema analítico (1.2) e o dicionário de variáveis. Essa posição quebra o raciocínio progressivo.

**Por que está errada aqui:** O leitor ainda não sabe qual métrica vai ser usada (isso só vem na seção 1.6). Apresentar a matriz de confusão e todas as métricas antes de justificar *por que* F-beta é a métrica certa inverte a lógica pedagógica.

**Ordem correta (recomendada):**
```
1.1 Contexto de negócio
1.2 Problema analítico
1.X Critério de sucesso de negócio      ← 1.5 atual
1.X Critério de sucesso analítico       ← 1.6 atual (justifica F-beta)
1.X Métricas e interpretação            ← AQUI move a célula [03]
1.X Riscos e cuidados                   ← 1.7 atual
```

A matriz de confusão é muito mais eficaz depois que o leitor já entendeu **por que** precisamos de F-beta. A sequência lógica é: definir o custo do erro → escolher métrica → explicar a métrica.

---

#### Problema 4 — Dois diagramas Mermaid sobrepostos (células [07] e [08])

A célula [07] é um `mindmap` sobre "Criação de hipóteses analíticas" (processo geral de como criar hipóteses). A célula [08] é um `graph TD` com o "Mapa Mental das Hipóteses" (as hipóteses específicas do projeto com status).

**Impacto:** Os dois diagramas têm aparência similar e propósitos diferentes, mas aparecem em sequência sem separação clara. Para um júnior, parece redundância. Para o template, o mindmap genérico (cell 07) mistura conteúdo didático sobre o *processo* com conteúdo analítico sobre *este projeto*.

**Recomendação:**
- **Manter apenas o `graph TD` (cell [08])**, que é específico do projeto e tem valor analítico direto (hipóteses com status).
- O `mindmap` genérico (cell [07]) poderia ir para uma seção de `📚 Referência metodológica` ou ser removido para manter o foco no projeto.
- Se o objetivo é didático (ensinar como criar hipóteses), separar visualmente com um cabeçalho explícito do tipo `> 💡 Como estruturar hipóteses analíticas (referência geral)`.

---

#### Problema 5 — Célula [09] "Regra final" está descontextualizada

A célula com "Hipótese boa conecta negócio, mecanismo plausível, dado disponível e decisão analítica" aparece solta após os dois diagramas, sem vínculo claro com o que vem antes ou depois.

**Recomendação:** Integrar esse parágrafo como nota de encerramento **dentro** da seção 1.8 (Hipóteses analíticas iniciais), logo após as hipóteses serem apresentadas. Isso fecha o raciocínio sobre hipóteses de forma natural.

---

### 1.2 O que está bom na seção 1

- A seção `1.1 Contexto de negócio` é direta e conecta negócio com análise de forma eficaz.
- A seção `1.2 Problema analítico` traduz o problema de negócio para linguagem técnica com um bom fluxograma Mermaid. Isso é exatamente o nível certo para um template público.
- O **dicionário semântico de variáveis** (cell [04]) está bem justificado e é uma adição valiosa ao Business Understanding — raramente visto em projetos públicos no GitHub.
- As hipóteses H1–H6 (seção 1.8) estão formuladas no formato correto: mecanismo plausível + evidência esperada + variáveis envolvidas.
- A seção `1.9 Evidências rápidas` e `1.10 Roteiro recomendado` são excelentes como ponte entre Business Understanding e Data Understanding.

---

## Seção 2 — Data Understanding

### 2.1 Problemas de ordem e estrutura

#### Problema 6 — Células [17] e [19] duplicam o mesmo conteúdo (H1)

Para a Hipótese H1, há **dois blocos de introdução** consecutivos:

- **Cell [17]:** "Hipótese 1 -- Escolaridade e Renda" — introdução mais simples, com perguntas em linguagem natural.
- **Cell [18]:** Lista numerada com os passos analíticos (1. calcular baseline, 2. agrupar...).
- **Cell [19]:** "Hipótese H1 — Escolaridade está associada à renda acima de 50K" — introdução mais formal, com notação matemática, baseline definida com fórmula LaTeX e explicação do raciocínio preditivo.

**Resultado:** O leitor lê a mesma hipótese introduzida duas vezes antes de ver qualquer código. Isso dilui o conteúdo e gera confusão sobre qual versão é a "oficial".

**Recomendação:** Manter **apenas a célula [19]** como introdução de H1. Ela é mais completa, matematicamente precisa e mais adequada para um template. A célula [17] deve ser removida. A lista de passos da célula [18] pode ser incorporada ao início da célula [19] como estrutura lógica da análise.

**Importante:** Verificar se o mesmo padrão de duplicação ocorre nas hipóteses H2–H6. H2 (células [32]/[33]) e H3 (célula [53]) parecem seguir o padrão correto (uma única introdução), mas vale validar antes de publicar.

---

#### Problema 7 — Cálculo de `baseline` repetido em cada hipótese

Em cada grupo semântico, o código repete:

```python
baseline = df["target"].mean()
print(f"Taxa marginal (baseline): {baseline:.1%}")
```

Isso aparece nas células [25], [54], [66], [88] — e provavelmente em outros grupos.

**Impacto:** Para um leitor (e para quem está aprendendo), ver essa linha repetida pode sugerir que o valor muda entre grupos, quando na verdade é uma constante do dataset. Além disso, enche o notebook de ruído.

**Recomendação:**
- Calcular `baseline` **uma única vez** na célula de sanidade estrutural (seção 2.1/2.2, cell [15]).
- Nos blocos de hipótese, apenas referenciar no comentário: `# baseline = 0.248 (calculada na seção 2.2)` e usar a variável diretamente.
- Isso também seria bom para ensinar a prática de não recalcular constantes em loops.

---

#### Problema 8 — Código de conversão `income → target` repetido em H2

A conversão da coluna `income` para binário (`target`) foi feita na célula [20] para H1. A mesma transformação aparece novamente na célula [35] no contexto de H2.

**Impacto:** Sugere que o notebook foi desenvolvido de forma incremental e não foi consolidado. Para um template, o leitor assume que o código roda em sequência — ter a mesma transformação duas vezes causa confusão e pode gerar erros se executado fora de ordem.

**Recomendação:** A conversão `income → target` deve estar **uma única vez**, na célula de setup da seção 2.2 (leitura do target), e depois ser apenas referenciada no texto das hipóteses.

---

#### Problema 9 — Funções auxiliares (seção 2.3, cell [101]) aparecem depois da análise

As funções `taxa_positiva_por_categoria`, `plot_target_distribution`, `plot_categorical_vs_target`, `plot_numeric_vs_target`, `plot_binned_positive_rate` e `plot_sparse_signal` estão definidas **depois** que toda a análise hipótese por hipótese já foi feita (cells [16]–[100]).

**Impacto:** A análise das hipóteses (H1–H6) foi feita com código inline, e depois aparecem funções que fazem a mesma coisa de forma mais organizada. Para o leitor, parece que há dois métodos paralelos de análise sem justificativa.

**Recomendação:** Escolha uma de duas abordagens:
- **Opção A (template limpo):** Mover as funções auxiliares para o início da seção 2 (antes da análise exploratória), usar apenas as funções durante as hipóteses, e remover o código inline duplicado. Isso é o padrão mais limpo para um template.
- **Opção B (didático):** Manter o código inline nas primeiras hipóteses (H1, H2) como demonstração passo a passo, depois apresentar as funções como "refatoração" e usá-las para H3–H6. Isso ensina o raciocínio de abstração progressiva — mas requer um texto explicando a transição.

A opção B é mais pedagógica para um leitor júnior. Se o objetivo é ser um template didático, ela é a mais adequada — mas precisa de texto de transição explícito.

---

#### Problema 10 — Tabela consolidada (cell [98]) parece inacabada

A tabela em cell [98] tem a instrução: *"Preencha a coluna **Amplitude observada** após executar cada bloco de hipótese acima."*

Toda a análise de H1–H6 já foi feita. A tabela deveria estar preenchida com os valores calculados. Deixá-la com instrução de preenchimento em aberto faz o notebook parecer um rascunho.

A célula [99] parece calcular os valores programaticamente, mas o resultado não está consolidado visualmente na tabela.

**Recomendação:** Substituir a instrução de preenchimento pela tabela já preenchida com os valores de amplitude observados para cada variável (education, occupation, age, hours-per-week, marital-status, relationship, capital-gain, capital-loss). Isso fecha a seção de forma profissional.

---

#### Problema 11 — Célula [100] "Como atualizar o Hypothesis Map" quebra a narrativa analítica

Esta célula é instrução operacional sobre como editar o arquivo `Hypothesis_Map.md`. Ela aparece no meio da seção 2, entre a tabela consolidada e as funções auxiliares.

**Impacto:** Quebra completamente o fluxo analítico. Um leitor júnior vai parar aqui esperando aprender algo sobre os dados, mas vai encontrar instruções de manutenção de arquivo.

**Recomendação:** Mover esta célula para o final da seção 2 (fechamento) ou para um bloco separado de `📋 Housekeeping / Atualizações de rastreamento`. O conteúdo é válido, mas precisa estar no lugar certo.

---

#### Problema 12 — Tabela de variáveis (cell [116]) está deslocada

A tabela detalhada de variáveis com colunas `Papel analítico`, `Padrão observado`, `Risco/atenção` e `Implicação para modelagem` aparece **depois** da célula de instruções sobre o Hypothesis Map.

Esta tabela é um dos entregáveis mais valiosos da seção 2. É o documento de decisão que conecta EDA com preparação de dados.

**Recomendação:** Mover esta tabela para logo depois da tabela consolidada de poder discriminativo (cell [98/99]), antes de qualquer conteúdo operacional ou de housekeeping. A ordem ideal seria:

```
[análise H6]
→ Tabela consolidada: amplitude por variável
→ Tabela de variáveis: papel, padrão, risco, implicação para modelagem  ← aqui
→ Registro de insights
→ Fechamento da seção 2
→ [instruções operacionais como housekeeping, se mantidas]
```

---

### 2.2 O que está bom na seção 2

- A **abertura da seção 2** (cell [13]) é precisa: define objetivo e entregáveis esperados sem redundância.
- A **estrutura por grupos semânticos** (H1 Capital Humano → H6 Variáveis Sensíveis) é excelente como padrão de template. Outros projetos podem seguir exatamente essa estrutura.
- A **seção de variáveis sensíveis (H6)** é um diferencial raro em notebooks públicos. A separação entre "a variável tem sinal estatístico" e "deveria ser usada na decisão de negócio?" é exatamente o nível de maturidade analítica que um template CRISP-DM deve demonstrar.
- As **conclusões de hipótese** ao final de cada grupo são bem estruturadas e objetivas. Seguem o padrão: hipótese confirmada/refutada + evidência principal + implicação para modelagem.
- O **cruzamento entre H1 e H2** (educação × ocupação) mostra raciocínio analítico avançado — pensar em interação entre variáveis antes da modelagem é um sinal importante.
- O **tratamento de capital-gain e capital-loss** (H5) como variáveis esparsas é tecnicamente correto e bem explicado. A decisão de usar flag binária além do valor bruto está bem justificada.
- O **Registro orientado de insights** (cell [117]) é um padrão excelente para documentação analítica.

---

## Recomendações prioritárias de ação

Ordenadas por impacto na clareza para um leitor júnior e na qualidade do template:

### Prioridade Alta (impacto direto na legibilidade)

1. **Reordenar seção 1:** Mover a célula [03] (Matriz de confusão) para depois das seções 1.5/1.6. A sequência correta é: problema → critério de sucesso → justificativa da métrica → explicação detalhada da métrica.

2. **Eliminar a duplicação de H1:** Remover a célula [17] e incorporar a lista de passos da célula [18] dentro da célula [19]. Verificar se a duplicação existe em outras hipóteses.

3. **Resolver a numeração da seção 1:** Eliminar o salto entre 1.2 e 1.5. Ou renumerar sequencialmente, ou criar explicitamente as seções 1.3 e 1.4 com conteúdo ou marcação de `TODO`.

4. **Integrar a célula [01]** ao início da seção 1.1 como bloco de premissas, não como célula avulsa.

### Prioridade Média (impacto na qualidade do template)

5. **Consolidar o cálculo de `baseline`:** Calcular uma vez na seção 2.2 e usar a variável ao longo do notebook.

6. **Remover a repetição da conversão `income → target`:** Garantir que está apenas na célula de setup.

7. **Mover a tabela de variáveis (cell [116])** para logo após a tabela consolidada de amplitude.

8. **Preencher a tabela consolidada** (cell [98]) com os valores já calculados, ou garantir que o código da cell [99] exibe o resultado completo e a instrução de preenchimento manual é removida.

9. **Decidir sobre as funções auxiliares (seção 2.3):** Ou movê-las para antes da análise (template limpo), ou criar uma seção de transição explicando a refatoração (abordagem didática).

### Prioridade Baixa (refinamento)

10. **Fundir ou remover um dos dois diagramas Mermaid** (cells [07] e [08]) para evitar confusão.

11. **Mover cell [100]** (instrução de atualização do Hypothesis Map) para o fechamento da seção 2 ou para um bloco de housekeeping separado.

12. **Integrar a célula [09]** ("Regra final para hipóteses") como nota de fechamento da seção 1.8.

---

## Estrutura recomendada para seção 1 (ordem de células)

```
Cell [00] — Introdução / Título do projeto
Cell [02] — 1.1 Contexto de negócio  (+ premissas de Cell [01] integradas)
Cell [02] — 1.2 Problema analítico   (mantém o flowchart Mermaid)
           [NOVA] 1.3 Restrições e premissas / 1.4 Inventário de dados (ou TODO)
Cell [05] — 1.5 Critério de sucesso de negócio
Cell [05] — 1.6 Critério de sucesso analítico (justifica F-beta)
Cell [03] — 1.X Métricas e interpretação (Matriz de confusão aqui, após justificativa)
Cell [05] — 1.7 Riscos e cuidados
Cell [04] — 1.X Dicionário semântico de variáveis
Cell [06] — 1.8 Hipóteses analíticas iniciais (H1–H6)
           [Cell 09 integrada aqui como fechamento]
Cell [08] — Mapa Mental das Hipóteses (graph TD — manter apenas este)
Cell [10] — 1.9 Evidências rápidas observadas
Cell [11] — 1.10 Roteiro recomendado para Data Understanding
```

---

## Estrutura recomendada para seção 2 (ordem de células)

```
Cell [13] — Objetivo e entregáveis da seção
Cell [12] — Setup (imports, carregamento)
           [Funções auxiliares aqui se usar Opção A]
Cell [14] — 2.1 Sanidade estrutural
Cell [15] — 2.2 Target e baseline  (baseline calculada UMA VEZ aqui)
Cell [16] — Introdução: EDA dirigida por hipóteses
           [Análise H1-H6 com células refinadas]
           [Tabela consolidada de amplitude preenchida]
           [Tabela de variáveis: papel/padrão/risco/implicação]
           [Registro de insights]
           [Fechamento da seção 2]
           [Housekeeping: instrução de atualização do Hypothesis Map]
```

---

## Nota final

O notebook já está bem acima da média do que se vê em repositórios públicos de CRISP-DM. O nível de documentação das hipóteses, a lógica da análise e o cuidado com variáveis sensíveis são diferenciais reais. As correções sugeridas aqui são de estrutura e ordem — não de conteúdo. Com os ajustes de reordenação e deduplicação, este notebook tem qualidade para servir como referência pública de como conduzir Business Understanding e Data Understanding de forma profissional e reprodutível.
