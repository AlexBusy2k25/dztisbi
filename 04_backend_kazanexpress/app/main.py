from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import db, models, schemas

app = FastAPI(
    title="KazanExpress API",
    description="API для управления товарами",
)


@app.on_event("startup")
def on_startup() -> None:
    models.Base.metadata.create_all(bind=db.engine)


def create_product_in_db(database: Session, product_data: schemas.ProductCreate) -> models.Product:
    """Создаёт товар в БД"""
    instance = models.Product(
        name=product_data.name,
        price=product_data.price,
        category=product_data.category,
        stock=product_data.stock,
    )
    database.add(instance)
    database.commit()
    database.refresh(instance)
    return instance


def get_product_or_404(database: Session, product_id: int) -> models.Product:
    """Возвращает товар или 404"""
    product = database.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products/", response_model=schemas.ProductResponse, status_code=201)
def create_product(
        payload: schemas.ProductCreate,
        database: Session = Depends(db.get_db),
):
    product = create_product_in_db(database, payload)
    return schemas.ProductResponse.model_validate(product)


@app.get("/products/", response_model=list[schemas.ProductResponse])
def list_products(
        skip: int = 0,
        limit: int = 100,
        database: Session = Depends(db.get_db),
):
    stmt = select(models.Product).offset(skip).limit(limit)
    products = database.execute(stmt).scalars().all()
    return [schemas.ProductResponse.model_validate(product) for product in products]


@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(
        product_id: int,
        database: Session = Depends(db.get_db),
):
    product = get_product_or_404(database, product_id)
    return schemas.ProductResponse.model_validate(product)


@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
        product_id: int,
        payload: schemas.ProductUpdate,
        database: Session = Depends(db.get_db),
):
    product = get_product_or_404(database, product_id)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(product, field, value)

    database.commit()
    database.refresh(product)
    return schemas.ProductResponse.model_validate(product)


@app.delete("/products/{product_id}", status_code=204)
def delete_product(
        product_id: int,
        database: Session = Depends(db.get_db),
):
    product = get_product_or_404(database, product_id)
    database.delete(product)
    database.commit()
    return None