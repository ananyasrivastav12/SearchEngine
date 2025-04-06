# 🗂 Indexing and Phrase Query Processing

This module builds an **inverted index** over a corpus of Shakespeare plays and scenes, and processes **phrase-based Boolean queries** to retrieve relevant documents (scenes or plays).

---

## 🧠 What It Does

- Reads a compressed JSON corpus of plays and builds an inverted index with positional information.
- Handles multi-word phrase queries and supports Boolean operators like `AND`.
- Returns either matching scenes or plays, depending on the query.
- Outputs results to text files — one per query.

---

## 📁 Folder Structure

- `src/indexer.py` — main script containing all logic.
- `shakespeare-scenes.json.gz` — compressed corpus of play scenes.
- `trainQueries.tsv` — file with structured queries.
- `results/` — output directory for query result files.

Each query is processed using a **document-at-a-time** strategy, checking whether the full phrase exists at the correct positions within documents.

---

## 🧾 Query Format (trainQueries.tsv)

Each query has the format:

```
query_id<TAB>return_type<TAB>boolean_operator<TAB>phrase_1<TAB>phrase_2<...>
```

Example:

```
001	scene	and	my lord<tab>good sir
```

- `scene`: retrieve scene IDs
- `and`: apply Boolean AND across phrases
- `my lord`, `good sir`: phrases to match

---

## 🚀 How to Run

```bash
python3 src/indexer.py
```

If not passing command-line arguments, default files will be used:
- `shakespeare-scenes.json.gz`
- `trainQueries.tsv`
- Outputs will be written to `results/`

You can also run it with custom files:

```bash
python3 src/indexer.py inputFile.json.gz queryFile.tsv outputFolder/
```

---

## 🧰 Libraries Used

- `gzip`, `json` — for reading compressed JSON corpus
- `os`, `sys` — for file handling
- `matplotlib` — for optional analysis/visualization (not essential for indexing)

---

## 📌 Key Functions

- `indexing()` — Builds the inverted index with word → [(playId, sceneId, position)] mappings
- `documentAtATime()` — Processes phrase queries with positional logic
- `boole()` — Applies Boolean `AND` across phrase result sets
- `write()` — Writes the sorted result list to file
- `main()` — Ties everything together for batch query processing


