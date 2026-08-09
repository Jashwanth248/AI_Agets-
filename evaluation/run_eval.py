from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from geo_toolkit import compare_claimed_distance

ROOT = Path(__file__).resolve().parent
DATASET = ROOT / "golden_dataset.jsonl"
RESULTS = ROOT / "results" / "eval_results.csv"


def main() -> None:
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for line in DATASET.read_text().splitlines():
        case = json.loads(line)
        started = time.perf_counter()
        out = compare_claimed_distance(
            case["lat1"], case["lon1"], case["lat2"], case["lon2"], case["claimed_distance_km"]
        )
        rows.append(
            {
                "name": case["name"],
                "expected": case["expected"],
                "predicted": out["verdict"],
                "correct": out["verdict"] == case["expected"],
                "latency_ms": round((time.perf_counter() - started) * 1000, 3),
            }
        )
    with RESULTS.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    accuracy = sum(r["correct"] for r in rows) / len(rows)
    print(f"accuracy={accuracy:.3f} cases={len(rows)} results={RESULTS}")
    if accuracy < 1.0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
