Codes for AI project built in my YouTube channel RayCodes [https://youtu.be/e55FOUHX--Y]

# 🎙️ Local AI Restaurant Receptionist (Sarah)

A minimal, zero-latency, and fully local AI Voice Receptionist named **Sarah** designed for **The Rusty Spoon**. This project leverages the **Dograh** local orchestration framework, **Kokoro-82M** for human-like Text-to-Speech (TTS), and **Ollama** for real-time Large Language Model (LLM) processing.

By running completely locally, this voice agent achieves sub-500ms response start latency through parallelized audio stream pipeline workers.

---

## 🛠️ Tech Stack
1. **Dograh Framework (`dograh.py`)**: A multi-threaded python voice orchestration framework that connects the audio hardware, speech recognition (STT), LLM generator, and Text-to-Speech (TTS).
2. **Kokoro-82M**: A state-of-the-art, lightweight, and high-quality local text-to-speech model that outputs natural, expressive speech.
3. **Ollama (Llama 3.2 3B)**: A fast, local inference engine hosting the conversational LLM.

---

## ⚙️ Setup Steps

Follow these steps to set up and run the receptionist on your machine.

### 1. Install Ollama & Pull the Model
1. Download and install Ollama from [ollama.com](https://ollama.com).
2. Start the Ollama server (running `ollama serve` or starting the desktop application).
3. Pull the recommended fast model:
   ```bash
   ollama pull llama3.2:3b
   ```

### 2. Install eSpeak NG (Required for Kokoro TTS Phonemization)
Kokoro requires `eSpeak NG` to convert text into speech phonemes.
*   **Windows**: 
    1. Download the latest `.msi` installer from [eSpeak NG Releases](https://github.com/espeak-ng/espeak-ng/releases).
    2. Run the installer (it typically installs to `C:\Program Files\eSpeak NG`).
    3. The application will automatically detect this installation path.
*   **macOS**:
    ```bash
    brew install espeak-ng
    ```
*   **Linux (Ubuntu/Debian)**:
    ```bash
    sudo apt-get update && sudo apt-get install -y espeak-ng
    ```

### 3. Create a Python Virtual Environment
Navigate to the project root directory in your terminal and execute:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Windows (Command Prompt):
.\venv\Scripts\activate.bat
# On macOS / Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
*Note: The first time you run the agent, the `kokoro` library will automatically download the 82M parameter model weights (~300MB) from Hugging Face.*

---

## 🚀 Run & Test Steps

### 1. Run the Agent
With your virtual environment active and Ollama running:
```bash
.\venv\Scripts\python.exe agent.py 
```
You can also customize the model, Ollama URL, or Kokoro voice:
```bash
.\venv\Scripts\python.exe agent.py  --model llama3.2:3b --voice af_bella
```

### 2. Test the Conversation
1. Once initialized, the agent will speak its greeting: `"Thank you for calling The Rusty Spoon. This is Sarah speaking, how can I help you today?"`
2. Speak clearly into your microphone when the prompt displays `Listening...`.
3. Try asking:
   - *"What are your opening hours?"*
   - *"Can I book a table for 4 people tonight at 7 PM?"*
   - *"What kind of food do you serve?"*
4. Say *"Goodbye"* or *"Exit"* to end the call.

---

## 📂 Code Explanation
- **`requirements.txt`**: Lists all python dependencies, including `kokoro` (TTS), `sounddevice` / `soundfile` (audio output), `SpeechRecognition` (STT), and `openai` (Ollama wrapper).
- **`receptionist_prompt.txt`**: Contains the system instructions configuring Sarah's persona, knowledge of "The Rusty Spoon", and instructions to keep responses to 1-2 sentences for minimum latency.
- **`dograh.py`**: The local orchestration engine. It defines `DograhPipeline` which manages a multi-threaded pipe (LLM streaming -> sentence splitting -> TTS synthesis -> audio playback) to overlap workloads and ensure zero-latency.
- **`agent.py`**: The main execution script that ties everything together by initializing the pipeline, registering the Kokoro TTS provider, loading the prompt, and launching the interactive voice loop.

---

## 💼 Business Use Cases
1. **After-Hours Booking**: Accept reservations and answer basic inquiries automatically when the physical restaurant is closed.
2. **Peak-Hours Hostess Support**: Handle incoming phone calls during busy dinner rushes so waitstaff can focus on in-house diners.
3. **Queue / Waitlist Management**: Inform guests about current wait times and add them to virtual queues over the phone.
4. **FAQ Automation**: Automatically handle repetitive calls asking for directions, hours of operation, parking options, or dietary menu options.
5. **Interactive Outbound Confirmations**: Automatically call guests to confirm their reservation details, reducing costly no-shows.

---

## 🔮 Future Features for Scaling
1. **Twilio / Telephony Integration**: Route real phone calls from Twilio to the local pipeline using WebSockets.
2. **Retrieval-Augmented Generation (RAG)**: Connect the agent to a vector database containing detailed menu ingredients, allergen lists, and daily specials.
3. **SQL Booking Database Integration**: Connect Sarah directly to booking systems (like OpenTable or a local PostgreSQL database) to write reservations in real-time.
4. **Local Speech-to-Text Upgrade**: Replace Google STT with a local instance of `faster-whisper` or `Vosk` for a fully offline and private setup.
5. **Barge-in / Interruption Handling**: Implement advanced voice activity detection (VAD) that stops speaking immediately when the user interrupts mid-sentence.
