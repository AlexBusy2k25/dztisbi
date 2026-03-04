from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import db, models, schemas

app = FastAPI(
    title="UpTrader API",
    description="API для управления задачами",
)


@app.on_event("startup")
def on_startup() -> None:
    models.Base.metadata.create_all(bind=db.engine)


def create_task_in_db(database: Session, task_data: schemas.TaskCreate) -> models.Task:
    """Создаёт задачу в БД"""
    instance = models.Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status or "pending",
    )
    database.add(instance)
    database.commit()
    database.refresh(instance)
    return instance


def get_task_or_404(database: Session, task_id: int) -> models.Task:
    """Возвращает задачу или 404"""
    task = database.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks/", response_model=schemas.TaskResponse, status_code=201)
def create_task(
        payload: schemas.TaskCreate,
        database: Session = Depends(db.get_db),
):
    task = create_task_in_db(database, payload)
    return schemas.TaskResponse.model_validate(task)


@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def list_tasks(
        skip: int = 0,
        limit: int = 100,
        database: Session = Depends(db.get_db),
):
    stmt = select(models.Task).offset(skip).limit(limit)
    tasks = database.execute(stmt).scalars().all()
    return [schemas.TaskResponse.model_validate(task) for task in tasks]


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(
        task_id: int,
        database: Session = Depends(db.get_db),
):
    task = get_task_or_404(database, task_id)
    return schemas.TaskResponse.model_validate(task)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
        task_id: int,
        payload: schemas.TaskUpdate,
        database: Session = Depends(db.get_db),
):
    task = get_task_or_404(database, task_id)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(task, field, value)

    database.commit()
    database.refresh(task)
    return schemas.TaskResponse.model_validate(task)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(
        task_id: int,
        database: Session = Depends(db.get_db),
):
    task = get_task_or_404(database, task_id)
    database.delete(task)
    database.commit()
    return None