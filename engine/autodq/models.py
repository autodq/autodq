"""Versioned contracts for profiles, rule books and analysis results."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat, model_validator

Probability = Annotated[FiniteFloat, Field(ge=0, le=1)]
Count = Annotated[int, Field(ge=0)]
PositiveCount = Annotated[int, Field(gt=0)]
MAX_DRIFT_RESAMPLES = 200_000


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class Kind(StrEnum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"
    DATE = "date"
    DATETIME = "datetime"
    TEXT = "text"
    EMPTY = "empty"


class Status(StrEnum):
    SUGGESTED = "suggested"
    APPROVED = "approved"
    REJECTED = "rejected"


class Outcome(StrEnum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIP = "skip"


class NumericSummary(Model):
    minimum: FiniteFloat
    maximum: FiniteFloat
    median: FiniteFloat
    q01: FiniteFloat
    q25: FiniteFloat
    q75: FiniteFloat
    q99: FiniteFloat
    mad: FiniteFloat | None


class ColumnProfile(Model):
    name: str
    kind: Kind
    missing: Count
    non_null: Count
    distinct: Count
    type_matches: Count
    top_values: tuple[tuple[str, PositiveCount], ...]
    numeric: NumericSummary | None = None


class DatasetProfile(Model):
    rows: Count
    columns: tuple[ColumnProfile, ...]


class RateReference(Model):
    trials: PositiveCount
    violations: Count
    coverage_lower_95: Probability

    @model_validator(mode="after")
    def check_counts(self) -> Self:
        if self.violations > self.trials:
            raise ValueError("Violations cannot exceed trials")
        return self


class MissingSpec(Model):
    kind: Literal["missing"] = "missing"
    reference: RateReference


class TypeSpec(Model):
    kind: Literal["type"] = "type"
    expected: Kind
    reference: RateReference


class RangeSpec(Model):
    kind: Literal["range"] = "range"
    lower: FiniteFloat
    upper: FiniteFloat
    reference: RateReference

    @model_validator(mode="after")
    def check_bounds(self) -> Self:
        if self.lower > self.upper:
            raise ValueError("Lower bound exceeds upper bound")
        return self


class SetSpec(Model):
    kind: Literal["in_set"] = "in_set"
    allowed: tuple[str, ...] = Field(min_length=1)
    reference: RateReference


class UniqueSpec(Model):
    kind: Literal["unique"] = "unique"
    reference_rows: PositiveCount
    max_duplicate_share: Probability = 0


class NumericBins(Model):
    kind: Literal["numeric"] = "numeric"
    cutpoints: tuple[FiniteFloat, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def check_order(self) -> Self:
        if any(a >= b for a, b in zip(self.cutpoints, self.cutpoints[1:])):
            raise ValueError("Cutpoints must be strictly increasing")
        return self


class CategoryBins(Model):
    kind: Literal["categorical"] = "categorical"
    vocabulary: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def check_unique(self) -> Self:
        if len(set(self.vocabulary)) != len(self.vocabulary):
            raise ValueError("Vocabulary entries must be unique")
        return self


Bins = Annotated[NumericBins | CategoryBins, Field(discriminator="kind")]


class DriftSpec(Model):
    kind: Literal["drift"] = "drift"
    bins: Bins
    reference_counts: tuple[Count, ...]

    @model_validator(mode="after")
    def check_counts(self) -> Self:
        labels = self.bins.cutpoints if isinstance(self.bins, NumericBins) else self.bins.vocabulary
        if len(self.reference_counts) != len(labels) + 1 or sum(self.reference_counts) == 0:
            raise ValueError("Reference histogram must include a count for every bin")
        return self


RateSpec = MissingSpec | TypeSpec | RangeSpec | SetSpec
Spec = Annotated[RateSpec | UniqueSpec | DriftSpec, Field(discriminator="kind")]


class Rule(Model):
    id: str
    column: str
    status: Status = Status.SUGGESTED
    reason: str
    spec: Spec


class FitConfig(Model):
    seed: Count = 42
    calibration_fraction: Annotated[FiniteFloat, Field(gt=0, lt=1)] = 0.30
    min_observations: Annotated[int, Field(ge=10)] = 30
    min_type_share: Annotated[FiniteFloat, Field(gt=0, le=1)] = 0.98
    min_coverage_lower: Probability = 0.85
    range_tail: Annotated[FiniteFloat, Field(gt=0, lt=0.5)] = 0.01
    max_categories: Annotated[int, Field(ge=2, le=100)] = 16
    numeric_bins: Annotated[int, Field(ge=2, le=100)] = 10


class RuleBook(Model):
    version: Literal[1] = 1
    profile: DatasetProfile
    discovery_rows: Count
    calibration_rows: Count
    config: FitConfig
    rules: tuple[Rule, ...]

    @model_validator(mode="after")
    def check_integrity(self) -> Self:
        if self.discovery_rows + self.calibration_rows != self.profile.rows:
            raise ValueError("Discovery and calibration must account for all reference rows")
        if len({rule.id for rule in self.rules}) != len(self.rules):
            raise ValueError("Duplicate rule ID")
        columns = {column.name for column in self.profile.columns}
        if any(rule.column not in columns for rule in self.rules):
            raise ValueError("Rule references an unknown column")
        return self


class CheckConfig(Model):
    alpha: Annotated[FiniteFloat, Field(gt=0, lt=1)] = 0.05
    min_observations: Annotated[int, Field(ge=10)] = 30
    min_rate_increase: Probability = 0.02
    min_js_distance: Probability = 0.10
    drift_resamples: Annotated[int, Field(ge=99, le=MAX_DRIFT_RESAMPLES)] = 1999
    seed: Count = 42


class Result(Model):
    rule_id: str
    column: str
    kind: str
    outcome: Outcome
    observations: Count = 0
    violations: Count | None = None
    rate: Probability | None = None
    reference_rate: Probability | None = None
    effect: FiniteFloat | None = None
    p_value: Probability | None = None
    adjusted_p_value: Probability | None = None
    current_counts: tuple[Count, ...] | None = None
    reason: str


class Report(Model):
    version: Literal[1] = 1
    outcome: Outcome
    rows: Count
    missing_columns: tuple[str, ...]
    extra_columns: tuple[str, ...]
    eligible_rules: Count
    evaluated_rules: Count
    quality_score: Annotated[FiniteFloat, Field(ge=0, le=100)] | None
    rule_coverage: Probability | None
    config: CheckConfig
    results: tuple[Result, ...]
