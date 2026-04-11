from __future__ import annotations

import hashlib
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Iterable


def setup_logger(debug: bool = False) -> logging.Logger:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )
    return logging.getLogger("termite")


def validate_file(path: str) -> Path:
    file_path = Path(path).expanduser().resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    return file_path


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def chunk_bytes(data: bytes, chunk_size: int = 4096) -> Iterable[bytes]:
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def hash_bytes(data: bytes) -> dict[str, str]:
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def file_size_human(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{size} B"


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def safe_decode(data: bytes, encoding: str = "utf-8") -> str:
    return data.decode(encoding, errors="replace")


def ensure_output_dir(path: str | None) -> Path | None:
    if not path:
        return None
    out_dir = Path(path).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def write_text_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def get_extension(path: Path) -> str:
    return path.suffix.lower()


def is_probably_text(data: bytes, threshold: float = 0.85) -> bool:
    if not data:
        return True
    printable = sum(32 <= b <= 126 or b in (9, 10, 13) for b in data)
    return (printable / len(data)) >= threshold