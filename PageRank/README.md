# 🌐 PageRank with the Random Surfer Model

This project implements the **PageRank algorithm** using the **random surfer model** over a set of hyperlinks. The input is a compressed `.gz` file containing links between pages, and the output is the computed PageRank scores and inlink statistics.

---

## 🧠 What It Does

- Parses a `.gz` file of hyperlinks into a graph representation
- Divides the graph into **Pages** and **Inlinks**
- Computes PageRank scores using an iterative, random-surfer-based method
- Stops iterating when L2 norm of rank change is below a threshold (τ)
- Outputs top-100 ranked pages and most linked pages

---

## 📂 Key Files

- `src/pagerank.py` — Main script with all logic
- `links.srt.gz` — Input file of links (default)
- `pagerank.txt` — Output: Top 100 pages by PageRank
- `inlinks.txt` — Output: Top 100 pages by inlink count

---

## 🚀 How to Run

Run with **default parameters**:

```bash
python3 src/pagerank.py
```

Run with **custom arguments**:

```bash
python3 src/pagerank.py inputFile.gz lambda_val tau inlinksOutput.txt pagerankOutput.txt k
```

Example:

```bash
python3 src/pagerank.py links.srt.gz 0.2 0.005 inlinks.txt pagerank.txt 100
```

---

## 🧪 Key Functions

- `inlinks()` — Parses the file and extracts:
  - `Pages`: All unique nodes
  - `Links`: Mapping of pages to their outlinks
  - `Inlink count`: Used to compute popularity

- `pagerank()` — Iteratively computes PageRank scores using:
  - `λ` (lambda_val): Random surfer probability
  - `τ` (tau): Convergence threshold

- `converge()` — Calculates L2 norm between rank vectors to determine convergence

- `writePagerank()` — Writes top-ranked pages by PageRank score
- `writeToInlinks()` — Writes top pages by number of inlinks

---

## 📚 Libraries Used

- `collections` — For frequency counting and sorting
- `gzip` — For reading `.gz` input files
- `math` — For computing L2 norm and square roots

---

## 🧾 Output Format

Both `pagerank.txt` and `inlinks.txt` list:

```
<page_id> <rank_position> <score/count>
```

