from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


def get_last_question(db: Session) -> models.Question | None:
    stmt = select(models.Question).order_by(models.Question.id.desc())
    return db.execute(stmt).scalars().first()


def save_questions(
    db: Session,
    questions: Iterable[dict],
) -> list[models.Question]:
    saved: list[models.Question] = []

    for q in questions:
        item = models.Question(
            external_id=q["id"],
            question=q["question"],
            answer=q["answer"],
        )
        db.add(item)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            continue
        db.refresh(item)
        saved.append(item)

    return saved


def fetch_and_store_unique_questions(
    db: Session,
    requester,
    amount: int,
) -> list[models.Question]:
    """
    Запрашивает новые вопросы у внешнего API и сохраняет только уникальные.
    """
    saved: list[models.Question] = []

    while len(saved) < amount:
        remaining = amount - len(saved)
        batch = requester(remaining)
        stored = save_questions(db, batch)

        if not stored:
            break

        saved.extend(stored)

    return saved

