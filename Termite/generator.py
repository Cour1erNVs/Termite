from __future__ import annotations

from pathlib import Path

from .utils import write_text_file


SAFE_SAMPLE_TEXT = """\
This is a safe synthetic analysis sample.
It includes test strings for parser validation only.

Examples:
- socket
- subprocess
- powershell
- systemd
- base64

This file is not executable and is intended for detection testing.
"""


def generate_sample_file(output_path: str) -> Path:
    path = Path(output_path).expanduser().resolve()
    write_text_file(path, SAFE_SAMPLE_TEXT)
    return path