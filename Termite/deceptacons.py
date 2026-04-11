from __future__ import annotations

import re
from typing import Any

SUSPICIOUS_PATTERNS: dict[str, list[str]] = {
    "networking_terms": [
        r"\bsocket\b",
        r"\bconnect\b",
        r"\bhttp\b",
        r"\bhttps\b",
        r"\bftp\b",
        r"\buser-agent\b",
    ],
    "process_execution": [
        r"\bsubprocess\b",
        r"\bos\.system\b",
        r"\bcmd\.exe\b",
        r"\bpowershell\b",
        r"\bCreateProcess\b",
        r"\bShellExecute\b",
    ],
    "scripting_indicators": [
        r"\beval\b",
        r"\bexec\b",
        r"\bbase64\b",
        r"\bfromcharcode\b",
        r"\bmarshal\b",
    ],
    "persistence_keywords": [
        r"\brun key\b",
        r"\bstartup\b",
        r"\bschtasks\b",
        r"\bcron\b",
        r"\bsystemd\b",
    ],
}


def score_entropy(entropy: float) -> dict[str, Any]:
    if entropy >= 7.5:
        return {
            "label": "high",
            "score": 3,
            "reason": "Very high entropy may indicate packing, compression, or encryption."
        }
    if entropy >= 6.8:
        return {
            "label": "medium",
            "score": 2,
            "reason": "Moderately high entropy may deserve inspection."
        }
    return {
        "label": "low",
        "score": 0,
        "reason": "Entropy appears normal for many common files."
    }


def inspect_strings(strings: list[str]) -> dict[str, Any]:
    findings: dict[str, list[str]] = {}
    total_score = 0

    for category, patterns in SUSPICIOUS_PATTERNS.items():
        matches: list[str] = []
        for s in strings:
            for pattern in patterns:
                if re.search(pattern, s, flags=re.IGNORECASE):
                    matches.append(s)
                    break
        if matches:
            findings[category] = matches[:10]
            total_score += 2

    return {
        "findings": findings,
        "score": total_score,
    }


def classify_risk(total_score: int) -> str:
    if total_score >= 7:
        return "high"
    if total_score >= 3:
        return "medium"
    return "low"


def evaluate(analysis_result: dict[str, Any]) -> dict[str, Any]:
    entropy = analysis_result["metadata"]["entropy"]
    strings = analysis_result.get("strings", [])

    entropy_result = score_entropy(entropy)
    string_result = inspect_strings(strings)

    total_score = entropy_result["score"] + string_result["score"]
    risk = classify_risk(total_score)

    return {
        "risk": risk,
        "total_score": total_score,
        "entropy_assessment": entropy_result,
        "string_assessment": string_result,
    }