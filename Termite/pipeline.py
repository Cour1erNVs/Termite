from __future__ import annotations

from pathlib import Path
from typing import Any

from .analyzer import analyze_file
from .deceptacons import evaluate


def run_pipeline(path: Path, strings_limit: int = 100) -> dict[str, Any]:
    analysis = analyze_file(path, strings_limit=strings_limit)
    heuristics = evaluate(analysis)

    return {
        "analysis": analysis,
        "heuristics": heuristics,
    }