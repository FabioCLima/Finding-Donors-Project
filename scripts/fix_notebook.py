"""
Transformation script for finding_donors_crispdm.ipynb

Applies all structural improvements from the technical review:
- Phase A: Business Understanding fixes
- Phase B: Data Understanding structural fixes
- Phase C: New content additions

Operations: Deletions (high→low) → Updates → Insertions (low→high)
"""

import json
import copy
from pathlib import Path

NOTEBOOK_PATH = Path("notebooks/finding_donors_crispdm.ipynb")


def make_markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": "inserted-cell",
        "metadata": {},
        "source": source,
    }


def make_code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "inserted-cell",
        "metadata": {},
        "outputs": [],
        "source": source,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Load
# ──────────────────────────────────────────────────────────────────────────────
with open(NOTEBOOK_PATH) as f:
    nb = json.load(f)

cells = nb["cells"]
print(f"Loaded notebook: {len(cells)} cells")

# Save original Cell[4] content before deletions (Confusion Matrix)
confusion_matrix_source = "".join(cells[4]["source"])

# ──────────────────────────────────────────────────────────────────────────────
# PHASE 1 — DELETIONS (highest index first to avoid shifting)
# ──────────────────────────────────────────────────────────────────────────────
delete_indices = sorted([83, 61, 49, 30, 29, 21, 19, 18, 9, 4, 1], reverse=True)

for idx in delete_indices:
    preview = "".join(cells[idx]["source"])[:60].replace("\n", " ")
    print(f"  Del[{idx}]: {preview!r}")
    del cells[idx]

print(f"\nAfter deletions: {len(cells)} cells (expected 91)")

# ──────────────────────────────────────────────────────────────────────────────
# PHASE 2 — UPDATES (post-deletion indices)
# ──────────────────────────────────────────────────────────────────────────────

# U1 — new[2] (was Cell[3]): append premissas blockquote at end
premissas_block = (
    "\n\n---\n\n"
    "> **Premissas do projeto:**\n"
    "> - Classificação binária supervisionada.\n"
    "> - Alvo: prever se uma pessoa possui renda `>50K`.\n"
    "> - Uso pretendido: priorização de contatos da CharityML.\n"
    "> - Métrica principal: `F0.5` — privilegia precisão sobre recall, pois falsos\n"
    ">   positivos representam contatos enviados sem retorno esperado."
)
cells[2]["source"] = "".join(cells[2]["source"]) + premissas_block
print(f"  U1 done: appended premissas to new[2]")

# U2 — new[3] (was Cell[5]): add "## 1.3" to dictionary header
cells[3]["source"] = "".join(cells[3]["source"]).replace(
    "## Dicionário e Classificação Semântica das Variáveis",
    "## 1.3 Dicionário e Classificação Semântica das Variáveis",
)
print(f"  U2 done: added '1.3' to dictionary header")

# U3 — new[5] (was Cell[7]): remove generic template intro, add "Regra final" at end
src7 = "".join(cells[5]["source"])

# Remove the generic template intro block (between header and first hypothesis)
generic_intro = (
    "\nAs hipóteses abaixo foram definidas para guiar a análise e evitar EDA genérica."
    '\n\n"Acredito que a *variável ou grupo de variáveis* tenha uma relação com o alvo, porque *racional de negócio*. Vou investigar isso *comparando evidências ou cortes analíticos*."\n'
    '\nExemplo:\n"Acredito que clientes com maior tempo de relacionamento tenham maior chance de renovação, porque relações mais longas indicam maior fidelização. Vou investigar isso comparando a taxa de renovação por faixa de tempo de casa."\n'
)
src7 = src7.replace(generic_intro, "\n")

# Add "Regra final" at the end
regra_final = (
    "\n\n---\n\n"
    "### Regra final para levar para qualquer projeto\n\n"
    "> **Hipótese boa conecta negócio, mecanismo plausível, dado disponível e decisão analítica.**\n\n"
    "Quando essa conexão aparece, a exploração deixa de ser barulho e passa a produzir direção."
)
cells[5]["source"] = src7 + regra_final
print(f"  U3 done: cleaned Cell[7] template intro, added regra final")

# U4 — new[12] (was Cell[15]): full replacement of setup cell
setup_cell_code = (
    "# 2.2 Leitura do target e baseline operacional\n\n"
    "target_col = \"income\"\n"
    "positive_label = \">50K\"\n\n"
    "# Criação da variável alvo binária (definida UMA VEZ aqui para todo o notebook)\n"
    "# 1 = renda >50K (classe positiva / potencial doador)\n"
    "# 0 = renda <=50K (classe negativa)\n"
    "df[\"target\"] = (df[target_col].str.strip() == positive_label).astype(int)\n\n"
    "target_summary = (\n"
    "    df[target_col].value_counts().rename_axis(\"classe\").reset_index(name=\"qtd\")\n"
    ")\n"
    "target_summary[\"percentual\"] = target_summary[\"qtd\"] / target_summary[\"qtd\"].sum()\n"
    "display(target_summary)\n\n"
    "# Baseline: taxa da classe positiva na base completa\n"
    "# Constante única para todas as comparações de H1–H6\n"
    "baseline = df[\"target\"].mean()\n"
    "print(f\"Taxa da classe positiva (baseline): {baseline:.2%}\")\n"
    "print()\n"
    "print(f\"Implicação para Data Preparation: base moderadamente desbalanceada ({baseline:.1%})\")\n"
    "print(f\"→ Usar stratify=y no train_test_split para preservar proporção nas partições.\")"
)
cells[12]["source"] = setup_cell_code
print(f"  U4 done: replaced setup cell with df['target'] + baseline")

# U5 — new[22] (was Cell[28]): update H2 steps list
new_h2_steps = (
    "1. agrupar por `occupation` → taxa positiva + suporte\n"
    "2. ordenar por taxa positiva decrescente\n"
    "3. visualizar com linha de base e suporte anotado\n"
    "4. identificar padrão e documentar conclusão\n\n"
    "> A baseline operacional está definida na seção 2.2 e disponível como `baseline`."
)
cells[22]["source"] = new_h2_steps
print(f"  U5 done: updated H2 steps list")

# U6 — new[40] (was Cell[48]): remove "1. Confirmar baseline" from H3 steps
src48 = "".join(cells[40]["source"])
old_steps = (
    "1. Confirmar a baseline\n"
    "2. Dividir cada variável em faixas (bins de largura fixa (como no código abaixo))\n"
    "3. Calcular a taxa da classe positiva por faixa\n"
    "4. Plotar: eixo X = faixas, eixo Y = taxa positiva, linha de baseline como referência\n"
    "5. Documentar se o padrão é linear, não linear, ou sem sinal"
)
new_steps = (
    "1. Dividir cada variável em faixas (bins de largura fixa)\n"
    "2. Calcular a taxa da classe positiva por faixa\n"
    "3. Plotar: eixo X = faixas, eixo Y = taxa positiva, linha de baseline como referência\n"
    "4. Documentar se o padrão é linear, não linear, ou sem sinal\n\n"
    "> A baseline operacional está definida na seção 2.2 e disponível como `baseline`."
)
cells[40]["source"] = src48.replace(old_steps, new_steps)
print(f"  U6 done: updated H3 steps (removed baseline step, renumbered)")

# U7 — new[41] (was Cell[50]): rename "Passo 2" → "Passo 1"
cells[41]["source"] = "".join(cells[41]["source"]).replace(
    "**Passo 2 — Tabela de taxa positiva por faixa de `age`**",
    "**Passo 1 — Tabela de taxa positiva por faixa de `age`**",
)
print(f"  U7 done: renamed 'Passo 2' → 'Passo 1' in H3")

# U8 — new[64] (was Cell[74]): remove baseline lines, keep zeros check
h5_zeros_code = (
    "# Passo 1 — Verificar esparsidade de capital-gain e capital-loss\n"
    "# A baseline operacional está disponível como `baseline` (seção 2.2)\n\n"
    "for col in [\"capital-gain\", \"capital-loss\"]:\n"
    "    zeros = (df[col] == 0).mean()\n"
    "    print(\n"
    "        f\"{col}: {zeros:.1%} dos registros são zero  |  {1 - zeros:.1%} têm valor > 0\"\n"
    "    )"
)
cells[64]["source"] = h5_zeros_code
print(f"  U8 done: cleaned H5 cell (removed baseline lines)")

# U9 — new[84] (was Cell[95]): insert critical findings section
src95 = "".join(cells[84]["source"])

achados_section = """
## Achados Críticos e Respostas a Dúvidas Técnicas

### Desequilíbrio do target
A classe positiva representa **24,8%** (11.208 de 45.222 registros). Moderadamente
desbalanceada. Decisões obrigatórias:
- `stratify=y` no `train_test_split` para preservar proporção nas partições.
- Avaliar com `F0.5`, precisão e recall — nunca apenas acurácia.
- Baseline ingênua (prever sempre ≤50K): acerta ~75,2%, mas com 0% de recall na classe positiva.

### Redundância confirmada: education_level × education-num
As duas variáveis são **bijetivas** (correspondência 1:1 comprovada em H1). Incluir ambas
duplica sinal sem adicionar informação.
**Decisão recomendada:** usar `education_level` (one-hot, interpretável) OU `education-num`
(ordinal, compacto). Nunca as duas simultaneamente.

### Complementaridade: marital-status × relationship (H4)
O cruzamento confirmou **sobreposição parcial, não redundância total**. Existem combinações
com granularidade adicional além de `marital-status` isolado.
**Decisão recomendada:** incluir ambas e eliminar uma via experimento controlado
(comparar ganho incremental no F0.5 de validação).

### Esparsidade de capital-gain e capital-loss (H5)
- `capital-gain`: 91% zeros; quando > 0, taxa positiva sobe ~3x (lift mais alto do estudo).
- `capital-loss`: 95% zeros; quando > 0, taxa sobe ~2x.
**Tratamento recomendado:** criar indicador binário (`flag = 1 se > 0`) + manter valor bruto.
Aplicar `np.log1p` ao valor bruto para modelos sensíveis a escala.

### Não-linearidade de age e hours-per-week (H3)
Padrões não monotônicos confirmados: `age` com pico em meia-carreira (~42–55 anos);
`hours-per-week` com salto expressivo na faixa 40–50h.
**Implicação:** modelos baseados em árvore (Random Forest, Gradient Boosting) capturam
esse padrão naturalmente. Modelos lineares exigem discretização ou termos polinomiais.

### Variáveis sensíveis: sex, race, native-country (H6)
Diferenças estatísticas presentes, mas reflexo de desigualdades estruturais históricas (1994).
**Uso recomendado:** apenas para diagnóstico de viés pós-treinamento (disparate impact,
equalized odds). Não devem ser features de entrada do modelo produtivo.

### Categorias esparsas: native-country
Muitas categorias com n < 50 (taxas positivas instáveis estatisticamente).
**Tratamento recomendado:** agrupar categorias com suporte < 50 como `"Other"` antes
do encoding.

"""

# Insert before "## Próximos Passos"
proximos_marker = "## Próximos Passos Recomendados"
if proximos_marker in src95:
    src95 = src95.replace(proximos_marker, achados_section + proximos_marker)
    # Also update item 2 in Próximos Passos
    src95 = src95.replace(
        "Tratar não linearidades e assimetrias: faixas para `age`/`hours-per-week`, flags e/ou log para `capital-gain` e `capital-loss`.",
        "Tratar não linearidades e assimetrias: (a) binning para `age` e `hours-per-week`; (b) flag binário + `np.log1p` para `capital-gain` e `capital-loss`.",
    )
    cells[84]["source"] = src95
    print(f"  U9 done: inserted 7 critical findings into Cell[95] conclusions")
else:
    print(f"  U9 WARNING: marker '{proximos_marker}' not found in Cell[95]")

# ──────────────────────────────────────────────────────────────────────────────
# PHASE 3 — INSERTIONS (lowest index first)
# ──────────────────────────────────────────────────────────────────────────────

# I1 — Insert Confusion Matrix at position 5 (after new[4]=criteria, before new[5]=hypotheses)
confusion_matrix_cell = make_markdown_cell(confusion_matrix_source)
cells.insert(5, confusion_matrix_cell)
print(f"\n  I1 done: inserted Confusion Matrix at position 5 ({len(cells)} cells)")

# I2 — Insert helper functions intro at position 49
# (H2 conclusions are around new[47] after I1 shift; +1 = 48; insert at 49)
# Let's verify by finding H2 conclusions cell
h2_conclusions_idx = None
for i, cell in enumerate(cells):
    src = "".join(cell["source"])
    if "### Conclusões da análise da hipótese H2:" in src:
        h2_conclusions_idx = i
        break

if h2_conclusions_idx is not None:
    insert_pos_i2 = h2_conclusions_idx + 1
    print(f"  Found H2 conclusions at index {h2_conclusions_idx}, inserting helper intro at {insert_pos_i2}")
else:
    insert_pos_i2 = 49
    print(f"  H2 conclusions not found, using fallback position {insert_pos_i2}")

helper_intro_source = (
    "## 2.3 Refatoração: Funções Auxiliares para Análise por Hipóteses\n\n"
    "As hipóteses H1 e H2 foram implementadas com código **inline** para tornar explícito\n"
    "o padrão: calcular suporte por categoria → taxa positiva → comparar com baseline.\n\n"
    "Com o padrão estabelecido, aplicamos o princípio **DRY** (*Don't Repeat Yourself*):\n"
    "extraímos o que é repetido como função reutilizável.\n\n"
    "> **Por que refatorar aqui e não no início?**  \n"
    "> Mostrar o código inline primeiro torna explícito o que as funções fazem internamente.\n"
    "> Refatorar após H1–H2 evita boilerplate desnecessário em H3–H6 sem sacrificar\n"
    "> transparência pedagógica."
)
cells.insert(insert_pos_i2, make_markdown_cell(helper_intro_source))
print(f"  I2 done: inserted helper functions intro at {insert_pos_i2} ({len(cells)} cells)")

# I3 — Insert helper function code immediately after I2
helper_code_source = (
    "def calcular_taxa_positiva_por_categoria(df, coluna, baseline, min_support=30):\n"
    "    \"\"\"Calcula taxa de renda >50K por categoria com suporte mínimo filtrado.\n\n"
    "    Parameters\n"
    "    ----------\n"
    "    df : pd.DataFrame\n"
    "    coluna : str  — variável categórica a analisar\n"
    "    baseline : float  — taxa marginal da classe positiva\n"
    "    min_support : int  — mínimo de registros por categoria\n\n"
    "    Returns\n"
    "    -------\n"
    "    pd.DataFrame com support, positive_rate e flag above_baseline,\n"
    "    ordenado por positive_rate decrescente.\n"
    "    \"\"\"\n"
    "    return (\n"
    "        df.groupby(coluna)[\"target\"]\n"
    "        .agg(support=\"count\", positive_rate=\"mean\")\n"
    "        .query(f\"support >= {min_support}\")\n"
    "        .assign(above_baseline=lambda x: x[\"positive_rate\"] > baseline)\n"
    "        .sort_values(\"positive_rate\", ascending=False)\n"
    "    )\n\n\n"
    "# Verificação — replicar H1 e H2 via função (deve coincidir com resultados inline)\n"
    "print(\"H1 — education_level (verificação via função):\")\n"
    "print(calcular_taxa_positiva_por_categoria(df, \"education_level\", baseline).to_string())\n"
    "print()\n"
    "print(\"H2 — occupation (verificação via função):\")\n"
    "print(calcular_taxa_positiva_por_categoria(df, \"occupation\", baseline).to_string())"
)
cells.insert(insert_pos_i2 + 1, make_code_cell(helper_code_source))
print(f"  I3 done: inserted helper function code at {insert_pos_i2 + 1} ({len(cells)} cells)")

# I4 — Insert variables decision table after amplitude table
# Find the amplitude table cell (Cell[94] which became ~Cell[84] after deletions, now shifted by I1+I2+I3)
amplitude_idx = None
for i, cell in enumerate(cells):
    src = "".join(cell["source"])
    if "## Comparativo Final de Força Discriminativa" in src:
        amplitude_idx = i
        break

# The code cell with amplitude calculation is right after the markdown
if amplitude_idx is not None:
    # Find the next code cell after the amplitude header
    for j in range(amplitude_idx + 1, len(cells)):
        if cells[j]["cell_type"] == "code":
            insert_pos_i4 = j + 1
            break
    else:
        insert_pos_i4 = amplitude_idx + 2
    print(f"  Found amplitude section at index {amplitude_idx}, inserting decision table at {insert_pos_i4}")
else:
    insert_pos_i4 = len(cells) - 7  # fallback: near end before templates
    print(f"  Amplitude section not found, using fallback position {insert_pos_i4}")

decision_table_source = (
    "## 2.5 Tabela de Decisões sobre Variáveis\n\n"
    "Esta tabela conecta os achados da EDA às decisões de preparação e modelagem.\n"
    "Cada variável recebe uma recomendação de tratamento derivada das análises de H1–H6.\n\n"
    "| Variável | Padrão observado | Risco / atenção | Decisão recomendada |\n"
    "|---|---|---|---|\n"
    "| `education_level` | Gradiente forte; taxa cresce com nível educacional | Redundante com `education-num` | Manter UM dos dois; nunca ambos simultaneamente |\n"
    "| `education-num` | Mesma informação que `education_level`, versão ordinal | Duplica sinal — mapeamento 1:1 confirmado | Alternativa compacta para modelos que se beneficiam de ordinalidade |\n"
    "| `occupation` | Alta amplitude (~45pp); exec/prof muito acima da baseline | Categorias raras (n < 30) | Agrupar categorias raras antes do encoding |\n"
    "| `workclass` | Setor e autonomia com diferencial relevante | Volume baixo em algumas categorias | Verificar estabilidade em conjunto com `occupation` |\n"
    "| `age` | Não linear; pico em meia-carreira (~42–55 anos) | Padrão se perde em modelos lineares simples | Árvores capturam diretamente; linear exige binning ou termos polinomiais |\n"
    "| `hours-per-week` | Salto expressivo na faixa 40–50h; efeito de intensidade | Sensível a outliers; interação com ocupação | Útil em modelos flexíveis; para linear, considerar discretização |\n"
    "| `marital-status` | `Married-civ-spouse` muito acima da baseline (~42%) | Sobreposição parcial com `relationship` | Manter ambas; eliminar uma via experimento controlado |\n"
    "| `relationship` | `Husband` e `Wife` concentram >50K | Sobreposição semântica com `marital-status` | Manter; avaliar ganho incremental no F0.5 de validação |\n"
    "| `capital-gain` | Lift ~3x quando > 0; 91% zeros | Esparsidade extrema; cauda longa | FLAG binário + valor bruto + `np.log1p` para modelos de escala |\n"
    "| `capital-loss` | Lift ~2x quando > 0; 95% zeros | Distribuição altamente assimétrica | Mesma lógica de `capital-gain` |\n"
    "| `sex` | Diferença de taxa entre grupos visível | Risco ético e reputacional | Apenas diagnóstico de viés pós-treinamento; não usar como feature |\n"
    "| `race` | Diferenças presentes; suportes muito desiguais | Risco de viés e superinterpretação | Apenas diagnóstico de viés |\n"
    "| `native-country` | Muitas categorias com n < 50 (taxas instáveis) | Alta instabilidade estatística | Agrupar n < 50 como `\"Other\"`; usar apenas em diagnóstico |"
)
cells.insert(insert_pos_i4, make_markdown_cell(decision_table_source))
print(f"  I4 done: inserted decision table at {insert_pos_i4} ({len(cells)} cells)")

# ──────────────────────────────────────────────────────────────────────────────
# PHASE 4 — Assign stable IDs to inserted cells
# ──────────────────────────────────────────────────────────────────────────────
import uuid
for i, cell in enumerate(cells):
    if cell.get("id") == "inserted-cell":
        cell["id"] = str(uuid.uuid4())[:8]

# ──────────────────────────────────────────────────────────────────────────────
# Save
# ──────────────────────────────────────────────────────────────────────────────
nb["cells"] = cells
with open(NOTEBOOK_PATH, "w") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\n✓ Notebook saved: {len(cells)} cells (expected 95)")
print("  Done!")
