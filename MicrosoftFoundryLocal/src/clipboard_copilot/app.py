"""Application logic: clipboard handling, hotkeys, and the main event loop."""

from __future__ import annotations

import time

import pyperclip

from clipboard_copilot.inference import HAS_FOUNDRY_SDK, correct_text

try:
    import keyboard

    HAS_KEYBOARD = True
except ImportError:
    HAS_KEYBOARD = False


def process_clipboard() -> None:
    """Read clipboard text, correct its grammar, and overwrite the clipboard."""
    start_time = time.time()
    raw_text = pyperclip.paste()

    if not raw_text or not raw_text.strip():
        print("\n\U0001f4cb Clipboard is empty! Copy some text first.")
        return

    print("\n" + "=" * 60)
    print("\u26a1 [Clipboard Copilot] Processing clipboard text...")
    print(f"\U0001f4e5 Original: {raw_text}")

    corrected = correct_text(raw_text)
    latency_ms = (time.time() - start_time) * 1000

    pyperclip.copy(corrected)

    print(f"\u2728 Corrected: {corrected}")
    print(f"\u23f1\ufe0f Latency:   {latency_ms:.1f} ms | Status: Clipboard Updated!")
    print("=" * 60 + "\n")


def _interactive_loop() -> None:
    """Run the enter-key driven interactive fallback loop."""
    while True:
        user_cmd = input(
            "\nPress Enter to fix current clipboard text (or 'exit' to quit): "
        ).strip()
        if user_cmd.lower() in ["exit", "quit", "q"]:
            break
        process_clipboard()


def main() -> None:
    """Entry point: print the banner and start the preferred listener."""
    print("\n" + "=" * 56)
    print(" \U0001f4cb Microsoft Foundry Offline Clipboard Copilot")
    print("=" * 56)
    if HAS_FOUNDRY_SDK:
        print(" \U0001f7e2 Active Engine : Microsoft Foundry Local SDK")
        print(" \U0001f680 Superpowers   : Zero HTTP Overhead | Auto-NPU Acceleration")
    else:
        print(" \U0001f7e2 Active Engine : Ollama Local HTTP Daemon")
    print(" \U0001f512 Privacy       : 100% On-Device Offline")
    print(" \u2328\ufe0f  Hotkey Hook   : Press [Ctrl + Alt + G] anywhere to fix clipboard")
    print(" \U0001f449 Press Ctrl+C in terminal to exit")
    print("=" * 56 + "\n")

    if HAS_KEYBOARD:
        try:
            keyboard.add_hotkey("ctrl+alt+g", process_clipboard)
            print("Listening for [Ctrl + Alt + G]... (Press Ctrl+C to stop)")
            keyboard.wait()
        except Exception as e:
            print(f"\u26a0\ufe0f Keyboard hook warning: {e}")
            print(
                "Running in interactive mode. Press Enter to trigger clipboard "
                "fix, or 'exit' to quit:"
            )
            _interactive_loop()
    else:
        print("Running in interactive CLI mode (keyboard hook unavailable).")
        _interactive_loop()
