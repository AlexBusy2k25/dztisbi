from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import db, models, schemas


app = FastAPI(
    title="KazanExpress Admin API",
    description="Упрощённое API админки магазина (по мотивам KazanExpress).",
)


@app.on_event("startup")
def on_startup() -> None:
    models.Base.metadata.create_all(bind=db.engine)


@app.post("/shops/", response_model=schemas.ShopResponse)
def create_shop(
    payload: schemas.ShopCreate,
    database: Session = Depends(db.get_db),
):
    instance = models.Shop(title=payload.title, image_url=payload.image_url)
    database.add(instance)
    database.commit()
    database.refresh(instance)
    return schemas.ShopResponse.model_validate(instance)


@app.get("/shops/", response_model=list[schemas.ShopResponse])
def list_shops(
    q: str | None = None,
    database: Session = Depends(db.get_db),
):
    stmt = select(models.Shop)
    if q:
        stmt = stmt.where(models.Shop.title.ilike(f"%{q}%"))
    records = database.execute(stmt).scalars().all()
    return [schemas.ShopResponse.model_validate(s) for s in records]


@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(
    payload: schemas.ProductCreate,
    database: Session = Depends(db.get_db),
):
    instance = models.Product(
        title=payload.title,
        price=payload.price,
        active=payload.active,
        shop_id=payload.shop_id,
    )
    database.add(instance)
    database.commit()
    database.refresh(instance)
    return schemas.ProductResponse.model_validate(instance)


@app.get("/products/", response_model=list[schemas.ProductResponse])
def list_products(
    active: bool | None = None,
    order_by_price: bool = False,
    database: Session = Depends(db.get_db),
):
    stmt = select(models.Product)
    if active is not None:
        stmt = stmt.where(models.Product.active == active)
    if order_by_price:
        stmt = stmt.order_by(models.Product.price)
    records = database.execute(stmt).scalars().all()
    return [schemas.ProductResponse.model_validate(p) for p in records]

