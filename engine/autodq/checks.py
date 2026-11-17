"""Evaluate approved rules on an independent dataset and summarize the batch."""

from __future__ import annotations

from collections.abc import Sequence
from math import ceil
from typing import TypedDict

import numpy as np

from .models import (
    MAX_DRIFT_RESAMPLES, CheckConfig, DriftSpec, Outcome, Report, Result, Rule, RuleBook, Status, UniqueSpec,
)
from .statistics import bin_counts, count_violations, distribution_test, higher_violation_rate, holm_adjust
from .table import Cell, Table


class ResultIdentity(TypedDict):
    rule_id: str
    column: str
    kind: str


def evaluate(
    rule: Rule, cells: Sequence[Cell], config: CheckConfig,
    rng: np.random.Generator, resamples: int,
) -> Result:
    spec = rule.spec
    identity: ResultIdentity = {"rule_id": rule.id, "column": rule.column, "kind": spec.kind}

    if isinstance(spec, UniqueSpec):
        observed = [value for value in cells if value is not None]
        trials = len(observed)
        if trials < config.min_observations:
            return Result(**identity, outcome=Outcome.SKIP, observations=trials, reason="Too few non-missing observations.")
        duplicates = trials - len(set(observed))
        rate = duplicates / trials
        failed = rate > spec.max_duplicate_share
        return Result(
            **identity, outcome=Outcome.FAIL if failed else Outcome.PASS,
            observations=trials, violations=duplicates, rate=rate,
            reason="Duplicate share exceeds the configured limit." if failed else "Duplicate share within the configured limit.",
        )

    if isinstance(spec, DriftSpec):
        counts = bin_counts(cells, spec.bins)
        trials = sum(counts)
        if min(trials, sum(spec.reference_counts)) < config.min_observations:
            return Result(
                **identity, outcome=Outcome.SKIP, observations=trials, current_counts=counts,
                reason="Too few observations in one of the two histograms.",
            )
        distance, p_value = distribution_test(spec.reference_counts, counts, resamples=resamples, rng=rng)
        return Result(
            **identity, outcome=Outcome.PASS, observations=trials, current_counts=counts,
            effect=distance, p_value=p_value, reason="Compared fixed-bin distributions.",
        )

    trials, violations = count_violations(cells, spec)
    if min(trials, spec.reference.trials) < config.min_observations:
        return Result(
            **identity, outcome=Outcome.SKIP, observations=trials, violations=violations,
            reason="Too few comparable observations.",
        )
    rate = violations / trials
    baseline = spec.reference.violations / spec.reference.trials
    return Result(
        **identity, outcome=Outcome.PASS, observations=trials, violations=violations,
        rate=rate, reference_rate=baseline, effect=rate - baseline,
        p_value=higher_violation_rate(trials, violations, spec.reference),
        reason="Compared the violation rates.",
    )


def decide(result: Result, adjusted_p: float, config: CheckConfig) -> Result:
    threshold = config.min_js_distance if result.kind == "drift" else config.min_rate_increase
    material = result.effect is not None and result.effect > 0 and result.effect >= threshold
    if material and adjusted_p <= config.alpha:
        outcome, reason = Outcome.FAIL, "Material change supported after Holm correction."
    elif material:
        outcome, reason = Outcome.WARN, "Material observed change with insufficient statistical evidence."
    else:
        outcome, reason = Outcome.PASS, "Observed change below the practical threshold."
    return result.model_copy(update={"outcome": outcome, "reason": reason, "adjusted_p_value": adjusted_p})


def check(table: Table, book: RuleBook, config: CheckConfig | None = None) -> Report:
    config = config or CheckConfig()
    expected = {col.name for col in book.profile.columns}
    missing = tuple(sorted(expected - table.columns.keys()))
    extra = tuple(sorted(table.columns.keys() - expected))
    active = tuple(rule for rule in book.rules if rule.status is Status.APPROVED)
    rng = np.random.default_rng(config.seed)
    needed = min(MAX_DRIFT_RESAMPLES, len(active) / config.alpha)
    resamples = max(config.drift_resamples, ceil(needed))
    results = []
    for rule in active:
        cells = table.columns.get(rule.column)
        if cells is None:
            result = Result(
                rule_id=rule.id, column=rule.column, kind=rule.spec.kind, outcome=Outcome.SKIP,
                reason="Required column is missing.",
            )
        else:
            result = evaluate(rule, cells, config, rng, resamples)
        results.append(result)
    corrected = holm_adjust({result.rule_id: result.p_value for result in results if result.p_value is not None})
    finalized = tuple(
        decide(result, corrected[result.rule_id], config) if result.rule_id in corrected else result
        for result in results
    )
    assessed = tuple(result for result in finalized if result.outcome is not Outcome.SKIP)
    outcomes = {result.outcome for result in assessed}
    if missing or Outcome.FAIL in outcomes:
        outcome = Outcome.FAIL
    elif not assessed:
        outcome = Outcome.SKIP
    elif extra or Outcome.WARN in outcomes or len(assessed) < len(active):
        outcome = Outcome.WARN
    else:
        outcome = Outcome.PASS
    passing = sum(result.outcome is Outcome.PASS for result in assessed)
    return Report(
        outcome=outcome, rows=table.row_count, missing_columns=missing, extra_columns=extra,
        eligible_rules=len(active), evaluated_rules=len(assessed),
        quality_score=round(100 * passing / len(assessed), 2) if assessed else None,
        rule_coverage=len(assessed) / len(active) if active else None,
        config=config, results=finalized,
    )
