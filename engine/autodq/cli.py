"""Command-line entry point for reviewing and comparing CSV snapshots."""

from __future__ import annotations

import argparse
import csv
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from .checks import check
from .models import CheckConfig, FitConfig, Outcome, RuleBook, Status
from .profiling import profile
from .reporting import render_html, write_json, write_text
from .rules import fit, review
from .table import read_csv


def console(stream: TextIO, message: str) -> None:
    encoding = stream.encoding or "utf-8"
    print(message.encode(encoding, errors="backslashreplace").decode(encoding), file=stream)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="autodq")
    commands = root.add_subparsers(dest="command", required=True)

    describe = commands.add_parser("profile", help="Describe the columns in a CSV snapshot")
    discover = commands.add_parser("fit", help="Learn and calibrate a reviewable rule book")
    assess = commands.add_parser("check", help="Compare a new CSV snapshot against approved rules")
    for command in (describe, discover, assess):
        command.add_argument("csv", type=Path)
        command.add_argument("--delimiter", default=",")
        command.add_argument("-o", "--output", type=Path, required=True)
    discover.add_argument("--config", type=Path, help="JSON FitConfig")
    discover.add_argument("--approve-all", action="store_true", help="Explicitly approve all suggestions")

    approve = commands.add_parser("review", help="Approve or reject suggested rule IDs")
    approve.add_argument("rules", type=Path)
    approve.add_argument("-o", "--output", type=Path, required=True)
    approve.add_argument("--approve", action="append", default=[], metavar="RULE_ID")
    approve.add_argument("--reject", action="append", default=[], metavar="RULE_ID")
    approve.add_argument("--approve-all", action="store_true")

    assess.add_argument("--rules", type=Path, required=True)
    assess.add_argument("--config", type=Path, help="JSON CheckConfig")
    assess.add_argument("--html", type=Path)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "review":
        inputs = [args.rules]
    else:
        inputs = [args.csv, getattr(args, "config", None), getattr(args, "rules", None)]
    try:
        outputs = [args.output] + ([args.html] if getattr(args, "html", None) else [])
        if len({path.resolve() for path in outputs}) != len(outputs):
            raise ValueError("JSON and HTML destinations must be distinct")
        if not args.command == "review" and any(
            output.resolve() == source.resolve() for output in outputs for source in inputs if source is not None
        ):
            raise ValueError("An output path points to an input file")

        if args.command == "review":
            book = RuleBook.model_validate_json(args.rules.read_text(encoding="utf-8"))
            if set(args.approve) & set(args.reject):
                raise ValueError("A rule cannot be approved and rejected in the same command")
            decisions = {rule.id: Status.APPROVED for rule in book.rules if args.approve_all and rule.status is Status.SUGGESTED}
            decisions.update(dict.fromkeys(args.approve, Status.APPROVED))
            decisions.update(dict.fromkeys(args.reject, Status.REJECTED))
            if not decisions and not args.approve_all:
                raise ValueError("Provide --approve, --reject, or --approve-all")
            write_json(args.output, review(book, decisions))
            return 0

        table = read_csv(args.csv, delimiter=args.delimiter)
        if args.command == "profile":
            write_json(args.output, profile(table))
            return 0
        if args.command == "fit":
            fit_config = FitConfig.model_validate_json(args.config.read_text(encoding="utf-8")) if args.config else FitConfig()
            book = fit(table, fit_config)
            if args.approve_all:
                book = review(book, {rule.id: Status.APPROVED for rule in book.rules})
            write_json(args.output, book)
            console(sys.stdout, f"{len(book.rules)} rules written to {args.output}")
            return 0

        book = RuleBook.model_validate_json(args.rules.read_text(encoding="utf-8"))
        check_config = CheckConfig.model_validate_json(args.config.read_text(encoding="utf-8")) if args.config else CheckConfig()
        report = check(table, book, check_config)
        write_json(args.output, report)
        if args.html:
            write_text(args.html, render_html(report))
        console(sys.stdout, f"{report.outcome.value.upper()} | {report.evaluated_rules}/{report.eligible_rules} rules | {args.output}")
        return {Outcome.FAIL: 2, Outcome.SKIP: 3}.get(report.outcome, 0)
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        console(sys.stderr, f"autodq: {error}")
        return 1
