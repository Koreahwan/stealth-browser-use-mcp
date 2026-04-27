"""Patchright patched Chromium binary management."""

import sys
import subprocess
from pathlib import Path

_cached_path: str | None = None


def ensure_chromium() -> None:
    """Install Patchright's patched Chromium if not already present."""
    subprocess.run(
        [sys.executable, "-m", "patchright", "install", "chromium"],
        check=True,
    )


def chromium_path() -> str:
    """Return the absolute path to Patchright's patched Chromium binary.

    Installs automatically on first call if the binary is missing.
    """
    global _cached_path
    if _cached_path and Path(_cached_path).exists():
        return _cached_path

    try:
        path = _resolve_path()
    except (OSError, RuntimeError):
        ensure_chromium()
        path = _resolve_path()

    if not Path(path).exists():
        ensure_chromium()
        path = _resolve_path()

    if not Path(path).exists():
        raise FileNotFoundError(
            f"Patchright Chromium not found at {path}. "
            "Run: patchright install chromium"
        )

    _cached_path = path
    return path


def _resolve_path() -> str:
    from patchright.sync_api import sync_playwright

    with sync_playwright() as p:
        return p.chromium.executable_path
