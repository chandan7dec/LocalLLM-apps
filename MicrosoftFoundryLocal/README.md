<div align="center">
  <a href="https://youtu.be/QkIgzW-OWcg">
    <img src="https://img.youtube.com/vi/QkIgzW-OWcg/0.jpg" alt="Microsoft Foundry is NOW LOCAL! Turn Your PC Into a Private AI Server">
  </a>
  <h3>📺 <a href="https://youtu.be/QkIgzW-OWcg">Watch the full tutorial on YouTube</a></h3>
</div>

<br />

# 📋 Microsoft Foundry Clipboard Copilot

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Foundry Local SDK](https://img.shields.io/badge/Foundry%20Local-1.2.4-00A4EF.svg)](https://learn.microsoft.com/en-us/azure/foundry-local/)
[![Offline Privacy](https://img.shields.io/badge/Privacy-100%25%20On--Device-7FBA00.svg)](#)

An instant, offline system-tray keyboard copilot that automatically fixes spelling, grammar, and sentence tone directly from your clipboard using local AI models with zero cloud latency.

## 🔄 3-Step Workflow

| Step 1: Input | Step 2: AI Action | Step 3: Result |
| :--- | :--- | :--- |
| Copy unedited draft text to OS clipboard | Press global hotkey `Ctrl+Alt+G` | Corrected text instantly updates clipboard |

---

## ⚡ Quickstart & Installation

### 1. Prerequisites & Model Download
Ensure [Ollama](https://ollama.com/) or Microsoft Foundry Local runtime is running locally. Download the fast 3B local model:

```powershell
ollama run llama3.2:3b
```

### 2. Create the Virtual Environment & Install Dependencies

```powershell
# One-command setup: creates .venv, installs the package (editable) with
# core deps, plus optional extras (Foundry SDK, keyboard, lint tools).
.\setup_env.ps1
```

Or do it manually:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .                                 # core dependencies
pip install -r requirements-optional.txt         # Foundry SDK + keyboard (optional)
```

> `foundry-local-sdk` and `keyboard` are **optional**. The app auto-detects
> them at startup and degrades gracefully (Ollama backend / interactive CLI)
> when they are not installed.

### 3. Launch the Copilot

```powershell
# Activate the environment
.venv\Scripts\Activate.ps1

# Option A: run as a module (recommended)
python -m clipboard_copilot

# Option B: use the installed console script, or the backward-compat shim
clipboard-copilot
# python main.py   # also still works
```


---

## 🛠️ Tech Stack

- **Microsoft Foundry Local SDK (`foundry-local-sdk`)**: On-device AI inference manager and ONNX engine runtime.
- **Pyperclip (`pyperclip`)**: Cross-platform system clipboard read/write engine.
- **Keyboard (`keyboard`)**: Low-latency global OS system keypress listener.
- **Python 3.10+**: Core orchestration engine.
- **`pyproject.toml` + `setuptools`**: Standard src-layout packaging with an optional editable install (`pip install -e .`).
- **`.venv` / `setup_env.ps1`**: Isolated virtual environment with one-command bootstrap.
- **Ruff / Mypy**: Linting and static type checking (in `requirements-dev.txt`).

---

## 🏆 Why Foundry Local SDK vs. Ollama?

| Feature / Metric | Microsoft Foundry Local SDK | Standard Ollama |
| :--- | :--- | :--- |
| **Execution Architecture** | **In-Process C++ ONNX Engine** (Zero HTTP socket latency) | Background Server Daemon (`ollama serve` HTTP API) |
| **NPU Acceleration** | **Native Copilot+ NPU & DirectML GPU** bindings | CUDA / ROCm / CPU fallback |
| **App Bundling** | **Standalone ~20MB Embedded SDK** inside your app | Requires users to download 500MB+ external installer |
| **Model Catalog** | ONNX Quantized Chat + Whisper Audio + Vision | GGUF LLM models only |

---

## 📁 File Structure

```text
Microsoft Foundry Local/
├── .gitignore
├── pyproject.toml             # project metadata + packaging (src-layout)
├── requirements.txt           # core dependencies
├── requirements-optional.txt  # foundry-local-sdk + keyboard (auto-detected)
├── requirements-dev.txt       # linting / typing tools
├── setup_env.ps1              # one-command Windows environment bootstrap
├── main.py                    # backward-compatible entry-point shim
└── src/
    └── clipboard_copilot/     # importable package
        ├── __init__.py
        ├── __main__.py        # python -m clipboard_copilot
        ├── version.py         # __version__
        ├── config.py          # constants + UTF-8 terminal setup
        ├── inference.py       # Foundry SDK + Ollama backends
        └── app.py             # clipboard logic, hotkeys, main loop
```

---

## 💡 5 Real-World Use Cases

1. **Slack & Teams Messages**: Instantly fix typos in casual draft chat messages before sending to leadership.
2. **Code Comment Polishing**: Refine awkwardly worded Python and JavaScript docstrings straight inside VS Code.
3. **Executive Email Drafts**: Polish quick informal notes into clear, professional client updates.
4. **Offline Travel Writing**: Edit documentation on flights without requiring cellular data or Wi-Fi.
5. **Private Confidential Notes**: Guarantee zero data exposure when editing sensitive legal or internal notes.

---

## 🔮 5 Future Enhancements

1. **Multi-Language Translation**: Add quick hotkey toggles (`Ctrl+Alt+T`) for instant local language translation.
2. **Tone Switcher**: Support custom hotkeys for Concise, Formal, or Friendly tone transformations.
3. **System Tray GUI Icon**: Add a native desktop taskbar icon with model selection menus.
4. **Custom Prompt Templates**: Allow users to save reusable local text modification prompts.
5. **Diff Highlight Overlay**: Display a temporary semi-transparent OS popup showing exact text edits before pasting.

---

## 🏷️ Keywords

`Microsoft Foundry Local` `Foundry Local SDK` `Local AI Server` `Clipboard Copilot` `On-Device AI` `Private AI` `Ollama` `Python AI Copilot` `ONNX Runtime` `DirectML NPU`
