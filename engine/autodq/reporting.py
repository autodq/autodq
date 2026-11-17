"""Portable JSON artifacts and a standalone HTML analysis report."""

from __future__ import annotations

from html import escape
from pathlib import Path
from tempfile import NamedTemporaryFile

from .models import Model, Report


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(text)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_json(path: Path, model: Model) -> None:
    write_text(path, model.model_dump_json(indent=2) + "\n")


def render_html(report: Report) -> str:
    def value(number: float | int | None) -> str:
        return f"{number:.4g}" if number is not None else "—"

    def cell(text: str) -> str:
        return "<td>" + escape(text) + "</td>"

    rows = "".join("<tr>" + "".join(map(cell, (
        item.column, item.kind, item.outcome.value, str(item.observations),
        value(item.rate), value(item.reference_rate), value(item.effect),
        value(item.adjusted_p_value), item.reason,
    ))) + "</tr>" for item in report.results)
    missing = escape(", ".join(report.missing_columns) or "—")
    extra = escape(", ".join(report.extra_columns) or "—")
    coverage = value(100 * report.rule_coverage if report.rule_coverage is not None else None)
    return f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>AutoDQ · Quality report</title>
<style>
body{{font:16px/1.5 system-ui,sans-serif;background:#f4f4f0;color:#0e0f12;margin:0}}
main{{max-width:1200px;margin:auto;padding:32px 18px}}
header{{background:#0e0f12;color:#f4f4f0;padding:20px 24px;border-radius:12px}}
header strong{{color:#c9ec5f}} .results{{overflow:auto}}
table{{width:100%;border-collapse:collapse;background:white;text-align:left}}
th,td{{padding:10px;border-bottom:1px solid #e4e4de}} td{{vertical-align:top}}
@media print{{body{{background:white}} main{{max-width:none;padding:0}} tr{{break-inside:avoid}}}}
</style>
<main><header><h1>AutoDQ quality report</h1><p>Outcome <strong>{report.outcome.value.upper()}</strong></p></header>
<p>Rows {report.rows} · Evaluated {report.evaluated_rules}/{report.eligible_rules} approved rules
· Coverage {coverage}% · Score {value(report.quality_score)}/100</p>
<p>Missing columns {missing} · Extra columns {extra}</p>
<div class="results"><table><thead><tr><th>Column</th><th>Rule</th><th>Outcome</th><th>Observations</th>
<th>Rate</th><th>Reference</th><th>Effect</th><th>Adjusted p</th><th>Reason</th></tr></thead>
<tbody>{rows}</tbody></table></div></main></html>
"""
