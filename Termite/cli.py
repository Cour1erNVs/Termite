from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich import box

from .generator import generate_sample_file
from .pipeline import run_pipeline
from .templates import (
    render_markdown_report,
    render_terminal_summary,
    get_banner,
)
from .utils import (
    ensure_output_dir,
    setup_logger,
    validate_file,
    write_text_file,
)

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="termite",
        description="Safe file analysis and triage toolkit."
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a file.")
    analyze_parser.add_argument("file", help="Path to the file to analyze.")
    analyze_parser.add_argument(
        "--strings-limit",
        type=int,
        default=100,
        help="Maximum number of extracted strings to keep."
    )
    analyze_parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format."
    )
    analyze_parser.add_argument(
        "--outdir",
        help="Optional directory to write report files into."
    )

    # sample generator
    gen_parser = subparsers.add_parser(
        "generate-sample",
        help="Generate a safe synthetic sample file."
    )
    gen_parser.add_argument(
        "--output",
        required=True,
        help="Output path for the sample file."
    )

    return parser


def print_banner():
    console.print(
        Panel.fit(
            Text(get_banner(), style="bold cyan"),
            border_style="cyan",
            box=box.DOUBLE,
        )
    )


def handle_analyze(args: argparse.Namespace) -> int:
    logger = setup_logger(args.debug)

    try:
        path = validate_file(args.file)
        result = run_pipeline(path, strings_limit=args.strings_limit)
    except Exception as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        return 1

    # Output handling
    if args.format == "json":
        console.print_json(json.dumps(result))
    elif args.format == "markdown":
        console.print(render_markdown_report(result), style="cyan")
    else:
        summary = render_terminal_summary(result)

        # Color based on risk
        risk = result["heuristics"]["risk"]
        if risk == "high":
            style = "bold red"
        elif risk == "medium":
            style = "bold yellow"
        else:
            style = "bold green"

        console.print(summary, style=style)

    # Save reports
    if args.outdir:
        outdir = ensure_output_dir(args.outdir)
        if outdir is not None:
            base_name = Path(args.file).name
            md_path = outdir / f"{base_name}.report.md"
            json_path = outdir / f"{base_name}.report.json"

            write_text_file(md_path, render_markdown_report(result))
            write_text_file(json_path, json.dumps(result, indent=2))

            console.print(f"[bold cyan]Saved reports to:[/bold cyan] {outdir}")

    return 0


def handle_generate_sample(args: argparse.Namespace) -> int:
    logger = setup_logger(args.debug)

    try:
        path = generate_sample_file(args.output)
        console.print(f"[bold green]Sample created:[/bold green] {path}")
        return 0
    except Exception as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        return 1


def main() -> int:
    print_banner()

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        return handle_analyze(args)

    if args.command == "generate-sample":
        return handle_generate_sample(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())