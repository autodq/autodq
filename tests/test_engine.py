from pathlib import Path

import pytest

from autodq import check, fit, profile, review
from autodq.models import CheckConfig, FitConfig, Kind, Outcome, RuleBook, Status
from autodq.reporting import render_html
from autodq.statistics import coverage_lower, holm_adjust
from autodq.table import Table, read_csv


def snapshot(*, shifted: bool = False, offset: int = 0) -> Table:
    return Table.from_rows(["order_id", "amount", "category", "date"], (
        (str(offset + (index // 2 if shifted else index)),
         None if shifted and index % 4 == 0 else str(index % 30 + (100 if shifted else 0)),
         ("new" if index % 2 else "old") if not shifted else "unexpected",
         "2026-10-03")
        for index in range(600)
    ))


def test_fit_serialization_review_and_independent_check() -> None:
    book = fit(snapshot(), FitConfig(seed=24))
    assert book == fit(snapshot(), FitConfig(seed=24))
    assert (book.discovery_rows, book.calibration_rows) == (420, 180)
    assert book == RuleBook.model_validate_json(book.model_dump_json())
    assert check(snapshot(offset=600), book).outcome is Outcome.SKIP
    assert {rule.spec.kind for rule in book.rules if rule.column == "order_id"} == {"unique", "missing", "type"}
    approved = review(book, {rule.id: Status.APPROVED for rule in book.rules})
    stable = check(snapshot(offset=600), approved)
    assert stable.outcome is Outcome.PASS
    assert stable.quality_score == 100
    report = check(snapshot(shifted=True, offset=1200), approved)
    assert report.outcome is Outcome.FAIL
    failures = {(result.column, result.kind) for result in report.results if result.outcome is Outcome.FAIL}
    assert {("amount", "drift"), ("amount", "missing"), ("amount", "range"),
            ("category", "in_set"), ("category", "drift"), ("order_id", "unique")} <= failures
    assert report == check(snapshot(shifted=True, offset=1200), approved)
    assert report.rule_coverage == 1


def test_missing_columns_small_samples_and_review_errors() -> None:
    book = fit(snapshot())
    approved = review(book, {rule.id: Status.APPROVED for rule in book.rules})
    removed = check(Table.from_rows(["order_id"], [["1"], ["2"]]), approved)
    assert removed.outcome is Outcome.FAIL
    assert removed.missing_columns == ("amount", "category", "date")
    assert removed.quality_score is None
    empty = check(Table.from_rows(list(snapshot().columns), []), approved, CheckConfig(min_observations=10))
    assert empty.outcome is Outcome.SKIP
    assert empty.rule_coverage == 0
    with pytest.raises(ValueError, match="Unknown rule IDs"):
        review(book, {"no-such-rule": Status.APPROVED})
    with pytest.raises(ValueError, match="reference rows"):
        fit(Table.from_rows(["id"], [["1"]]))


def test_profile_and_csv_edge_cases(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    path.write_text("key,empty,date,value\n001, ,2026-11-17,2\n002,,2026-11-18,4\n", encoding="utf-8-sig")
    columns = profile(read_csv(path)).columns
    assert [column.kind for column in columns] == [Kind.TEXT, Kind.EMPTY, Kind.DATE, Kind.INTEGER]
    assert columns[1].missing == 2
    assert columns[-1].numeric is not None
    assert columns[-1].numeric.maximum == 4
    path.write_text("key,empty\n1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected 2 fields"):
        read_csv(path)
    with pytest.raises(ValueError, match="Duplicate"):
        Table.from_rows(["id", " id "], [])


def test_statistics_and_escaping() -> None:
    assert coverage_lower(100, 100) == pytest.approx(0.97366, rel=1e-4)
    assert holm_adjust({"a": 0.01, "b": 0.03, "c": 0.04}) == pytest.approx({"a": 0.03, "b": 0.06, "c": 0.06})
    book = fit(Table.from_rows(["<script>"], [["x"]] * 80))
    report = check(Table.from_rows(["other"], [["x"]] * 80), book)
    assert "&lt;script&gt;" in render_html(report)
