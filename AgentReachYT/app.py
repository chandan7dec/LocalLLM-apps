"""Streamlit entry point for the YouTube-to-Blog SEO Engine."""

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from agentreachyt.ui import render

if __name__ == "__main__":
    render()
