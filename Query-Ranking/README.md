# 📊 Query Ranking with BM25 and Query Likelihood (QL)

This module implements document ranking for text queries using two classic Information Retrieval models: **BM25** and **Query Likelihood (QL)**. The system ranks either scenes or plays from a Shakespeare corpus using an inverted index built per document.

---

## 🧠 What It Does

- Builds an inverted index from the input corpus (`.json.gz`)
- Reads structured queries from a `.tsv` file
- Supports two ranking methods:
  - **BM25** — Uses term frequency, document length, and inverse document frequency
  - **Query Likelihood (QL)** — Language model-based scoring with Dirichlet smoothing (μ = 300)
- Ranks documents per query and outputs results in a TREC-style format

---

## 📂 Key Files

- `src/query.py` — Main script with all logic
- `shakespeare-scenes.json.gz` — Input corpus
- `trainQueries.tsv` — Queries to rank
- `train.results` — Output ranked list for each query

---

## 🚀 How to Run

```bash
python3 src/query.py
```

Or with custom files:

```bash
python3 src/query.py inputFile.json.gz queryFile.tsv outputFile.txt
```

---

## 📌 Important Functions

- `indexing()` — Builds inverted index by scene ID
- `docLength()` — Computes document lengths and average length
- `BM25(query, index)` — Ranks using BM25 formula
- `ql(query, index)` — Ranks using QL model
- `write()` — Ranks documents for each query and writes top 100 to output

---

## 🧾 Query Format

Each query in the `.tsv` file should follow this format:

```
query_id<TAB>return_type<TAB>ranking_model<TAB>term_1<TAB>term_2<...>
```

Example:
```
001	scene	bm25	my	lord
```

- `scene` or `play`: ranking unit
- `bm25` or `ql`: ranking method

---

## 📐 BM25 Formula

```
Score = IDF * ((k1 + 1) * fi / (K + fi)) * ((k2 + 1) * qfi / (k2 + qfi))
```

Where:
- `fi` = term freq in doc
- `qfi` = term freq in query
- `ni` = num of docs containing term
- `N` = total docs
- `K = k1 * ((1-b) + b * |D| / avgDL)`

Constants:
- `k1 = 1.8`, `k2 = 5`, `b = 0.75`

---

## 📐 QL Formula

Uses Dirichlet smoothing (μ = 300):

```
P(q|D) = log((fqi + μ * (cqi / |C|)) / (|D| + μ))
```

Where:
- `fqi` = term freq in doc
- `cqi` = term freq in collection
- `|C|` = total term count in corpus
- `|D|` = length of document

