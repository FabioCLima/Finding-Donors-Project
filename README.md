
# Supervised Learning

## Project: Finding Donors for CharityML

### 1. Introduction

This project applies supervised learning to census data collected from the 1994 U.S. Census to help CharityML, a fictional non-profit, identify individuals most likely to donate. The core task is a binary classification problem: predict whether a person earns more than $50,000 per year. Because high-income individuals are more likely to make large donations, this model helps CharityML prioritize outreach, reduce campaign cost, and improve return on investment.

The dataset originates from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Census+Income). It was donated by Ron Kohavi and Barry Becker after being published in the article _"Scaling Up the Accuracy of Naive-Bayes Classifiers: A Decision-Tree Hybrid"_. The data used here includes small modifications to the original, such as removing the `fnlwgt` feature and records with missing or ill-formatted entries.

---

### 2. Dataset

**Size:** 45,222 records — 34,014 with income `<=50K` (~75%) and 11,208 with income `>50K` (~25%).

The target variable is imbalanced: approximately 75% of individuals earn `<=50K`. This motivated the choice of **F-beta score (β = 0.5)** as the primary evaluation metric, which weights precision more heavily than recall — appropriate when false positives (contacting non-donors) carry an operational cost.

#### 2.1 Features

| Feature | Type | Semantic Group | Meaning |
| --- | --- | --- | --- |
| `age` | Continuous | Demographic | Individual's age in years |
| `sex` | Binary | Demographic | Biological sex (Female / Male) |
| `race` | Categorical | Demographic | Self-identified racial group |
| `native-country` | Categorical | Demographic | Country of origin |
| `workclass` | Categorical | Socioeconomic | Employment sector |
| `occupation` | Categorical | Socioeconomic | Type of work performed |
| `hours-per-week` | Continuous | Socioeconomic | Average hours worked per week |
| `education` | Categorical (ordinal) | Education | Highest level of education attained |
| `education-num` | Continuous | Education | Numeric encoding of education level |
| `marital-status` | Categorical | Family / Social | Current marital status |
| `relationship` | Categorical | Family / Social | Role within the household |
| `capital-gain` | Continuous | Financial | Income from capital asset investments |
| `capital-loss` | Continuous | Financial | Losses from capital asset sales |

---

### 3. Methodology

#### 3.1 Preprocessing

- Log transformation (`np.log1p`) applied to `capital-gain` and `capital-loss` to reduce skewness.
- `MinMaxScaler` applied to all numerical features.
- One-hot encoding via `pd.get_dummies()` on all categorical variables (103 features after encoding).
- Target variable binarized: `<=50K → 0`, `>50K → 1`.
- Train/test split (80/20) with `stratify=income` to preserve class proportions.

| Split | Samples |
| --- | ---: |
| Training set | 36,177 |
| Test set | 9,045 |

#### 3.2 Naive Predictor Baseline

A naive predictor that always predicts `>50K` was used as a lower bound reference:

| Metric | Value |
| --- | ---: |
| Accuracy | 0.2478 |
| F-score (β=0.5) | 0.2917 |

#### 3.3 Model Comparison

Three supervised learning algorithms were evaluated at 1%, 10%, and 100% of the training data:

| Model | Strengths |
| --- | --- |
| `LogisticRegression` | Fast, interpretable baseline; good for linearly separable features |
| `RandomForestClassifier` | Robust to non-linear patterns; provides feature importance estimates |
| `GradientBoostingClassifier` | High performance on tabular data; sequential error correction |

**`GradientBoostingClassifier`** was selected as the final model based on its highest F-score (β=0.5) at 100% training data with acceptable training time.

#### 3.4 Hyperparameter Tuning

`GridSearchCV` with `StratifiedKFold (cv=5)` and `make_scorer(fbeta_score, beta=0.5)` was used to tune:

- `n_estimators`
- `learning_rate`
- `max_depth`

#### 3.5 Final Results

|     Metric     | Naive Predictor | Unoptimized Model | Optimized Model |
| :------------: | :-------------: | :---------------: | :-------------: |
| Accuracy       | 0.2478          | 0.8639            | **0.8719**      |
| F-score (β=0.5)| 0.2917          | 0.7461            | **0.7581**      |

The optimized model improved both accuracy (+0.008) and F-score (+0.012) over the unoptimized model, and vastly outperformed the naive baseline.

#### 3.6 Feature Importance and Reduction

Feature importances were extracted using `RandomForestClassifier`. Top 5 features:

1. `age`
2. `hours-per-week`
3. `capital-gain`
4. `marital-status__Married-civ-spouse`
5. `education-num`

A reduced model trained on only these 5 features achieved accuracy of **0.8526** and F-score of **0.7172** — a performance drop that confirms the remaining features still carry useful signal.

---

### 4. Project Structure

```text
Finding_Donors_Project/
├── configs/
│   └── base.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── figs/
├── models/
├── notebooks/
│   ├── finding_donors.ipynb
│   └── finding_donors_crispdm.ipynb
├── reports/
│   ├── experiments/
│   └── metrics/
├── scripts/
│   ├── run_pipeline.py
│   └── run_train.py
├── src/
│   └── finding_donors/
│       ├── core/
│       ├── data/
│       ├── features/
│       ├── models/
│       ├── evaluation/
│       └── pipeline.py
├── tests/
├── docs/
│   └── Analyze_Finding_Donors_from_Udacity.md
└── README.md
```

---

### 5. Dependencies

- Python 3.x
- `numpy`, `pandas`, `scipy`
- `scikit-learn`, `joblib`
- `matplotlib`, `seaborn`
- `loguru` (structured logging)
- `pydantic`, `pydantic-settings` (typed config and validation)
- `pyyaml` (external config files)

---

### 6. Run the Refactored Pipeline

```bash
uv sync
uv run python scripts/run_train.py
```

Optional:

```bash
uv run python scripts/run_train.py --config configs/base.yaml --log-level DEBUG
```

---

### 7. References

1. Kohavi, R. (1996). Scaling Up the Accuracy of Naive-Bayes Classifiers: A Decision-Tree Hybrid. _Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD-96)_.
2. Hosmer, D. W., & Lemeshow, S. (2000). _Applied Logistic Regression_ (2nd ed.). Wiley-Interscience.
3. Breiman, L. (2001). Random Forests. _Machine Learning_, 45(1), 5–32. [https://doi.org/10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
4. Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. _Annals of Statistics_, 29(5), 1189–1232. [https://doi.org/10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451)
5. UCI Machine Learning Repository — Census Income dataset: [https://archive.ics.uci.edu/ml/datasets/Census+Income](https://archive.ics.uci.edu/ml/datasets/Census+Income)
