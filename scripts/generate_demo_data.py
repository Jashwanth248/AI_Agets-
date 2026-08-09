from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta, timezone

from data_pipeline.warehouse import AuditWarehouse


def main(n: int = 250) -> None:
    random.seed(42)
    warehouse = AuditWarehouse()
    now = datetime.now(timezone.utc)
    for i in range(n):
        deviation = max(0.0, random.gauss(22, 28))
        verdict = "Accurate" if deviation <= 10 else "Inaccurate"
        risk = min(deviation / 100.0, 1.0)
        warehouse.write_event(
            {
                "audit_id": str(uuid.uuid4()),
                "created_at": (now - timedelta(minutes=i * 17)).isoformat(),
                "pipeline": random.choice(["geo_distance", "general_fact", "dataset_quality"]),
                "verdict": verdict,
                "confidence": round(random.uniform(0.72, 0.99), 3),
                "risk_score": round(risk, 3),
                "latency_ms": round(random.uniform(8, 950), 2),
                "deviation_pct": round(deviation, 2),
                "input_length": random.randint(25, 1200),
                "evidence_count": random.randint(1, 6),
            }
        )
    print(warehouse.summary())


if __name__ == "__main__":
    main()
