#!/usr/bin/env python3
"""
SuperClaude Framework Management Hub
Unified entry point for all SuperClaude operations

Usage:
    SuperClaude install [options]
    SuperClaude update [options]
    SuperClaude uninstall [options]
    SuperClaude backup [options]
    SuperClaude --help
"""

from pathlib import Path

# Read version from VERSION file
try:
    __version__ = (Path(__file__).parent.parent / "VERSION").read_text().strip()
except Exception:
    __version__ = "4.0.9"  # Fallback
__author__ = "NomenAK, Mithun Gowda B"
__email__ = "anton.knoery@gmail.com"
__license__ = "MIT"
