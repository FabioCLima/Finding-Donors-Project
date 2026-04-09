---
title: Hypothesis Map — Business Understanding
project: Finding Donors for CharityML
generated: 2026-04-08
phase: CRISP-DM Phase 1 — Business Understanding
---

# Hypothesis Map — Finding Donors for CharityML

> Mapa visual das hipóteses iniciais levantadas antes de qualquer análise de dados,
> seguindo a disciplina CRISP-DM de separar o raciocínio a priori dos achados empíricos.

## Mapa Mental das Hipóteses

```mermaid
graph TD
    classDef problemNode fill:#2d6a4f,color:#fff,stroke:#1b4332,rx:8
    classDef hypothesisNode fill:#1d3557,color:#fff,stroke:#457b9d,rx:6
    classDef contrarianNode fill:#6d2b3d,color:#fff,stroke:#c9184a,stroke-dasharray:6 3,rx:6
    classDef testNode fill:#f4a261,color:#000,stroke:#e76f51,rx:4
    classDef confirmedNode fill:#2a9d8f,color:#fff,stroke:#264653,rx:6
    classDef refutedNode fill:#e63946,color:#fff,stroke:#c1121f,rx:6

    PROBLEM["🎯 CharityML — Donor Targeting\nPredict individuals with income > 50K\nTarget: income (binary: <=50K / >50K)"]:::problemNode

    H1["H1 — Education Level\neducation / education-num → Higher ed = higher income\nStatus: Pendente"]:::hypothesisNode
    H2["H2 — Occupation Type\noccupation → Exec/Prof roles = higher income\nStatus: Pendente"]:::hypothesisNode
    H3["H3 — Capital Assets\ncapital-gain / capital-loss → Wealth signal\nStatus: Pendente"]:::hypothesisNode
    H4["⚡ H4 — Hours Worked\nhours-per-week → More hours = higher income\nStatus: Pendente"]:::contrarianNode
    H5["H5 — Age / Career Stage\nage → Mid-career peak 35-55\nStatus: Pendente"]:::hypothesisNode
    H6["H6 — Marital and Household Role\nmarital-status / relationship → Household head = higher income\nStatus: Pendente"]:::hypothesisNode

    TEST_H1["🔬 Positive-class rate\nacross education levels"]:::testNode
    TEST_H2["🔬 Rank occupation categories\nby positive-class rate"]:::testNode
    TEST_H3["🔬 Distribution comparison\ncapital features by income class"]:::testNode
    TEST_H4["🔬 Mean hours-per-week\nacross income classes"]:::testNode
    TEST_H5["🔬 Positive-class rate\nacross age bins"]:::testNode
    TEST_H6["🔬 Positive-class rate\nacross marital-status and relationship"]:::testNode

    PROBLEM --> H1
    PROBLEM --> H2
    PROBLEM --> H3
    PROBLEM --> H4
    PROBLEM --> H5
    PROBLEM --> H6

    H1 --> TEST_H1
    H2 --> TEST_H2
    H3 --> TEST_H3
    H4 --> TEST_H4
    H5 --> TEST_H5
    H6 --> TEST_H6
```

## Hipóteses — Referência Rápida

| # | Nome Curto | Variável | Direção Esperada | Método de Teste | Status |
|---|---|---|---|---|---|
| H1 | Education Level | `education` / `education-num` | Higher education → higher P(income >50K) | Positive-class rate across education levels | Pendente |
| H2 | Occupation Type | `occupation` | Exec/Prof/Specialty roles → higher income | Rank occupation categories by positive-class rate | Pendente |
| H3 | Capital Assets | `capital-gain` / `capital-loss` | Non-zero capital activity → higher income | Distribution comparison by income class | Pendente |
| H4 ⚡ | Hours Worked | `hours-per-week` | More hours → higher income (may not hold for salaried) | Mean hours-per-week across income classes | Pendente |
| H5 | Age / Career Stage | `age` | Mid-career (35–55) → peak income probability | Positive-class rate across age bins | Pendente |
| H6 | Marital & Household Role | `marital-status` / `relationship` | Married household head → higher income | Positive-class rate across marital-status and relationship | Pendente |

## Legenda

| Cor do nó | Significado |
|---|---|
| Verde escuro | Problem Statement |
| Azul escuro | Hipótese pendente |
| Vermelho bordô (tracejado) | Hipótese contrarian |
| Verde água | Hipótese confirmada |
| Vermelho | Hipótese refutada |
| Laranja | Método de teste |

---

*Gerado pelo skill `/hypothesis-map` — atualizar manualmente o Status conforme os achados da análise avançam.*
