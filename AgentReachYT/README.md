<div align="center">
  <a href="https://youtu.be/S6AQKvweekA">
    <img src="https://img.youtube.com/vi/S6AQKvweekA/0.jpg" alt="Agent Reach AI: Build Your Own Content Engine Locally">
  </a>
  <h3>📺 <a href="https://youtu.be/S6AQKvweekA">Watch the full tutorial on YouTube</a></h3>
</div>

# 🎬 Zero-API YouTube-to-Blog SEO Engine — Agent Reach + Local LLM

<p align="center">
  <strong>Turn any YouTube video into a fully structured, SEO-optimized blog post - locally, for free, in seconds.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/LLM-Local%20(or%20Ollama)-black?style=for-the-badge&logo=ollama&logoColor=white" alt="Local LLM">
  <img src="https://img.shields.io/badge/yt--dlp-Agent%20Reach-red?style=for-the-badge&logo=youtube&logoColor=white" alt="yt-dlp">
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  <a href="#-features">Features</a> ·
  <a href="#-tech-stack">Tech Stack</a> ·
  <a href="#-setup--run">Setup</a> ·
  <a href="#-project-files">Files</a> ·
  <a href="#-use-cases">Use Cases</a> ·
  <a href="#-future-ideas">Future Ideas</a>
</p>

---

## 🌟 What is This?

A **zero-cost, privacy-first Streamlit app** that:

1. Takes any YouTube URL as input
2. Uses **Agent Reach** (`yt-dlp`) to download the video transcript - **no YouTube API key required**
3. Strips timestamps and deduplicates to produce clean plain text
4. Sends the transcript to a **local LLM** (Ollama or llama.cpp) via REST API
5. Outputs a fully structured, **SEO-optimized blog post** with meta description, headers, and bullet points

> 💡 **No API costs. No rate limits. No data leaves your machine.**

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🔑 **Zero-API** | No YouTube API key - uses `yt-dlp` (148K ⭐) via Agent Reach methodology |
| 🦙 **Local LLM** | Supports Ollama or llama.cpp - runs 100% offline after setup |
| 📝 **SEO Output** | Auto-generates meta description, H2/H3 headers, bullet points |
| 🌊 **Streaming** | Live streaming response directly in the Streamlit UI |
| 🧹 **Auto Cleanup** | Temporary `.vtt` transcript files deleted after use |
| ⚡ **Fast** | Uses quantized local models for quick, sharp responses |

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| **UI** | [Streamlit](https://streamlit.io) | Instant Python web UI, zero frontend code |
| **Transcript** | [yt-dlp](https://github.com/yt-dlp/yt-dlp) via Python API | Agent Reach's primary YouTube backend - no API key, 1800+ sites |
| **LLM** | [Ollama](https://ollama.com) or [llama.cpp](https://github.com/ggerganov/llama.cpp) | Run powerful models locally, fully free |
| **HTTP** | `requests` | POST to local LLM REST API |
| **Parsing** | Built-in string ops | Strip VTT timestamps and deduplicate cleanly |
| **Cleanup** | `os` + `glob` | Remove temp `.vtt` files post-extraction |

---

## ⚙️ Setup Instructions (Windows PowerShell)

### 1. Clone This Repo

```powershell
git clone https://github.com/47thtechcorner/AgentReachYT.git
cd AgentReachYT
```

### 2. Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -e ".[dev]"
```

### 4. Choose Your LLM Backend

#### Option A: Ollama

```powershell
# Install Ollama from https://ollama.com
ollama pull qwen2.5-coder:1.5b
```

Update `src/agentreachyt/config.py`:
```python
llm_backend = "ollama"
ollama_url = "http://localhost:11434/api/generate"
model = "qwen2.5-coder:1.5b"
```

#### Option B: llama.cpp (Docker)

```powershell
# Create models directory
mkdir models

# Place your .gguf model file in ./models/
# Example: models/LFM2.5-2.6B-Q4_K_M.gguf
```

Create `docker-compose.yml` in project root:

```yaml
services:
  llm-engine:
    image: ghcr.io/ggml-org/llama.cpp:server
    container_name: llama-cpp
    restart: unless-stopped
    ports:
      - "11434:8080"
    volumes:
      - ./models:/models
    command: "-m /models/YOUR_MODEL.gguf -c 32768 --host 0.0.0.0 --port 8080 --embedding --pooling mean"
```

Start the server:
```powershell
docker compose up -d
```

Update `src/agentreachyt/config.py`:
```python
llm_backend = "llama-cpp"
llama_cpp_url = "http://localhost:11434/v1/chat/completions"
model = "YOUR_MODEL.gguf"
```

### 5. Run the App

```powershell
streamlit run app.py
```

Open **http://localhost:8501** in your browser and paste any YouTube URL.

---

## 📁 Project Files

```
AgentReachYT/
├── .gitignore
├── docker-compose.yml       # Optional: llama.cpp server
├── pyproject.toml
├── app.py                   # Streamlit entry point
├── src/
│   └── agentreachyt/
│       ├── __init__.py
│       ├── config.py        # Settings and backend selection
│       ├── exceptions.py    # Custom exception classes
│       ├── llm.py           # Ollama + llama.cpp streaming
│       ├── transcript.py    # yt-dlp download + VTT parsing
│       └── ui.py            # Streamlit UI functions
└── tests/
    └── test_agentreachyt.py
```

### `app.py`

Minimal Streamlit entry point with Windows asyncio compatibility fix.

### `src/agentreachyt/`

The application logic, split into focused modules:

| Module | Purpose |
|--------|---------|
| **`config.py`** | Immutable settings dataclass, backend selection, API URLs |
| **`exceptions.py`** | Custom exception hierarchy |
| **`transcript.py`** | `yt-dlp` Python API invocation and VTT parsing |
| **`llm.py`** | Ollama + llama.cpp REST API streaming integration |
| **`ui.py`** | Streamlit page layout, inputs, and output rendering |

---

## 💡 Use Cases

- **Content Creators** - Repurpose your YouTube videos as blog posts automatically, boosting SEO without extra writing effort
- **Marketers** - Extract insights from competitor YouTube videos and publish keyword-rich summaries
- **Educators** - Convert lecture videos or tutorials into readable, shareable study notes
- **Developers** - Prototype AI-powered content pipelines locally with zero cloud costs
- **Journalists / Researchers** - Rapidly digest long-form interview or podcast videos into structured article drafts

---

## 🔮 Future Ideas

- **Multi-language support** - Auto-detect and translate non-English VTT transcripts before blogging
- **Batch mode** - Process entire YouTube playlists (channel-level SEO campaigns)
- **CMS export** - One-click publish to WordPress, Ghost, or Hashnode via their REST APIs
- **Custom prompts** - Let users pick blog style: listicle, deep-dive, news article, or tutorial
- **Keyword injector** - Input target SEO keywords and have the LLM weave them naturally into the post

---

## 🧠 Agent Reach Methodology

This project is built on the **Agent Reach** philosophy:

> *"The most reliable access path for each platform - chosen, installed, and health-checked for you."*

For YouTube, Agent Reach designates [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) as the primary backend - zero API key, zero rate limits, 1800+ supported sites.

```
YouTube URL → yt-dlp → .vtt file → parse → clean text → Local LLM → SEO Blog ✅
```

---

## 📄 License

MIT © 2026 - Free to use, fork, and build upon.

---

<!-- SEO KEYWORDS -->
<p align="center">
  <sub>
    agent reach tutorial · yt-dlp no api key · youtube to blog ai · ollama local llm · llama.cpp docker · streamlit ai app · free content engine · ai blog generator · youtube transcript extractor · local ai content automation · zero api youtube scraper · ai seo blog writer · python youtube automation · agent reach yt-dlp setup · free ai content pipeline
  </sub>
</p>
