import os
import json
import datetime

from extract_sections import extract_sections_from_documents
from embedder import load_embedder
from score_sections import rank_sections
from refine_text import extract_subsections

# Load persona and job-to-be-done
with open("sample_input.json", "r", encoding="utf-8") as f:
    input_data = json.load(f)
    persona_text = input_data.get("persona", {}).get("role", "")
    job_text = input_data.get("job_to_be_done", {}).get("task", "")
    input_docs_info = input_data.get("documents", [])

# Load the embedder model
embedder = load_embedder()
persona_embedding = embedder.encode(persona_text)
job_embedding = embedder.encode(job_text)

# Extract sections from documents
input_folder = "docs"
all_sections = []
input_docs = []

print("\n🔍 Extracting sections...")
for doc in input_docs_info:
    filename = doc["filename"]
    filepath = os.path.join(input_folder, filename)
    if os.path.exists(filepath):
        input_docs.append(filename)
        sections = extract_sections_from_documents(filepath)
        all_sections.extend(sections)
    else:
        print(f"⚠️ File not found: {filepath}")

# Rank sections
print("\n📊 Ranking sections...")
top_sections = rank_sections(all_sections, persona_embedding, job_embedding, embedder)

# Refine top sections
print("\n✨ Refining top sections...")
refined_subsections = extract_subsections(top_sections)

# Remove full text from top sections for final output
for section in top_sections:
    section.pop("text", None)

# Save output
output = {
    "metadata": {
        "input_documents": input_docs,
        "persona": persona_text,
        "job_to_be_done": job_text,
        "processing_timestamp": str(datetime.datetime.now())
    },
    "extracted_sections": top_sections,
    "subsection_analysis": refined_subsections
}

with open("sample_output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("\n✅ Output saved to sample_output.json")
