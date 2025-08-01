# 🧭 Round 1B Submission — Travel Planner Document Intelligence

In Round 1B of the "Connect What Matters — For the User Who Matters" challenge, we were tasked with building a **CPU-only, <1GB model** that analyzes input documents and intelligently extracts **relevant sections** based on a given **user persona** and their **job-to-be-done (JTBD)**.

## 💡 Solution Summary

Our solution is an **offline document intelligence pipeline** that:
- Extracts text from PDFs.
- Splits it into semantic sections and subsections.
- Embeds each section using a lightweight transformer model.
- Scores relevance based on cosine similarity with the persona + JTBD.
- Outputs a structured `sample_output.json` with metadata, ranked sections, and refined summaries.

## 🛠️ Tech Stack

- 🧠 Model: `all-MiniLM-L6-v2` from `sentence-transformers`
- 📚 PDF Processing: `PyMuPDF (fitz)`
- 🔍 Ranking: Maximal Marginal Relevance (MMR)
- 🧹 Text Refinement: Heuristic-based filtering
- 📦 Format: JSON output for easy downstream consumption


## 📦 Project Structure

```
Round_1B/
├── docs/                                # Folder for input PDFs
├── embedder.py                          # Embeds sections using MiniLM
├── extract_sections.py                  # Extracts title, text, and page
├── persona_job_embedding.py             # Embeds persona + task
├── refine_text.py                       # Cleans and summarizes extracted content
├── score_sections.py                    # Scores and ranks sections using MMR
├── main.py                              # Runs the complete pipeline
├── utils.py                             # Helper functions
├── sample_input.json                    # Persona + job input
├── sample_output.json                   # Final output in expected format
├── all_scored_sections.json             # All sections with cosine scores
├── top_sections_output.json             # Top-N relevant sections
├── refined_text.json                    # Refined summaries for top sections
├── SupervisedLearning_sections.json     # (Optional) output from supervised scoring
└── README.md                            # You’re here!
```

---

## ⚙️ How to Run

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Place PDFs** in the `docs/` folder.

3. **Edit** `sample_input.json` with your persona and task.

4. **Run pipeline**

   ```bash
   python main.py
   ```

5. **Output will be saved** as `sample_output.json`.

---

## ⚙️ How It Works

1. **Load Inputs**: PDFs from `docs/`, persona and JTBD from `sample_input.py`.
2. **Extract Sections**: Parse PDF into chunks with headings, body text, and page numbers.
3. **Embed Everything**: Encode both sections and the persona+JTBD using `MiniLM`.
4. **Score & Rank**: Use MMR to select top sections balancing relevance and diversity.
5. **Refine Text**: Clean up selected sections by removing noise and stitching context.
6. **Output**: Save structured JSON to `sample_output.json`.


---

## 📤 Sample Output

```json
{
  "metadata": {
    "input_documents": ["South of France - Cities.pdf", "..."],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-07-25 15:04:08.120201"
  },
  "extracted_sections": [
    {
      "document": "South of France - Cities.pdf",
      "section_title": "Page 2",
      "page_number": 2,
      "importance_rank": 1
    },
    ...
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Cities.pdf",
      "refined_text": "Overview of the Region...",
      "page_number": 2
    },
    ...
  ]
}
```

---

## 📌 Notes

* Uses `all-MiniLM-L6-v2` for embedding (\~80MB)
* Cosine similarity + Maximal Marginal Relevance (MMR) for ranking
* Efficient on CPU, no GPU required

---

## ✨ Improvements

* Better title/heading detection using layout-aware models (e.g., LayoutLM)
* Integrate abstractive summarization (DistilBART or LED)
* Add persona-task fine-tuning for scoring

---
