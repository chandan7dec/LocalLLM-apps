import os
import sys
from pathlib import Path

from anydoc_pipeline.converter import convert_document_to_markdown
from anydoc_pipeline.llm import query_llm

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "sample_docs"


def main():
    print("🚀 Initializing Firecrawl AnyDoc Markdown Converter & Intelligence Pipeline...")
    if not DOCS_DIR.exists():
        print(f"Directory '{DOCS_DIR}' not found.")
        return

    converted_markdown = {}
    files = sorted(os.listdir(str(DOCS_DIR)))
    print(f"📂 Found {len(files)} document files in '{DOCS_DIR}': {files}\n")

    for filename in files:
        filepath = DOCS_DIR / filename
        if filepath.is_file():
            print(f"⚡ Converting file to Markdown via Firecrawl AnyDoc: {filename}")
            md_text = convert_document_to_markdown(filepath)
            converted_markdown[filename] = md_text

    combined_context = ""
    for fname, text in converted_markdown.items():
        combined_context += f"\n=== FIRECRAWL ANYDOC MARKDOWN: {fname} ===\n{text}\n"

    prompt = f"""You are AnyDoc AI Document Intelligence Assistant powered by Firecrawl AnyDoc sub-5ms document converter.
Analyze the following clean GitHub-Flavored Markdown converted across multi-format enterprise files (PPTX, DOCX, CSV, HTML, TXT) and provide a comprehensive executive synthesis.

CONVERTED GFM MARKDOWN:
{combined_context}

FORMAT YOUR RESPONSE IN CLEAN MARKDOWN WITH:
# 📄 AnyDoc Executive Intelligence Synthesis

## 📊 Executive Overview
(Summarize the strategic objectives, financial performance, and enterprise compliance across all converted documents)

## 📁 Document-by-Document Extraction Analysis
(Detail key findings for each file: Q4_AI_Strategy.pptx, Vendor_Agreement.docx, Financial_Metrics.csv, Release_Notes.html, System_Audit.txt)

## 📈 Key Quantitative & Financial Metrics
(Present tabular data summarizing Ingested Documents, Accuracy, Latency, and Cost Savings)

## 🎯 Strategic Recommendations & Next Steps
(List 4 actionable recommendations based on the audit logs and vendor terms)
"""

    print("\n🧠 Querying local llama.cpp model (llama3.2:3b)...")
    ai_synthesis = query_llm(prompt)

    output_filepath = PROJECT_ROOT / "outputs.md"
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(ai_synthesis)

    print(f"\n✅ Firecrawl AnyDoc document conversion execution completed successfully!")
    print(f"📝 Output saved to: {output_filepath}")


if __name__ == "__main__":
    main()
