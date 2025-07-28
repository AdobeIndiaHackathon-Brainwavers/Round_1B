import fitz  # PyMuPDF
import os

def extract_subsections(top_sections):
    refined = []

    for section in top_sections:
        doc_path = section["document"]
        page_num = section["page_number"]
        title = section["section_title"].strip().lower()

        # ✅ Correct full path to the PDF inside "docs/" folder
        full_path = os.path.join("docs", doc_path)

        try:
            doc = fitz.open(full_path)
            page = doc[page_num - 1]

            text_blocks = page.get_text("blocks")
            all_text = " ".join([block[4].strip() for block in text_blocks if block[4].strip()])
            all_text_lower = all_text.lower()

            # Split text into logical paragraphs
            paragraphs = all_text.split("\n\n")
            matched_para = ""

            # Try to match paragraph with section title
            for para in paragraphs:
                if title in para.lower():
                    matched_para = para.strip()
                    break

            # Fallback: first long enough paragraph
            if not matched_para:
                for para in paragraphs:
                    if len(para.strip()) > 80:
                        matched_para = para.strip()
                        break

            refined.append({
                "document": doc_path,
                "refined_text": matched_para,
                "page_number": page_num
            })

        except Exception as e:
            print(f"Error processing {doc_path} page {page_num}: {e}")

    return refined
