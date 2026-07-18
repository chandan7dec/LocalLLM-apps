#!/usr/bin/env python
"""
agent.py
Main execution script for the local AI Restaurant Receptionist.
Sets up the Dograh Pipeline, Kokoro-82M TTS, and Ollama.
"""

import sys
import argparse
from loguru import logger
from dograh import DograhPipeline, KokoroTTSProvider

def parse_args():
    parser = argparse.ArgumentParser(description="Dograh Local AI Restaurant Receptionist (Sarah)")
    parser.add_argument(
        "--model", 
        type=str, 
        default="llama3.2:3b", 
        help="Ollama model to use (default: llama3.2:3b)"
    )
    parser.add_argument(
        "--ollama-url", 
        type=str, 
        default="http://192.168.29.60:11434/v1", 
        help="Ollama API base URL"
    )
    parser.add_argument(
        "--voice", 
        type=str, 
        default="af_bella", 
        help="Kokoro voice to use (default: af_bella)"
    )
    parser.add_argument(
        "--prompt-path", 
        type=str, 
        default="receptionist_prompt.txt", 
        help="Path to system prompt file"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Configure logging
    logger.remove()
    logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}", level="INFO")
    
    logger.info("Starting Sarah - Local AI Restaurant Receptionist...")
    
    # 1. Initialize the Dograh Pipeline
    pipeline = DograhPipeline(llm_model=args.model, llm_url=args.ollama_url)
    
    # 2. Register Kokoro-82M as the TTS provider
    # af_bella is a warm, friendly female voice (perfect for a receptionist)
    tts_provider = KokoroTTSProvider(voice=args.voice, speed=1.0)
    pipeline.set_tts_provider(tts_provider)
    
    # 3. Load the receptionist persona prompt
    try:
        pipeline.load_prompt(args.prompt_path)
    except FileNotFoundError:
        logger.error(f"System prompt file not found at {args.prompt_path}. Please check your files.")
        return 1
        
    # 4. Connect to Ollama, initialize hardware, and start the voice loop
    try:
        pipeline.start_voice_loop()
    except Exception as e:
        logger.error(f"Failed to start receptionist voice agent: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
