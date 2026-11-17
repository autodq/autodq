"""Statistical primitives used to calibrate and compare data quality rules."""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Mapping, Sequence
from math import sqrt
from statistics import NormalDist

import numpy as np
from scipy.spatial.distance import jensenshannon
from scipy.stats import fisher_exact

from .models import (
    Bins, CategoryBins, MissingSpec, NumericBins, RangeSpec, RateReference, RateSpec, SetSpec, TypeSpec,
)
from .profiling import matches_type, numbers, parse_number
from .table import Cell


def coverage_lower(successes: int, trials: int) -> float:
    """One-sided 95% Wilson lower confidence bound for binomial coverage."""
    z = NormalDist().inv_cdf(0.95)
    share = successes / trials
    scale = z * z / trials
    center = share + scale / 2
    radius = z * sqrt(share * (1 - share) / trials + scale / (4 * trials))
    return max(0.0, (center - radius) / (1 + scale))


def count_violations(cells: Sequence[Cell], spec: RateSpec) -> tuple[int, int]:
    if isinstance(spec, MissingSpec):
        return len(cells), sum(value is None for value in cells)
    observed = [value for value in cells if value is not None]
    if isinstance(spec, TypeSpec):
        return len(observed), sum(not matches_type(value, spec.expected) for value in observed)
    if isinstance(spec, SetSpec):
        allowed = set(spec.allowed)
        return len(observed), sum(value not in allowed for value in observed)
    parsed = numbers(observed)
    return len(parsed), sum(not spec.lower <= value <= spec.upper for value in parsed)


def bin_counts(cells: Sequence[Cell], bins: Bins) -> tuple[int, ...]:
    if isinstance(bins, NumericBins):
        histogram = [0] * (len(bins.cutpoints) + 1)
        for value in cells:
            if value is not None and (number := parse_number(value)) is not None:
                histogram[bisect_right(bins.cutpoints, number)] += 1
        return tuple(histogram)
    if isinstance(bins, CategoryBins):
        lookup = {label: index for index, label in enumerate(bins.vocabulary)}
        other = len(lookup)
        histogram = [0] * (other + 1)
        for value in cells:
            if value is not None:
                histogram[lookup.get(value, other)] += 1
        return tuple(histogram)
    raise TypeError("Unknown histogram bins")


def higher_violation_rate(current: int, failures: int, baseline: RateReference) -> float:
    return float(fisher_exact(
        [[failures, current - failures], [baseline.violations, baseline.trials - baseline.violations]],
        alternative="greater",
    ).pvalue)


def distribution_test(
    reference: Sequence[int], current: Sequence[int], *, resamples: int, rng: np.random.Generator
) -> tuple[float, float]:
    """Jensen–Shannon distance and a conditional Monte Carlo Pearson test."""
    baseline_counts = np.asarray(reference, dtype=np.int64)
    current_counts = np.asarray(current, dtype=np.int64)
    combined = baseline_counts + current_counts
    active = combined > 0
    if int(active.sum()) < 2:
        return 0.0, 1.0

    distance = float(jensenshannon(baseline_counts[active], current_counts[active], base=2))
    margins = combined[active]
    sample_size = int(current_counts.sum())
    expected = margins * (sample_size / int(margins.sum()))
    weights = 1 / expected + 1 / (margins - expected)
    statistic = float(np.sum((current_counts[active] - expected) ** 2 * weights))
    if statistic == 0:
        return distance, 1.0

    extreme = 0
    for start in range(0, resamples, 2048):
        draws = rng.multivariate_hypergeometric(margins, sample_size, size=min(2048, resamples - start))
        simulated = np.sum((draws - expected) ** 2 * weights, axis=1)
        extreme += int(np.count_nonzero(simulated >= statistic - 1e-12))
    return distance, (extreme + 1) / (resamples + 1)


def holm_adjust(p_values: Mapping[str, float]) -> dict[str, float]:
    """Adjust an entire batch of tests, controlling familywise error."""
    running = 0.0
    adjusted = {}
    for index, (rule_id, probability) in enumerate(sorted(p_values.items(), key=lambda pair: pair[1])):
        running = min(1.0, max(running, probability * (len(p_values) - index)))
        adjusted[rule_id] = running
    return adjusted
