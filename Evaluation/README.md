# 📈 Evaluation of IR Ranking Outputs

This module evaluates the effectiveness of ranking models (e.g., BM25, QL, SDM) using standard Information Retrieval metrics. It compares system outputs (`.trecrun` files) against relevance judgments (`qrels`) to compute scores such as NDCG, MRR, MAP, Precision, Recall, and F1.

---

## 🧠 What It Does

- Reads `.trecrun` files (ranking outputs) and corresponding `qrels` (ground truth)
- Computes standard IR evaluation metrics:
  - **NDCG@75**
  - **Reciprocal Rank (RR)**
  - **Precision@15**
  - **Recall@20**
  - **F1@25**
  - **Average Precision (AP)**
  - **Mean Average Precision (MAP)**

---

## 📁 Key Files

- `src/eval.py` — Main script with all logic
- `bm25.trecrun`, `ql.trecrun`, `sdm.trecrun` — System output files to evaluate
- `qrels` — File containing relevance judgments
- `bm25.eval`, `ql.eval`, `sdm.eval` — Output evaluation result files

---

## 🚀 How to Run

Use default arguments:

```bash
python3 src/eval.py
```

Or with custom files:

```bash
python3 src/eval.py runfile.trecrun qrels outputFile.eval
```

Example:

```bash
python3 src/eval.py bm25.trecrun qrels bm25.eval
```

---

## 🧪 Metrics Implemented

| Metric      | Description                                      |
|-------------|--------------------------------------------------|
| **NDCG@75** | Normalized Discounted Cumulative Gain           |
| **RR**      | Reciprocal Rank of first relevant result        |
| **P@15**    | Precision at rank 15                            |
| **R@20**    | Recall at rank 20                               |
| **F1@25**   | Harmonic mean of P and R at rank 25             |
| **AP**      | Average Precision                               |
| **MAP**     | Mean of average precision across all queries    |

---

## 📚 Libraries Used

- None — implemented fully in pure Python.

