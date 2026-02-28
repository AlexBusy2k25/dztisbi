from collections import defaultdict
from hashlib import sha256
from typing import Dict, Iterable, Tuple

from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from . import db, models


app = FastAPI(
    title="AppBooster Experiments API",
    description="Упрощённый сервис A/B‑экспериментов.",
)


EXPERIMENTS = {
    "button_color": {
        "options": ["#FF0000", "#00FF00", "#0000FF"],
        "weights": [1, 1, 1],
    },
    "price": {
        "options": ["10", "20", "50", "5"],
        "weights": [75, 10, 5, 10],
    },
}


@app.on_event("startup")
def on_startup() -> None:
    models.Base.metadata.create_all(bind=db.engine)


def weighted_choice(
    device_token: str,
    key: str,
    options: Iterable[str],
    weights: Iterable[int],
) -> str:
    """
    Детерминированный выбор опции по весам.

    Для пары (device_token, key) получаем хэш и используем его
    как псевдослучайное число, распределяя его по интервалам весов.
    """
    opts = list(options)
    wts = list(weights)
    total = sum(wts)
    if total <= 0:
        raise ValueError("Total weight must be positive")

    hash_input = f"{device_token}:{key}".encode("utf-8")
    digest = sha256(hash_input).hexdigest()
    # Берём первые 8 символов как 32‑битное число:
    value = int(digest[:8], 16) % total

    cumulative = 0
    for option, weight in zip(opts, wts):
        cumulative += weight
        if value < cumulative:
            return option

    return opts[-1]


@app.get("/experiments/")
def get_experiments(
    device_token: str | None = Header(default=None, alias="Device-Token"),
    database: Session = Depends(db.get_db),
) -> Dict[str, str]:
    if device_token is None:
        raise HTTPException(status_code=400, detail="Device-Token header is required")

    result: Dict[str, str] = {}

    for key, config in EXPERIMENTS.items():
        options: Tuple[str, ...] = tuple(config["options"])
        weights: Tuple[int, ...] = tuple(config["weights"])

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

        value = weighted_choice(device_token, key, options, weights)
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


