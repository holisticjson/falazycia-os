"""
Video Editor Plugin for Hermes Agentic OS.
Handles trimming, sub-clipping, subtitles, and b-roll via MoviePy.
"""

from typing import Any

def register(ctx: Any) -> None:
    """Register tools for the Video Editor."""
    from .tools import register_tools
    register_tools(ctx)
