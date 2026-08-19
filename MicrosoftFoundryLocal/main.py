"""Backward-compatible entry point.

The application now lives in the ``clipboard_copilot`` package
(``src/clipboard_copilot``). Run either:

    python -m clipboard_copilot
    clipboard-copilot      (console script, after install)

This shim keeps ``python main.py`` working for existing workflows.
"""

from clipboard_copilot.app import main

if __name__ == "__main__":
    main()
