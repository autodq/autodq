"""Infer logical types and summarize observed distributions."""

from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Sequence
from datetime import date, datetime

import numpy as np

from .models import ColumnProfile, DatasetProfile, Kind, NumericSummary
from .table import Cell, Table

INTEGER = re.compile(r"[+-]?(?:0|[1-9][0-9]*)")
NUMBER = re.compile(r"[+-]?(?:(?:0|[1-9][0-9]*)(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
DATETIME = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}.*")
TYPE_ORDER = (Kind.BOOLEAN, Kind.INTEGER, Kind.NUMBER, Kind.DATE, Kind.DATETIME)


def parse_number(value: str) -> float | None:
    text = value.strip()
    if NUMBER.fullmatch(text) is None:
        return None
    parsed = float(text)
    return parsed if math.isfinite(parsed) else None


def matches_type(value: str, kind: Kind) -> bool:
    text = value.strip()
    if kind is Kind.BOOLEAN:
        return text.casefold() in {"true", "false"}
    if kind is Kind.INTEGER:
        return INTEGER.fullmatch(text) is not None and parse_number(text) is not None
    if kind is Kind.NUMBER:
        return parse_number(text) is not None
    if kind is Kind.DATE and DATE.fullmatch(text):
        try:
            date.fromisoformat(text)
        except ValueError:
            return False
        return True
    if kind is Kind.DATETIME and DATETIME.fullmatch(text):
        try:
            datetime.fromisoformat(text)
        except ValueError:
            return False
        return True
    return kind is Kind.TEXT


def infer_type(values: Sequence[str], minimum_share: float) -> tuple[Kind, int]:
    if not values:
        return Kind.EMPTY, 0
    for kind in TYPE_ORDER:
        matched = sum(matches_type(value, kind) for value in values)
        if matched / len(values) >= minimum_share and matched > 0:
            return kind, matched
    return Kind.TEXT, len(values)


def numbers(values: Sequence[Cell]) -> list[float]:
    return [
        number for value in values
        if value is not None and (number := parse_number(value)) is not None
    ]


def quantiles(values: Sequence[float], probabilities: Sequence[float]) -> tuple[float, ...]:
    return tuple(float(value) for value in np.quantile(values, probabilities, method="inverted_cdf"))


def summarize_numbers(values: Sequence[float]) -> NumericSummary:
    q01, q25, median, q75, q99 = quantiles(values, (0.01, 0.25, 0.5, 0.75, 0.99))
    mad, = quantiles([abs(value - median) for value in values], (0.5,))
    return NumericSummary(
        minimum=min(values), maximum=max(values), median=median, q01=q01,
        q25=q25, q75=q75, q99=q99, mad=mad if math.isfinite(mad) else None,
    )


def profile(table: Table, *, min_type_share: float = 0.98) -> DatasetProfile:
    """Describe every column, including columns made entirely of missing values."""
    if not 0 < min_type_share <= 1:
        raise ValueError("min_type_share must be in (0, 1]")
    columns = []
    for name, cells in table.columns.items():
        observed = [cell for cell in cells if cell is not None]
        counts = Counter(observed)
        kind, type_matches = infer_type(observed, min_type_share)
        numeric = summarize_numbers(numbers(observed)) if kind in {Kind.INTEGER, Kind.NUMBER} else None
        top = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:10]
        columns.append(ColumnProfile(
            name=name, kind=kind, missing=table.row_count - len(observed), non_null=len(observed),
            distinct=len(counts), type_matches=type_matches, top_values=tuple(top), numeric=numeric,
        ))
    return DatasetProfile(rows=table.row_count, columns=tuple(columns))
