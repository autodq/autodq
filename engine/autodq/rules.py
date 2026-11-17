"""Learn candidate rules on a discovery split and characterize them on held-out rows."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from hashlib import sha256
from random import Random

from .models import (
    Bins, CategoryBins, DriftSpec, FitConfig, Kind, MissingSpec, NumericBins, RangeSpec,
    RateReference, RateSpec, Rule, RuleBook, SetSpec, Spec, Status, TypeSpec, UniqueSpec,
)
from .profiling import infer_type, numbers, profile, quantiles
from .statistics import bin_counts, count_violations, coverage_lower
from .table import Cell, Table

DISCOVERY_ONLY = RateReference(trials=1, violations=0, coverage_lower_95=0)


def create_rule(column: str, spec: Spec, reason: str) -> Rule:
    identifier = sha256((spec.kind + "\0" + column).encode()).hexdigest()[:16]
    return Rule(id=identifier, column=column, spec=spec, reason=reason)


def calibrate(cells: Sequence[Cell], spec: RateSpec, config: FitConfig) -> RateSpec | None:
    trials, violations = count_violations(cells, spec)
    if trials < config.min_observations:
        return None
    lower = coverage_lower(trials - violations, trials)
    if not isinstance(spec, MissingSpec) and lower < config.min_coverage_lower:
        return None
    evidence = RateReference(trials=trials, violations=violations, coverage_lower_95=lower)
    return spec.model_copy(update={"reference": evidence})


def candidates(
    column: str, train: Sequence[Cell], validation: Sequence[Cell], config: FitConfig,
) -> Iterable[Rule]:
    observed = [value for value in train if value is not None]
    held_out = [value for value in validation if value is not None]
    kind, _ = infer_type(observed, config.min_type_share)
    frequency = Counter(observed)
    baseline: list[tuple[RateSpec, str]] = []
    if observed or held_out:
        baseline.append((MissingSpec(reference=DISCOVERY_ONLY), "Track increases in the share of missing values."))
    identifier = column.casefold() in {"id", "uuid"} or column.casefold().endswith(("_id", "_uuid"))
    bins: Bins | None = None
    if len(observed) >= config.min_observations and kind not in {Kind.EMPTY, Kind.TEXT}:
        baseline.append((TypeSpec(expected=kind, reference=DISCOVERY_ONLY), "Logical type inferred on discovery rows."))
    if not identifier and kind in {Kind.INTEGER, Kind.NUMBER}:
        numeric = numbers(observed)
        # Floating-point histograms are unsuitable for integer identifier precision beyond 2**53.
        if len(numeric) >= config.min_observations and (kind is Kind.NUMBER or max(map(abs, numeric)) < 2**53):
            lower, upper = quantiles(numeric, (config.range_tail, 1 - config.range_tail))
            baseline.append((
                RangeSpec(lower=lower, upper=upper, reference=DISCOVERY_ONLY),
                "Bounds learned from the empirical discovery quantiles.",
            ))
            cuts = tuple(sorted(set(quantiles(
                numeric, [index / config.numeric_bins for index in range(1, config.numeric_bins)]
            ))))
            bins = NumericBins(cutpoints=cuts)
    elif not identifier and len(observed) >= config.min_observations and 1 <= len(frequency) <= config.max_categories:
        vocabulary = tuple(sorted(frequency))
        baseline.append((
            SetSpec(allowed=vocabulary, reference=DISCOVERY_ONLY),
            "Low-cardinality vocabulary learned on discovery rows.",
        ))
        bins = CategoryBins(vocabulary=vocabulary)

    for spec, reason in baseline:
        if (fitted := calibrate(validation, spec, config)) is not None:
            yield create_rule(column, fitted, reason)

    if identifier and len(observed) >= config.min_observations and len(held_out) >= config.min_observations:
        observed_values, held_out_values = set(observed), set(held_out)
        if (
            len(observed_values) == len(observed) and len(held_out_values) == len(held_out)
            and observed_values.isdisjoint(held_out_values)
        ):
            yield create_rule(
                column, UniqueSpec(reference_rows=len(observed) + len(held_out)),
                "Every non-missing value is distinct across both reference splits.",
            )
    if bins is not None:
        counts = bin_counts(validation, bins)
        if sum(counts) >= config.min_observations:
            yield create_rule(
                column, DriftSpec(bins=bins, reference_counts=counts),
                "Discovery bins are fixed; held-out counts are the comparison baseline.",
            )


def fit(table: Table, config: FitConfig | None = None) -> RuleBook:
    config = config or FitConfig()
    size = table.row_count
    if size < 2 * config.min_observations:
        raise ValueError(f"At least {2 * config.min_observations} reference rows are required")
    calibration_size = min(
        size - config.min_observations,
        max(config.min_observations, round(size * config.calibration_fraction)),
    )
    indices = list(range(size))
    Random(config.seed).shuffle(indices)
    discovery, validation = table.select(indices[calibration_size:]), table.select(indices[:calibration_size])
    materialized = tuple(
        rule for column, cells in discovery.columns.items()
        for rule in candidates(column, cells, validation.columns[column], config)
    )
    return RuleBook(
        profile=profile(table, min_type_share=config.min_type_share),
        discovery_rows=discovery.row_count, calibration_rows=validation.row_count,
        config=config, rules=materialized,
    )


def review(book: RuleBook, decisions: Mapping[str, Status]) -> RuleBook:
    """Apply an explicit review decision to each listed rule ID."""
    unknown = decisions.keys() - {rule.id for rule in book.rules}
    if unknown:
        raise ValueError("Unknown rule IDs: " + ", ".join(sorted(unknown)))
    return book.model_copy(update={
        "rules": tuple(rule.model_copy(update={"status": decisions.get(rule.id, rule.status)}) for rule in book.rules),
    })
