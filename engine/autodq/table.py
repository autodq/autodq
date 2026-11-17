"""Read rectangular datasets and keep the data-source boundary out of the engine."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

Cell = str | None


@dataclass(frozen=True, slots=True)
class Table:
    columns: Mapping[str, tuple[Cell, ...]]
    row_count: int

    def __post_init__(self) -> None:
        if not self.columns or any(not name.strip() for name in self.columns):
            raise ValueError("Expected at least one named column")
        if self.row_count < 0 or any(len(values) != self.row_count for values in self.columns.values()):
            raise ValueError("All columns must have the same row count")
        object.__setattr__(self, "columns", MappingProxyType(dict(self.columns)))

    @classmethod
    def from_rows(cls, header: Sequence[str], rows: Iterable[Sequence[Cell]]) -> Table:
        names = tuple(name.strip() for name in header)
        if len(set(names)) != len(names):
            raise ValueError("Duplicate column name")
        fields: list[list[Cell]] = [[] for _ in names]
        row_count = 0
        for row_count, row in enumerate(rows, start=1):
            if len(row) != len(names):
                raise ValueError(f"Data row {row_count}: expected {len(names)} fields, got {len(row)}")
            for field, value in zip(fields, row, strict=True):
                field.append(None if value is None or not value.strip() else value)
        return cls(dict(zip(names, (tuple(field) for field in fields), strict=True)), row_count)

    def select(self, indices: Sequence[int]) -> Table:
        return Table(
            {name: tuple(values[index] for index in indices) for name, values in self.columns.items()},
            len(indices),
        )


def read_csv(path: Path, *, delimiter: str = ",") -> Table:
    """Read UTF-8 CSV. Empty/whitespace fields are missing, literal 'NULL' is a value."""
    if len(delimiter) != 1:
        raise ValueError("Delimiter must be a single character")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, delimiter=delimiter, strict=True)
        header = next(reader, None)
        if header is None:
            raise ValueError("CSV must include a header")
        return Table.from_rows(header, reader)
