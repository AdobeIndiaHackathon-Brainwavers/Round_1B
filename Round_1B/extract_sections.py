import fitz  # PyMuPDF
import os
import re

def extract_sections_from_documents(filepath):
    doc = fitz.open(filepath)
    extracted_sections = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            block_text = ""
            for line in block["lines"]:
                for span in line["spans"]:
                    block_text += span["text"] + " "

            block_text = block_text.strip()
            if not block_text:
                continue

            # Heuristic: uppercase and short blocks are section titles
            is_title = bool(re.fullmatch(r"[A-Z\s:,\-0-9]{5,100}", block_text.strip()))
            section_title = block_text if is_title else f"Page {page_num + 1}"

            extracted_sections.append({
                "document": os.path.basename(filepath),
                "section_title": section_title.strip(),
                "page_number": page_num + 1,
                "text": block_text
            })

    return extracted_sections
