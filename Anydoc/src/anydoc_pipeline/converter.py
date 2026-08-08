"""Document conversion using Firecrawl AnyDoc."""

import anydoc
from pathlib import Path


def convert_document_to_markdown(filepath: Path) -> str:
    """
    Uses Firecrawl AnyDoc (firecrawl-anydoc) Rust C-extension bindings
    to convert office documents (PPTX, DOCX, CSV, PDF, RTF) into LLM-ready GFM Markdown in sub-5ms.
    """
    try:
        markdown = anydoc.to_markdown(str(filepath))
        return markdown.strip()
    except anydoc.UnsupportedError:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        return f"[AnyDoc Conversion Error: {e}]"
