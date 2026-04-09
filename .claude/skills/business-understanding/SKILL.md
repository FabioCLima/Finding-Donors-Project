---
name: business-understanding
description: Create only the Business Understanding phase of a CRISP-DM project in a professional, decision-oriented, and concise way
---

# Phase 1 skill: Business Understanding

First of all read the dataset in the following path: `/home/fabiolima/Desktop/Finding_Donors_Project/data/census.csv`

Use this skill when the agent is responsible only for `Phase 1 - Business Understanding`.

The agent must not jump into modeling, feature engineering, or exploratory analysis before the business problem is clearly framed.

The purpose of this phase is to translate a vague project idea into a precise analytical problem that the next phases can execute.

## Core mission

The Business Understanding agent must answer:

1. What business problem are we solving?
2. What decision will this analysis or model support?
3. Why does this matter to the organization?
4. How should the ML problem be framed?
5. What defines success from business and analytical perspectives?
6. Which initial hypotheses should guide Data Understanding?

## Required inputs

Before writing the phase, gather the minimum context available from:

- `README.md`

If information is missing, do not invent detailed facts. State assumptions explicitly and keep the framing conservative.

## Workflow

Follow these steps in order.

### Step 1. Read and extract the business context

Identify:

- organization or project name
- domain
- business objective
- operational pain point
- current decision that needs support
- why the problem matters now

Output of this step:

- 1 short paragraph explaining the business situation in plain language

### Step 2. Define the business decision

Write the exact decision the project is meant to improve.

Examples:

- who should be prioritized for outreach
- which customers are at risk of churn
- which transactions should be escalated for review

This section must make clear:

- what action will be taken after the model output
- who uses the output
- what resource is being optimized

Output of this step:

- 1 decision statement in the form:
  `The project supports the decision of [action] for [population] in order to [business benefit].`

### Step 3. Frame the problem as an ML task

Translate the business problem into an analytical problem.

Define explicitly:

- prediction target
- unit of analysis
- type of ML problem
- positive class
- prediction use case
- main tradeoff between false positives and false negatives

Use language such as:

- `This is a supervised binary classification problem.`
- `The unit of analysis is one individual record.`
- `The positive class is ...`

If the target is a proxy, say so clearly.

Example:

`Income >50K is not donation behavior itself. It is a proxy for higher donation potential.`

Output of this step:

- 1 short paragraph called `Framing the ML Problem`

### Step 4. Clarify assumptions, risks, and constraints

Document what may limit the project.

Typical items:

- proxy target limitations
- historical bias
- fairness concerns
- data availability
- class imbalance
- operational budget limits
- interpretability expectations

Do not turn this into a long ethics essay. Keep only what affects project design or decision quality.

Output of this step:

- 3 to 6 bullets under `Assumptions, Risks, and Constraints`

### Step 5. Define success criteria

Success criteria must exist at three levels.

#### 5.1 Business success criteria

Examples:

- reduce wasted outreach
- improve prioritization quality
- increase campaign efficiency

#### 5.2 ML success criteria

Define the metric according to the business tradeoff.

Examples:

- `Precision` if false positives are expensive
- `Recall` if missed positives are expensive
- `F-beta` when balancing both with business-weighted emphasis

The agent must explain why the chosen metric matches the decision context.

#### 5.3 Project success criteria

Examples:

- reproducible workflow
- interpretable reasoning
- clear handoff to Data Understanding
- documented assumptions

Output of this step:

- 3 short subsections:
  - `Business Success Criteria`
  - `ML Success Criteria`
  - `Project Success Criteria`

### Step 6. Form initial business-driven hypotheses

Create hypotheses before Data Understanding starts.

Each hypothesis must:

- be connected to the business objective
- mention a plausible driver
- point to one or more variables
- be testable with available data

Use this structure:

`I believe [variable or variable group] is related to [target] because [business rationale]. This will be investigated by [comparison or analysis].`

Good hypothesis example:

`I believe education level is positively related to income >50K because higher education often improves access to higher-paying occupations. This will be investigated by comparing the positive-class rate across education levels.`

Bad hypothesis examples:

- `I will plot age.`
- `I will analyze the categorical variables.`
- `occupation seems important.`

Output of this step:

- 3 to 6 initial hypotheses
- mermaid flowchart as mind map, explain how the hypotheses are related to each other

### Step 7. Prepare the handoff to Data Understanding

End the phase by stating what Data Understanding must validate next.

The handoff should answer:

- which variables deserve early inspection
- which hypotheses should be tested first
- which data quality issues need confirmation
- which risks should be monitored

Output of this step:

- 1 short section called `Implications for Data Understanding`

## Final deliverable structure

The Business Understanding agent should produce the phase in this order:

1. `Business Context`
2. `Business Objective`
3. `Decision to Support`
4. `Framing the ML Problem`
5. `Assumptions, Risks, and Constraints`
6. `Success Criteria`
7. `Initial Hypotheses`
8. `Implications for Data Understanding`

## Writing standard

The output must be:

- professional
- concise
- decision-oriented
- explicit about assumptions
- free of generic filler

Avoid:

- long introductions
- textbook definitions without project relevance
- jumping into EDA findings
- choosing metrics without business justification
- writing hypotheses that are only chart requests

## Quality checklist

Before finishing, verify:

- the business problem is specific
- the decision is operational, not abstract
- the ML framing is explicit
- the success criteria match the business tradeoff
- hypotheses are testable and business-linked
- the phase creates a clear bridge into Data Understanding

## Output style

Use short sections and direct language.

Prefer:

- one sharp paragraph per section
- small bullet lists only where needed
- concrete statements over general commentary

## Minimal template

```md
## 1. Business Understanding

### Business Context
[Explain the business situation, operational pain point, and why the problem matters.]

### Business Objective
[State the business objective clearly.]

### Decision to Support
[State the operational decision this project will improve.]

### Framing the ML Problem
[Define target, unit of analysis, ML task, positive class, and proxy limitations.]

### Assumptions, Risks, and Constraints
- [...]
- [...]
- [...]

### Success Criteria

#### Business Success Criteria
- [...]

#### ML Success Criteria
- [...]

#### Project Success Criteria
- [...]

### Initial Hypotheses
1. [...]
2. [...]
3. [...]

### Implications for Data Understanding
[Explain what must be validated next in the data.]

### Final deliverable
- markdown file at /home/fabiolima/Desktop/Finding_Donors_Project/notebooks/01_Business_Understanding.md
- obsidian note in the following folder: /home/fabiolima/Desktop/Study_DS/MLOPs/Projetos/Finding Donors - ML
```
