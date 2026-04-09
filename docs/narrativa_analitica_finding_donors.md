# Finding Donors for CharityML

## Narrativa Analitica Didatica

Este documento foi escrito para servir como uma leitura guiada do estudo, sem codigo e sem depender da ordem das celulas do notebook. A ideia e simples: cada secao responde uma pergunta analitica, mostra o resultado principal e explica por que aquela variavel merece atencao.

O objetivo e que, ao terminar a leitura, voce consiga responder com clareza:

- qual e a decisao de negocio apoiada pelo estudo;
- por que certas variaveis aparecem como prioritarias;
- o que cada grupo de variaveis esta tentando explicar;
- quais conclusoes de Data Understanding realmente importam para as proximas etapas do CRISP-DM.

## 1. Business Understanding

O objetivo maior do projeto e ajudar a CharityML a decidir quem deve ser priorizado nas campanhas de captacao. Como a organizacao nao quer desperdicar esforco com contatos pouco promissores, o problema foi traduzido para prever se uma pessoa pertence ao grupo com renda anual acima de `50 mil dolares`, usado aqui como proxy de maior capacidade de doacao. Em termos simples: o estudo nao quer apenas "prever renda"; ele quer apoiar uma lista de prioridade para outreach com mais eficiencia.

## 2. Como Ler a Etapa de Data Understanding

Depois da sanidade estrutural da base, a analise deixa de perguntar apenas "como sao os dados?" e passa a perguntar "quais variaveis realmente ajudam a separar a classe `>50K` da classe `<=50K`?".

Essa etapa fica mais clara quando organizada por grupos semanticos. Em vez de ler uma sequencia de graficos soltos, lemos uma historia:

1. capital humano;
2. ocupacao e insercao profissional;
3. ciclo de carreira e intensidade de trabalho;
4. estrutura familiar;
5. eventos financeiros raros;
6. variaveis sensiveis e de contexto;
7. variaveis de apoio e de menor prioridade.

## 3. Mapa Rapido das Variaveis

| Variavel | Grupo semantico | Hipotese central | Resultado principal | Prioridade |
|---|---|---|---|---|
| `education_level` | Capital humano | Escolaridade mais alta aumenta a chance de `>50K` | O gradiente educacional e muito forte | Alta |
| `education-num` | Capital humano | Versao ordinal da escolaridade separa bem as classes | Sinal forte e mais compacto que `education_level` | Alta |
| `occupation` | Situacao ocupacional | Ocupacoes mais qualificadas concentram mais `>50K` | `Exec-managerial` e `Prof-specialty` se destacam | Alta |
| `workclass` | Situacao ocupacional | Tipo de vinculo de trabalho ajuda a explicar renda | Ha sinal, mas menor que em `occupation` | Media |
| `age` | Ciclo de carreira | A chance de `>50K` cresce com a maturidade economica, mas nao linearmente | Pico em faixas intermediarias da vida adulta | Alta |
| `hours-per-week` | Intensidade de trabalho | Jornadas maiores tendem a aparecer mais na classe positiva | O efeito existe, mas nao e linear simples | Alta |
| `marital-status` | Estrutura familiar | Arranjo conjugal ajuda a diferenciar renda | `Married-civ-spouse` fica muito acima da media | Alta |
| `relationship` | Estrutura familiar | Papel no domicilio captura contexto economico do individuo | `Wife` e `Husband` concentram mais `>50K` | Alta |
| `capital-gain` | Evento financeiro raro | Ter ganho de capital e um sinal forte de renda alta | Mesmo raro, separa muito bem as classes | Alta |
| `capital-loss` | Evento financeiro raro | Perda de capital tambem pode carregar sinal economico | Sinal relevante, mas menor que `capital-gain` | Media/Alta |
| `sex` | Sensivel | Pode ter sinal preditivo, mas exige cautela | Diferencas existem, mas o uso e delicado | Diagnostico |
| `race` | Sensivel | Pode aparecer como sinal, mas com risco etico | Diferencas existem, com cuidado extra | Diagnostico |
| `native-country` | Sensivel/contextual | Pode capturar contexto, mas com alta fragmentacao | Ha categorias com taxa alta, mas volumes pequenos | Diagnostico |
| `fnlwgt` | Peso amostral | Pode ser util na amostra, nao necessariamente na previsao | Nao e prioridade como feature preditiva | Baixa |

## 4. Hipotese 1: Capital Humano

### Pergunta analitica

Pessoas com maior escolaridade apresentam maior probabilidade de estar na classe `>50K`?

### Como responder a essa pergunta

A forma correta de responder nao e olhar apenas a distribuicao de escolaridade na base. O importante e comparar, para cada nivel educacional, qual e a taxa de pessoas com renda acima de `50K`. A pergunta deixa de ser "qual categoria aparece mais?" e passa a ser "em qual categoria a chance de `>50K` e maior?".

### Insight principal

Sim. O efeito da escolaridade e um dos mais fortes de todo o estudo. Ha um gradiente muito claro: categorias educacionais mais altas concentram taxas positivas muito acima da media da base.

### Resultado por variavel

#### `education_level`

O resultado mostra uma escada educacional bastante coerente. Niveis como `Prof-school` e `Doctorate` ficam acima de `73%` de classe positiva. `Masters` tambem aparece muito acima da media, com cerca de `55%`, e `Bachelors` com cerca de `42%`. Em contraste, `HS-grad` fica perto de `16%`, e niveis mais baixos ficam ainda menores.

Leitura final da variavel: `education_level` e importante porque separa muito bem grupos de baixa e alta renda de forma intuitiva e interpretavel.

#### `education-num`

Essa variavel conta a mesma historia de forma ordinal e mais compacta. Nas faixas mais baixas de escolaridade, a taxa de `>50K` fica perto de `6%`. Em niveis intermediarios ela sobe para a casa de `20%` a `37%`. Nas faixas mais altas, ultrapassa `60%`.

Leitura final da variavel: `education-num` e uma das candidatas mais fortes do estudo porque preserva o gradiente de escolaridade de forma simples, compacta e analiticamente muito util.

### Por que esse grupo e prioritario

Esse grupo e prioritario porque combina tres qualidades ao mesmo tempo:

- faz sentido do ponto de vista economico;
- mostra separacao forte entre as classes;
- gera uma decisao concreta para a etapa seguinte: revisar a redundancia entre `education_level` e `education-num`.

### Implicacao analitica

O estudo sugere que escolaridade deve entrar cedo na modelagem, mas com critero. Como `education_level` e `education-num` carregam praticamente a mesma historia, faz sentido comparar se vale manter as duas ou priorizar a representacao ordinal.

## 5. Hipotese 2: Ocupacao e Insercao Profissional

### Pergunta analitica

O tipo de ocupacao e de vinculo de trabalho ajuda a diferenciar pessoas com maior probabilidade de renda `>50K`?

### Como responder a essa pergunta

A resposta vem de comparar taxa positiva por categoria, sempre olhando volume junto com a taxa. Nao basta uma ocupacao ter percentual alto se ela quase nao aparece na base.

### Insight principal

Sim. O tipo de ocupacao ajuda bastante a separar classes. O tipo de vinculo de trabalho tambem ajuda, mas com menos forca do que a ocupacao em si.

### Resultado por variavel

#### `occupation`

As ocupacoes `Exec-managerial` e `Prof-specialty` aparecem como os sinais mais fortes e mais estaveis, com taxas perto de `48%` e `45%`. Isso e relevante porque nao sao categorias pequenas; elas tambem tem alto volume. Ja ocupacoes como `Adm-clerical` e `Machine-op-inspct` ficam bem abaixo.

Leitura final da variavel: `occupation` e prioritaria porque oferece separacao forte com volume suficiente para o padrao parecer confiavel.

#### `workclass`

Aqui o sinal existe, mas e menos determinante. `Self-emp-inc` e `Federal-gov` aparecem acima da media, enquanto `Private` fica mais proximo do comportamento geral da base. O tipo de vinculo ajuda, mas parece contar uma historia mais ampla e menos precisa que a ocupacao.

Leitura final da variavel: `workclass` e util, mas entra como apoio, nao como protagonista.

### Por que esse grupo e prioritario

Esse grupo faz ponte direta com capacidade de geracao de renda. Em termos de negocio, ele ajuda a contar uma historia facil de explicar: perfis ocupacionais mais especializados ou em posicoes de maior senioridade concentram mais casos de renda alta.

### Implicacao analitica

`occupation` merece destaque na modelagem e na interpretacao. `workclass` merece entrar, mas com expectativa de sinal complementar. Tambem vale monitorar categorias raras para nao superinterpretar casos pouco frequentes.

## 6. Hipotese 3: Ciclo de Carreira e Intensidade de Trabalho

### Pergunta analitica

Idade e horas trabalhadas por semana ajudam a explicar a classe `>50K`? Se ajudam, a relacao e linear ou muda por faixa?

### Como responder a essa pergunta

Nesse caso, nao basta usar media. O ideal e olhar a comparacao entre classes e tambem dividir a variavel em faixas. Assim fica mais facil enxergar se a taxa positiva sobe, estabiliza ou cai ao longo do eixo da variavel.

### Insight principal

Sim. As duas variaveis ajudam, mas de forma nao linear. Isso significa que nao existe uma regra simples do tipo "quanto maior, melhor" em todos os pontos da distribuicao.

### Resultado por variavel

#### `age`

O padrao de idade e muito claro. Entre `17` e `23` anos, a taxa de `>50K` e quase nula, perto de `0,7%`. A partir da entrada e consolidacao na vida profissional, essa taxa sobe rapidamente. Entre `42` e `55` anos, chega perto de `39%`. Depois cai um pouco nas idades mais altas.

Leitura final da variavel: `age` e importante porque captura maturidade economica e estagio de carreira, mas o efeito nao e reto; ele cresce e depois desacelera.

#### `hours-per-week`

Aqui tambem ha um gradiente. Quem trabalha ate `30` horas por semana tem taxa positiva perto de `6,6%`. Nas faixas centrais, a taxa sobe bastante. Entre `45` e `50` horas, passa de `42%`. Acima disso, o ganho nao cresce indefinidamente; ele parece estabilizar.

Leitura final da variavel: `hours-per-week` ajuda a separar classes, mas seu efeito depende de faixa e provavelmente conversa com ocupacao e estagio de carreira.

### Por que esse grupo e prioritario

Esse grupo e prioritario porque explica a renda sob a lente do tempo e da intensidade. Em outras palavras: nao fala apenas sobre "quem a pessoa e", mas sobre em que fase economica ela parece estar e quanto trabalho ela realiza.

### Implicacao analitica

Essas variaveis sao fortes, mas pedem cuidado na modelagem. Como o efeito nao e linear, pode ser melhor usar modelos que capturem curvas e interacoes naturalmente, ou criar faixas mais interpretaveis.

## 7. Hipotese 4: Estrutura Familiar

### Pergunta analitica

Estado civil e papel no domicilio ajudam a diferenciar grupos de renda?

### Como responder a essa pergunta

Aqui o caminho e o mesmo das categoricas anteriores: comparar taxa positiva por categoria, mas sempre lembrando que essas variaveis nao devem ser lidas como causa direta. Elas funcionam mais como marcadores de contexto social e economico.

### Insight principal

Sim. Esse e um dos grupos mais fortes do estudo. A diferenca entre categorias e muito grande e aparece com alto volume.

### Resultado por variavel

#### `marital-status`

`Married-civ-spouse` aparece com taxa positiva de cerca de `45%`, muito acima da media da base. `Never-married`, por outro lado, fica perto de `4,8%`. As demais categorias ficam em niveis intermediarios, mas ainda bem abaixo do grupo casado civilmente.

Leitura final da variavel: `marital-status` e forte porque separa perfis de forma muito clara e com categorias volumosas.

#### `relationship`

`Wife` e `Husband` concentram as maiores taxas, por volta de `48,6%` e `45,6%`. `Own-child` quase nao concentra classe positiva, ficando perto de `1,6%`. Isso indica que o papel no domicilio conta uma historia economica muito relevante.

Leitura final da variavel: `relationship` tambem e fortissima, mas provavelmente sobrepoe parte da historia ja contada por `marital-status`.

### Por que esse grupo e prioritario

Esse grupo e prioritario porque apresenta uma separacao muito expressiva das classes. Alem disso, ele traz uma discussao analitica importante: duas variaveis podem ser fortes ao mesmo tempo e ainda assim serem parcialmente redundantes.

### Implicacao analitica

O proximo passo nao e decidir imediatamente qual das duas excluir. O mais maduro e registrar que ambas parecem fortes, mas contam historias parecidas. A modelagem deve testar se vale manter as duas ou se uma ja resume bem o sinal.

## 8. Hipotese 5: Eventos Financeiros Raros

### Pergunta analitica

Ganhos e perdas de capital, mesmo raros, ajudam a identificar a classe `>50K`?

### Como responder a essa pergunta

Essas variaveis pedem uma leitura diferente. O primeiro corte relevante nao e o valor exato, mas sim a distincao entre `zero` e `maior que zero`. Isso acontece porque a maior parte da base esta concentrada em zero.

### Insight principal

Sim. `capital-gain` e um dos sinais mais fortes do estudo. `capital-loss` tambem ajuda, mas com menor intensidade.

### Resultado por variavel

#### `capital-gain`

Mais de `91%` da base tem valor zero. Mesmo assim, quando o valor e maior que zero, a taxa positiva salta para cerca de `62,7%`. Quando o valor e zero, ela fica perto de `21,3%`.

Leitura final da variavel: `capital-gain` e rara, mas extremamente informativa.

#### `capital-loss`

O padrao e parecido, embora menos forte. Cerca de `95%` da base tem zero. Quando ha valor positivo, a taxa de `>50K` sobe para `51,3%`. Quando nao ha, ela fica em torno de `23,5%`.

Leitura final da variavel: `capital-loss` tambem carrega sinal importante, mas com menor alcance e menor poder que `capital-gain`.

### Por que esse grupo e prioritario

Esse grupo e prioritario porque mostra um caso classico de variavel rara com alto sinal. Ele lembra que frequencia baixa nao significa pouca utilidade.

### Implicacao analitica

Essas variaveis merecem tratamento proprio. Uma leitura madura e considerar que o modelo talvez aprenda melhor com uma representacao como "tem ou nao tem ganho/perda" do que apenas com o valor bruto.

## 9. Hipotese 6: Variaveis Sensiveis e de Contexto

### Pergunta analitica

Variaveis sensiveis como sexo, raca e pais de origem apresentam sinal? Se apresentarem, esse sinal deve ser usado na decisao?

### Como responder a essa pergunta

O primeiro passo e reconhecer que aqui existem duas perguntas diferentes. A primeira e estatistica: a variavel separa classes? A segunda e de governanca: mesmo separando, ela deveria influenciar a decisao de negocio?

### Insight principal

Sim, essas variaveis mostram diferencas. Mas a existencia de sinal nao significa autorizacao automatica para uso operacional.

### Resultado por variavel

#### `sex`

Ha uma diferenca visivel entre os grupos: a taxa positiva entre homens fica perto de `31,2%`, enquanto entre mulheres fica perto de `11,4%`.

Leitura final da variavel: `sex` carrega sinal, mas o uso exige cautela tecnica e etica.

#### `race`

Alguns grupos aparecem com taxa maior que outros, mas parte dessa leitura depende de volumes diferentes. O ponto importante aqui nao e so o percentual; e o risco de transformar uma diferenca observada em regra de priorizacao.

Leitura final da variavel: `race` pode servir para diagnostico e monitoramento de vies, mais do que como orientadora de acao.

#### `native-country`

Existem categorias com taxa alta, mas varias delas tem pouco volume. Isso fragiliza a interpretacao. Alem disso, a variavel e contextual e sensivel ao mesmo tempo.

Leitura final da variavel: `native-country` nao e boa candidata a protagonista analitica, porque mistura fragmentacao, sensibilidade e risco de superinterpretacao.

### Por que esse grupo nao deve liderar o estudo

Essas variaveis nao devem liderar a narrativa principal porque o custo de uso responsavel e alto. Mesmo quando existe poder preditivo, ele precisa ser equilibrado com interpretabilidade, fairness e risco reputacional.

### Implicacao analitica

A leitura mais madura e manter esse grupo em uma camada de diagnostico. Ele pode ser util para avaliar vies e comportamento do modelo, mas nao deve ser a base principal da explicacao de negocio.

## 10. Variavel de Apoio: `fnlwgt`

### Pergunta analitica

O peso amostral do censo ajuda de forma direta a prever quem esta em `>50K`?

### Como responder a essa pergunta

Antes de olhar qualquer numero, a propria semantica da variavel ja orienta a resposta. `fnlwgt` representa peso estatistico da amostra no levantamento, e nao uma caracteristica economica ou comportamental do individuo.

### Insight principal

Mesmo que possa ter alguma correlacao com o target, ela nao e uma feature intuitiva para liderar explicacao de negocio.

### Leitura final da variavel

`fnlwgt` nao entra como prioridade porque seu significado e amostral, nao substantivo. Em um estudo voltado a interpretacao e decisao, outras variaveis contam historias muito mais claras.

## 11. Ordem Recomendada de Storytelling

Como mentor, minha sugestao e contar a historia nesta sequencia:

1. Comece pela decisao de negocio: quem priorizar no outreach.
2. Mostre a taxa-base da classe positiva para criar referencia.
3. Entre em capital humano: escolaridade costuma ser a historia mais intuitiva.
4. Passe para ocupacao e insercao profissional: isso aprofunda a narrativa da capacidade economica.
5. Depois mostre ciclo de carreira com `age` e `hours-per-week`: aqui voce explica que renda nao depende de um unico fator, mas de fase da vida e intensidade de trabalho.
6. Em seguida, apresente estrutura familiar: esse grupo costuma ter sinal forte e ajuda a enriquecer a historia social e economica do individuo.
7. Depois entre em eventos financeiros raros: esse bloco mostra que variaveis raras podem ser muito informativas.
8. Deixe as variaveis sensiveis para o final: assim voce as trata com maturidade, sem deixar que dominem a narrativa principal.
9. Termine cada bloco com uma frase de transicao para a etapa seguinte: o que isso muda na preparacao ou modelagem.

## 12. Fechamento

O ponto central deste estudo nao e listar variaveis importantes, mas construir uma narrativa analitica coerente. Uma feature vira prioridade quando ela combina significado semantico, separacao observavel do target, volume suficiente para confianca e utilidade pratica para as proximas decisoes do CRISP-DM.

Se a leitura seguir essa ordem, o notebook deixa de parecer uma colecao de funcoes e plots e passa a se comportar como uma historia: primeiro entendemos o negocio, depois entendemos quais mecanismos parecem explicar a renda e, so entao, decidimos como preparar e modelar os dados.
