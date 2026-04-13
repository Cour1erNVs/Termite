from __future__ import annotations

from typing import Any


def render_markdown_report(result: dict[str, Any]) -> str:
    metadata = result["analysis"]["metadata"]
    heuristics = result["heuristics"]

    lines: list[str] = []
    lines.append(f"# Termite Report: {metadata['name']}")
    lines.append("")
    lines.append("## File Metadata")
    lines.append(f"- Path: `{metadata['path']}`")
    lines.append(f"- Type Guess: {metadata['file_type_guess']}")
    lines.append(f"- Size: {metadata['size_human']} ({metadata['size_bytes']} bytes)")
    lines.append(f"- Entropy: {metadata['entropy']}")
    lines.append("")
    lines.append("## Hashes")
    lines.append(f"- MD5: `{metadata['hashes']['md5']}`")
    lines.append(f"- SHA1: `{metadata['hashes']['sha1']}`")
    lines.append(f"- SHA256: `{metadata['hashes']['sha256']}`")
    lines.append("")
    lines.append("## Heuristic Assessment")
    lines.append(f"- Risk: **{heuristics['risk'].upper()}**")
    lines.append(f"- Total Score: {heuristics['total_score']}")
    lines.append(f"- Entropy Label: {heuristics['entropy_assessment']['label']}")
    lines.append(f"- Entropy Note: {heuristics['entropy_assessment']['reason']}")
    lines.append("")

    findings = heuristics["string_assessment"]["findings"]
    lines.append("## String-Based Findings")
    if not findings:
        lines.append("- No notable string matches found.")
    else:
        for category, matches in findings.items():
            lines.append(f"- **{category}**")
            for item in matches[:5]:
                lines.append(f"  - `{item}`")

    strings = result["analysis"].get("strings", [])
    lines.append("")
    lines.append("## Extracted Strings Sample")
    if not strings:
        lines.append("- No printable strings extracted.")
    else:
        for s in strings[:20]:
            lines.append(f"- `{s}`")

    preview = result["analysis"].get("text_preview", "")
    if preview:
        lines.append("")
        lines.append("## Text Preview")
        lines.append("```text")
        lines.append(preview[:1000])
        lines.append("```")

    return "\n".join(lines)


def render_terminal_summary(result: dict[str, Any]) -> str:
    metadata = result["analysis"]["metadata"]
    heuristics = result["heuristics"]

    return (
        f"[Termite] {metadata['name']}\n"
        f"Type: {metadata['file_type_guess']}\n"
        f"Size: {metadata['size_human']}\n"
        f"Entropy: {metadata['entropy']}\n"
        f"Risk: {heuristics['risk'].upper()} "
        f"(score={heuristics['total_score']})\n"
        f"SHA256: {metadata['hashes']['sha256']}"
    )


def get_banner() -> str:
    return r"""
████████╗███████╗██████╗ ███╗   ███╗██╗████████╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║╚══██╔══╝██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║   █████╗  
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║   ██╔══╝  
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║   ██║   ███████╗
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚══════╝

        Termite v0.1.0  |  File Analysis Toolkit
    """