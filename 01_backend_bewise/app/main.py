from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, db, external_api, models, schemas


app = FastAPI(
    title="Bewise Questions Service",
    description="Сервис для работы с вопросами викторины (тестовое Bewise).",
)


@app.on_event("startup")
def on_startup() -> None:
    models.Base.metadata.create_all(bind=db.engine)


@app.post("/questions/", response_model=schemas.QuestionResponse | dict)
def create_questions(
    payload: schemas.QuestionsRequest,
    database: Session = Depends(db.get_db),
):
    previous = crud.get_last_question(database)
    crud.fetch_and_store_unique_questions(
        db=database,
        requester=external_api.fetch_questions,
        amount=payload.questions_num,
    )

    if previous is None:
        return {}

    return schemas.QuestionResponse.model_validate(previous)


@app.get("/questions/last", response_model=schemas.QuestionResponse | dict)
def get_last_question(database: Session = Depends(db.get_db)):
    item = crud.get_last_question(database)
    if item is None:
        return {}
    return schemas.QuestionResponse.model_validate(item)

