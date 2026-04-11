from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from .utils import (
    file_size_human,
    get_extension,
    hash_bytes,
    is_probably_text,
    read_bytes,
    safe_decode,
)

PRINTABLE_STRINGS_RE = re.compile(rb"[\x20-\x7e]{4,}")


def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0

    freq = [0] * 256
    for byte in data:
        freq[byte] += 1

    entropy = 0.0
    data_len = len(data)
    for count in freq:
        if count == 0:
            continue
        probability = count / data_len
        entropy -= probability * math.log2(probability)

    return round(entropy, 4)


def extract_strings(data: bytes, min_length: int = 4, limit: int = 100) -> list[str]:
    strings = []
    for match in PRINTABLE_STRINGS_RE.finditer(data):
        s = match.group().decode("utf-8", errors="replace")
        if len(s) >= min_length:
            strings.append(s)
        if len(strings) >= limit:
            break
    return strings


def guess_file_type(path: Path, data: bytes) -> str:
    ext = get_extension(path)

    if data.startswith(b"MZ"):
        return "PE/Windows executable"
    if data.startswith(b"\x7fELF"):
        return "ELF/Linux executable"
    if data.startswith(b"%PDF"):
        return "PDF document"
    if data.startswith(b"PK\x03\x04"):
        return "ZIP-based archive/document"
    if is_probably_text(data[:4096]):
        if ext in {".py"}:
            return "Python source"
        if ext in {".js"}:
            return "JavaScript source"
        if ext in {".ps1"}:
            return "PowerShell script"
        if ext in {".txt", ".log", ".md"}:
            return "Text file"
        return "Probable text file"

    return "Unknown/binary"


def collect_basic_metadata(path: Path, data: bytes) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": str(path),
        "name": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "size_human": file_size_human(stat.st_size),
        "file_type_guess": guess_file_type(path, data),
        "hashes": hash_bytes(data),
        "entropy": calculate_entropy(data),
    }


def analyze_file(path: Path, strings_limit: int = 100) -> dict[str, Any]:
    data = read_bytes(path)
    metadata = collect_basic_metadata(path, data)

    text_preview = ""
    if is_probably_text(data[:4096]):
        text_preview = safe_decode(data[:2000])

    return {
        "metadata": metadata,
        "strings": extract_strings(data, limit=strings_limit),
        "text_preview": text_preview,
    }