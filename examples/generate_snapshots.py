"""Create deterministic CSV inputs for the documented CLI walkthrough."""

from __future__ import annotations

import csv
from pathlib import Path
from random import Random


def generate(path: Path, *, first_id: int, seed: int, changed: bool = False) -> None:
    rng = Random(seed)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("order_id", "amount", "status", "recorded_on"))
        for index in range(1200):
            order_id = first_id + index
            amount = round(rng.lognormvariate(5.0 + 0.9 * changed, 0.45), 2)
            status = rng.choices(("paid", "pending", "cancelled"), (80, 15, 5))[0]
            if changed and index % 7 == 0:
                status = "unknown"
            if changed and index % 16 == 1:
                order_id -= 1
            writer.writerow((
                order_id, None if changed and index % 5 == 0 else amount, status, "2026-11-17",
            ))


if __name__ == "__main__":
    output = Path("autodq-runs")
    output.mkdir(exist_ok=True)
    generate(output / "reference.csv", first_id=1, seed=90210)
    generate(output / "stable.csv", first_id=1201, seed=73614)
    generate(output / "shifted.csv", first_id=2401, seed=75381, changed=True)
