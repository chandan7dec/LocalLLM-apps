import os
import sys
import time
import queue
import threading
import re
from pathlib import Path
from loguru import logger
from openai import OpenAI

# Automatically configure eSpeak NG paths on Windows if found
if sys.platform == "win32":
    espeak_paths = [
        r"C:\Program Files\eSpeak NG\espeak-ng.exe",
        r"C:\Program Files (x86)\eSpeak NG\espeak-ng.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\eSpeak NG\espeak-ng.exe")
    ]
    for path in espeak_paths:
        if os.path.exists(path):
            logger.info(f"Automatically configured eSpeak NG path: {path}")
            os.environ["PHONEMIZER_ESPEAK_PATH"] = os.path.dirname(path)
            break

class KokoroTTSProvider:
    """TTS Provider using the local Kokoro-82M model."""
    def __init__(self, voice="af_bella", speed=1.0, lang_code="a"):
        self.voice = voice
        self.speed = speed
        self.lang_code = lang_code
        self.pipeline = None

    def initialize(self):
        """Lazy load the Kokoro model to keep startup fast."""
        try:
            from kokoro import KPipeline
            logger.info(f"Initializing Kokoro-82M pipeline for language '{self.lang_code}'...")
            # KPipeline handles downloading the model from HuggingFace to cache
            self.pipeline = KPipeline(lang_code=self.lang_code)
            logger.info("Kokoro-82M TTS initialized successfully.")
        except ImportError:
            raise ImportError(
                "Could not import 'kokoro'. Please ensure you have run: pip install kokoro torch soundfile"
            )
        except Exception as e:
            if "espeak" in str(e).lower() or "phonemizer" in str(e).lower():
                raise RuntimeError(
                    f"Kokoro G2P initialization failed: {e}\n"
                    "Dograh requires eSpeak NG on your system for phonemization.\n"
                    "Download and install eSpeak NG from: https://github.com/espeak-ng/espeak-ng/releases"
                )
            raise e

    def generate_audio(self, text):
        """Generates audio samples for the given text.
        Yields numpy arrays (audio chunks) and samplerate.
        """
        if not self.pipeline:
            self.initialize()
        
        # Kokoro pipeline returns a generator yielding (graphemes, phonemes, audio)
        # where audio is a numpy array of 24kHz audio samples
        generator = self.pipeline(text, voice=self.voice, speed=self.speed)
        for _, _, audio in generator:
            if audio is not None and len(audio) > 0:
                yield audio, 24000


class LocalMicrophoneTransport:
    """Handles local microphone input capture and speaker output."""
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.recognizer = None
        self.microphone = None

    def initialize(self):
        """Initialize audio devices and speech recognition."""
        try:
            import speech_recognition as sr
            import sounddevice as sd
            self.recognizer = sr.Recognizer()
            # Set dynamic energy thresholding for better silence detection
            self.recognizer.dynamic_energy_threshold = True
            
            # Verify input device exists
            devices = sd.query_devices()
            input_device = sd.query_devices(kind='input')
            logger.info(f"Using default input audio device: {input_device['name']}")
            
            self.microphone = sr.Microphone(sample_rate=self.sample_rate)
            logger.info("Microphone and Speaker audio devices initialized.")
        except OSError as e:
            raise RuntimeError(
                f"Failed to access audio hardware: {e}\n"
                "Please verify that a microphone is plugged in, active, and that Python has permissions to access it."
            )
        except ImportError:
            raise ImportError(
                "Could not import speech_recognition or sounddevice. "
                "Run: pip install SpeechRecognition sounddevice"
            )

    def listen(self, timeout=10, phrase_time_limit=6):
        """Listens to the microphone and returns transcribed text using SpeechRecognition."""
        if not self.recognizer:
            self.initialize()
        
        import speech_recognition as sr
        with self.microphone as source:
            logger.info("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio_data = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logger.info("Processing speech...")
                # Recognize using Google Speech Recognition (free, fast, no API key needed)
                text = self.recognizer.recognize_google(audio_data)
                return text.strip()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                # Speech was detected but could not be understood
                return ""
            except sr.RequestError as e:
                logger.warning(f"Google Speech Recognition service error: {e}. Falling back...")
                return ""


class DograhPipeline:
    """The Dograh Voice Agent Orchestration Pipeline."""
    def __init__(self, llm_model="llama3.2:3b", llm_url="http://localhost:11434/v1"):
        self.llm_model = llm_model
        self.llm_url = llm_url
        self.system_prompt = ""
        self.history = []
        
        self.transport = LocalMicrophoneTransport()
        self.tts_provider = None
        self.llm_client = None
        
        # Threading queues for overlapping pipeline execution (pipelining)
        self.sentence_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        
        self.is_running = False
        self.threads = []

    def set_tts_provider(self, tts_provider: KokoroTTSProvider):
        """Registers the TTS provider."""
        self.tts_provider = tts_provider

    def load_prompt(self, path):
        """Loads system prompt from a file."""
        self.system_prompt = Path(path).read_text(encoding="utf-8").strip()
        logger.info(f"Loaded system prompt from {path}")

    def initialize(self):
        """Initializes all registered sub-components."""
        # Connect to Ollama via OpenAI API compatibility
        self.llm_client = OpenAI(base_url=self.llm_url, api_key="ollama")
        
        # Verify Ollama server connection
        try:
            self.llm_client.models.list()
            logger.info(f"Connected to Ollama instance at {self.llm_url}")
        except Exception as e:
            raise RuntimeError(
                f"Could not connect to Ollama server at {self.llm_url}.\n"
                "Please make sure Ollama is running (`ollama serve`) and you have pulled the model (`ollama pull {self.llm_model}`)."
            )
        
        # Initialize hardware & TTS
        self.transport.initialize()
        if self.tts_provider:
            self.tts_provider.initialize()
        else:
            logger.warning("No TTS provider registered in Dograh pipeline! Speech playback will be disabled.")

    def _split_into_sentences(self, text_stream_generator):
        """Splits incoming text tokens into full sentences to feed into TTS without delay."""
        buffer = ""
        sentence_endings = re.compile(r'([.!?]+)\s*')
        
        for chunk in text_stream_generator:
            content = chunk.choices[0].delta.content
            if content:
                buffer += content
                # Search for sentence boundaries
                match = sentence_endings.search(buffer)
                while match:
                    end_idx = match.end()
                    sentence = buffer[:end_idx].strip()
                    buffer = buffer[end_idx:]
                    if sentence:
                        yield sentence
                    match = sentence_endings.search(buffer)
        
        # Yield any remaining text
        remaining = buffer.strip()
        if remaining:
            yield remaining

    def _llm_worker(self, user_input):
        """Streams LLM tokens, splits them into sentences, and queues them."""
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            # Append conversation history
            messages.extend(self.history[-8:]) # Last 8 turns to preserve context and speed
            messages.append({"role": "user", "content": user_input})
            
            stream = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                stream=True,
                temperature=0.7
            )
            
            full_response = ""
            for sentence in self._split_into_sentences(stream):
                if not self.is_running:
                    break
                # Filter out raw markdown bolding or think tags
                clean_sentence = re.sub(r'<\/?think>', '', sentence)
                clean_sentence = clean_sentence.replace("**", "").replace("*", "").strip()
                if clean_sentence:
                    logger.debug(f"LLM Sentence: {clean_sentence}")
                    self.sentence_queue.put(clean_sentence)
                    full_response += clean_sentence + " "
            
            # Store turn in history
            self.history.append({"role": "user", "content": user_input})
            self.history.append({"role": "assistant", "content": full_response.strip()})
            
        except Exception as e:
            logger.error(f"Error in LLM stream: {e}")
            self.sentence_queue.put("Sorry, I had trouble processing that request.")
        finally:
            # Signal that the LLM is done generating sentences
            self.sentence_queue.put(None)

    def _tts_worker(self):
        """Pulls sentences from queue, synthesizes audio using Kokoro, and queues audio arrays."""
        while self.is_running:
            try:
                sentence = self.sentence_queue.get(timeout=0.5)
                if sentence is None:
                    # End of response stream
                    self.audio_queue.put((None, None))
                    self.sentence_queue.task_done()
                    break
                
                start_time = time.time()
                # Generate audio chunk
                if self.tts_provider:
                    audio_chunks = list(self.tts_provider.generate_audio(sentence))
                    if audio_chunks:
                        logger.info(f"Synthesized audio in {time.time() - start_time:.3f}s for: '{sentence}'")
                        for audio, rate in audio_chunks:
                            self.audio_queue.put((audio, rate))
                
                self.sentence_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in TTS synthesis: {e}")

    def _playback_worker(self):
        """Pulls audio chunks from queue and plays them back sequentially."""
        import sounddevice as sd
        while self.is_running:
            try:
                audio, rate = self.audio_queue.get(timeout=0.5)
                if audio is None:
                    self.audio_queue.task_done()
                    break
                
                # Play audio using sounddevice
                sd.play(audio, rate)
                sd.wait() # Block until playback finishes
                self.audio_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error during audio playback: {e}")

    def run_agent_turn(self, user_input):
        """Executes a single conversational agent turn."""
        self.is_running = True
        
        # Clean queues
        while not self.sentence_queue.empty():
            self.sentence_queue.get()
        while not self.audio_queue.empty():
            self.audio_queue.get()
            
        # Spawn pipelined background workers for LLM generation, TTS synthesis, and audio playback
        llm_thread = threading.Thread(target=self._llm_worker, args=(user_input,))
        tts_thread = threading.Thread(target=self._tts_worker)
        playback_thread = threading.Thread(target=self._playback_worker)
        
        llm_thread.start()
        tts_thread.start()
        playback_thread.start()
        
        # Block until playback completes
        llm_thread.join()
        tts_thread.join()
        playback_thread.join()
        
        self.is_running = False

    def start_voice_loop(self):
        """Runs the main interactive voice conversation loop."""
        logger.info("Initializing voice loop components...")
        self.initialize()
        
        print("\n=======================================================")
        print("    Sarah, The Rusty Spoon Receptionist is Online!     ")
        print("=======================================================")
        print("Speak into your microphone. Say 'exit' or 'quit' to stop.\n")
        
        # Speak initial greeting
        initial_greeting = "Thank you for calling The Rusty Spoon. This is Sarah speaking, how can I help you today?"
        print(f"Sarah: {initial_greeting}")
        if self.tts_provider:
            # Simple synchronous greeting playback
            for audio, rate in self.tts_provider.generate_audio(initial_greeting):
                import sounddevice as sd
                sd.play(audio, rate)
                sd.wait()
                
        # Main conversational loop
        while True:
            try:
                user_input = self.transport.listen()
                if user_input is None:
                    # Timeout, no speech detected
                    continue
                
                if user_input == "":
                    # Unrecognized speech
                    print("Sarah: (could not hear you clearly)")
                    continue
                
                print(f"You: {user_input}")
                
                if user_input.lower() in ["exit", "quit", "goodbye", "bye"]:
                    farewell = "Thank you for calling The Rusty Spoon. Have a wonderful day!"
                    print(f"Sarah: {farewell}")
                    if self.tts_provider:
                        for audio, rate in self.tts_provider.generate_audio(farewell):
                            import sounddevice as sd
                            sd.play(audio, rate)
                            sd.wait()
                    break
                
                # Execute turn with pipelining
                self.run_agent_turn(user_input)
                
            except KeyboardInterrupt:
                print("\nStopping Agent...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                break
        
        print("=======================================================")
        print("                   Agent Terminated                    ")
        print("=======================================================")
