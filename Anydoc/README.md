<div align="center">
  <a href="https://youtu.be/G_yqPWRHlXM">
    <img src="https://img.youtube.com/vi/G_yqPWRHlXM/0.jpg" alt="Firecrawl AnyDoc: Blazing Fast 4ms Document Parsing!">
  </a>
  <h3>📺 <a href="https://youtu.be/G_yqPWRHlXM">Watch the full tutorial on YouTube</a></h3>
</div>

# 📄 Firecrawl AnyDoc Markdown Engine

<p align="left">
  <a href="https://pypi.org/project/firecrawl-anydoc/"><img src="https://img.shields.io/pypi/v/firecrawl-anydoc.svg?style=for-the-badge&color=FF5722" alt="PyPI"></a>
  <a href="https://ollama.com"><img src="https://img.shields.io/badge/Ollama-llama3.2%3A3b-8B5CF6?style=for-the-badge" alt="Ollama"></a>
  <a href="https://github.com/firecrawl/anydoc"><img src="https://img.shields.io/badge/Speed-Sub--5ms-10B981?style=for-the-badge" alt="Speed"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-00C8FF?style=for-the-badge" alt="License"></a>
</p>

An enterprise multi-format document conversion and AI intelligence pipeline powered by **Firecrawl AnyDoc (`firecrawl-anydoc`)** sub-5ms Rust C-extension bindings and local **Ollama LLM (`llama3.2:3b`)** reasoning.

---

### 🚨 Problem to be Solved & Target Solution

> [!IMPORTANT]
> **Enterprise Document Challenge:** Multi-format document workflows suffer from high latency (500ms–1100ms+ per doc), incomplete file coverage (failing on `.pptm`, `.docm`, `.rtf`, `.odt`), and cloud privacy risks.
> **Firecrawl AnyDoc Solution:** Converts 14/14 office formats into unified GFM Markdown in sub-5ms with zero cloud token cost and 100% local on-premise execution.

#### 🎯 Enterprise Document Challenge vs Firecrawl AnyDoc Solution

| Feature Category | ❌ Legacy Document Parsers (LibreOffice / Docling) | ✅ Firecrawl AnyDoc Engine |
| :--- | :--- | :--- |
| ⏱️ **Conversion Latency** | **500ms – 1,129ms** per document (Heavy ML/JVM overhead) | ⚡ **4.4ms median speed** (100x faster pure Rust C-extension) |
| 📁 **Format Coverage** | **4 – 8 formats** (Fails on `.pptm`, `.docm`, `.rtf`, `.odt`) | 📦 **14 / 14 Formats** (`.docx`, `.pptx`, `.xlsx`, `.pdf`, `.epub`, `.csv`) |
| 🧠 **LLM Readiness** | Inconsistent Markdown, broken tables, missing anchors | 📄 **Unified GFM Markdown** (Shared document model & single serializer) |
| 🔒 **Privacy & Cost** | High cloud API costs / Third-party data exposure | 🛡️ **100% On-Premise & Local** (Zero external cloud token fees) |

```text
┌───────────────────────────────────┐      ┌───────────────────────────────────┐      ┌───────────────────────────────────┐
│   📁 14+ Document Formats         │      │  ⚡ Firecrawl AnyDoc Engine       │      │   🧠 Local Ollama AI Pipeline     │
│                                   │      │                                   │      │                                   │
│   • PowerPoint (.pptx, .ppt)      │ ───► │   • Content-Based Format Detection│ ───► │   • llama3.2:3b Reasoning Model   │
│   • Word (.docx, .doc)            │      │   • Shared Document Representation│      │   • Multi-Document Synthesis      │
│   • Excel (.csv, .xlsx)           │      │   • Sub-5ms GFM Markdown Stream   │      │   • Output: Executive AI Report   │
└───────────────────────────────────┘      └───────────────────────────────────┘      └───────────────────────────────────┘
```

---

## ⚡ Quick Start & Run Commands

Execute these steps in your Windows PowerShell terminal:

### 1. Setup Virtual Environment & Install Dependencies
```powershell
uv venv
uv sync
```

### 2. Launch Local Ollama Model
Ensure Ollama is running locally and pull the target reasoning model:
```powershell
ollama run llama3.2:3b
```

### 3. Run Document Intelligence Engine
Execute the conversion pipeline to convert all files inside `sample_docs/` to Markdown and synthesize executive insights:
```powershell
uv run anydoc
```

---

## 📐 Technical Architecture & Module Structure

The project maintains a high-performance Python engine leveraging Firecrawl AnyDoc Rust native binaries:

```
Anydoc/
├── pyproject.toml        # ⚡ Project metadata, dependencies, and uv entry point
├── src/
│   └── anydoc_pipeline/  # 📦 Main Python package
│       ├── __init__.py
│       ├── converter.py  # ⚡ Firecrawl AnyDoc document-to-Markdown conversion
│       ├── llm.py        # 🧠 Local Ollama LLM query wrapper
│       └── main.py       # ⚡ Primary orchestration engine
├── sample_docs/          # 📂 Multi-format document workspace
│   ├── Q4_AI_Strategy.pptx
│   ├── Vendor_Agreement.docx
│   ├── Financial_Metrics.csv
│   ├── Release_Notes.html
│   └── System_Audit.txt
├── outputs.md            # 📄 Generated executive synthesis report
└── README.md             # 📄 Root project documentation
```

### Module Explanations

- **`pyproject.toml`**: Defines project metadata, dependencies (`firecrawl-anydoc`, `requests`), and the `anydoc` console script entry point managed by `uv`.
- **`src/anydoc_pipeline/`**: Main Python package containing the engine logic.
- **`converter.py`**: Wraps `anydoc.to_markdown(filepath)` C-extension calls with error handling. Detects format signatures and converts documents into unified GFM Markdown in <5ms.
- **`llm.py`**: Handles communication with the local Ollama REST API (`llama3.2:3b`), constructing prompts and streaming responses.
- **`main.py`**: Orchestrates the pipeline — scans `sample_docs/`, converts each file, combines markdown context, queries the LLM, and writes the final synthesis to `outputs.md`.
- **`sample_docs/`**: Working document directory containing multi-category open-source test files demonstrating slide deck parsing, table mapping, spreadsheet numerical ingestion, and text log analysis.
- **`README.md`**: Project documentation covering setup, architecture, installation, and usage commands.

---

## 🌟 5 Real-World Enterprise Use Cases

1. **⚡ Sub-5ms LLM RAG Ingestion**: Convert incoming email attachments (DOCX, PPTX, XLSX) into clean Markdown instantly before vector embedding in RAG pipelines.
2. **📈 M&A Financial Auditing**: Ingest quarterly financial spreadsheets (CSV/XLSX) and presentation decks (PPTX) into unified Markdown reports for instant compliance checks.
3. **📜 Legal Contract Review**: Convert multi-page Word contracts (`.docx`/`.doc`) to GFM Markdown with preserved heading anchors and table structures for automated risk scoring.
4. **🔒 Offline Air-Gapped Intelligence**: Process sensitive enterprise documents locally without external OCR services, cloud API keys, or internet connectivity.
5. **🌐 Cross-Format Knowledge Migration**: Convert legacy office documents (`.doc`, `.ppt`, `.rtf`, `.odt`) into standardized GitHub-Flavored Markdown for developer documentation portals.

---

## 🚀 5 Future Engineering Roadmap Features

1. **☁️ Hosted Firecrawl Parse Cloud OCR**: Integrate Firecrawl Parse hosted API for scanned image-only PDF OCR extraction.
2. **🌐 WASM Browser Client Integration**: Embed `@firecrawl/anydoc-wasm` for zero-server client-side document conversions inside web apps.
3. **⚡ Multi-Threaded Directory Ingestion**: Process large document folders using Python thread pools to convert thousands of files per second.
4. **🗄️ Vector Database Chroma Integration**: Embed converted GFM document chunks directly into local ChromaDB collection indexes.
5. **🤖 CLI Skill Distribution**: Package as an Agent Skill (`npx skills add firecrawl/anydoc`) for automated LLM coding agent document reading.

---

## 🏷️ Keywords & Search Tags
`firecrawl-anydoc` `document-parsing` `rust-converter` `gfm-markdown` `ollama-llm` `python-bindings` `fast-markdown-converter` `anydoc` `firecrawl` `document-ai`
