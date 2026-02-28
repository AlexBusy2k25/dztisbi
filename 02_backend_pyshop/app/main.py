import json

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import db, models, schemas


app = FastAPI(
    title="PyShop Checks Service",
    description="Упрощённый сервис генерации чеков (по мотивам тестового PyShop).",
)


@app.on_event("startup")
def on_startup() -> None:
    models.Base.metadata.create_all(bind=db.engine)


@app.post("/printers/", response_model=schemas.PrinterResponse)
def create_printer(
    payload: schemas.PrinterCreate,
    database: Session = Depends(db.get_db),
):
    instance = models.Printer(
        name=payload.name,
        api_key=payload.api_key,
        check_type=payload.check_type,
        point_id=payload.point_id,
    )
    database.add(instance)
    database.commit()
    database.refresh(instance)
    return schemas.PrinterResponse.model_validate(instance)


@app.post("/orders/", response_model=list[schemas.CheckResponse])
def create_order_checks(
    payload: schemas.OrderCreate,
    database: Session = Depends(db.get_db),
):
    printers_stmt = select(models.Printer).where(
        models.Printer.point_id == payload.point_id,
    )
    printers = database.execute(printers_stmt).scalars().all()
    if not printers:
        raise HTTPException(status_code=400, detail="No printers for this point")

    checks: list[models.Check] = []
    for printer in printers:
        item = models.Check(
            printer_id=printer.id,
            type=printer.check_type,
            order_payload=json.dumps(payload.payload, ensure_ascii=False),
        )
        database.add(item)
        checks.append(item)

    database.commit()

    for item in checks:
        database.refresh(item)

    return [
        schemas.CheckResponse.model_validate(check)
        for check in checks
    ]


@app.get("/checks/", response_model=list[schemas.CheckResponse])
def list_checks(database: Session = Depends(db.get_db)):
    stmt = select(models.Check).order_by(models.Check.created_at.desc())
    records = database.execute(stmt).scalars().all()
    return [schemas.CheckResponse.model_validate(check) for check in records]

