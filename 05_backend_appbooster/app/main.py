from collections import defaultdict
from typing import Dict

from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from . import db, models


app = FastAPI(
    title="AppBooster Experiments API",
    description="Упрощённый сервис A/B‑экспериментов.",
)


EXPERIMENTS = {
    "button_color": ["#FF0000", "#00FF00", "#0000FF"],
    "price": ["10", "20", "50", "5"],
}


@app.on_event("startup")
def on_startup() -> None:
    models.Base.metadata.create_all(bind=db.engine)


def deterministic_choice(device_token: str, key: str, options: list[str]) -> str:
    seed = sum(ord(ch) for ch in (device_token + key))
    index = seed % len(options)
    return options[index]


@app.get("/experiments/")
def get_experiments(
    device_token: str | None = Header(default=None, alias="Device-Token"),
    database: Session = Depends(db.get_db),
) -> Dict[str, str]:
    if device_token is None:
        raise HTTPException(status_code=400, detail="Device-Token header is required")

    result: Dict[str, str] = {}

    for key, options in EXPERIMENTS.items():
        stmt = select(models.ExperimentAssignment).where(
            and_(
                models.ExperimentAssignment.device_token == device_token,
                models.ExperimentAssignment.experiment_key == key,
            ),
        )
        existing = database.execute(stmt).scalars().first()
        if existing is not None:
            result[key] = existing.option_value
            continue

        value = deterministic_choice(device_token, key, options)
        assignment = models.ExperimentAssignment(
            device_token=device_token,
            experiment_key=key,
            option_value=value,
        )
        database.add(assignment)
        database.commit()
        result[key] = value

    return result


@app.get("/experiments/stats")
def experiments_stats(database: Session = Depends(db.get_db)):
    stmt = select(models.ExperimentAssignment)
    rows = database.execute(stmt).scalars().all()
    stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        stats[row.experiment_key][row.option_value] += 1
    return stats

