from collections import defaultdict
from typing import Dict, List

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import db, models, schemas

app = FastAPI(
    title="UpTrader Menu Service",
    description="Упрощённый сервис древовидного меню (по мотивам тестового UpTrader).",
)


@app.on_event("startup")
def on_startup() -> None:
    models.Base.metadata.create_all(bind=db.engine)


@app.post("/menu-items/", response_model=schemas.MenuItemNode)
def create_menu_item(
    payload: schemas.MenuItemCreate,
    database: Session = Depends(db.get_db),
):
    instance = models.MenuItem(
        name=payload.name,
        url=payload.url,
        menu_name=payload.menu_name,
        parent_id=payload.parent_id,
    )
    database.add(instance)
    database.commit()
    database.refresh(instance)
    return schemas.MenuItemNode.model_validate(instance)


@app.get("/menus/{menu_name}", response_model=List[schemas.MenuItemNode])
def get_menu(menu_name: str, database: Session = Depends(db.get_db)):
    stmt = select(models.MenuItem).where(models.MenuItem.menu_name == menu_name)
    items = database.execute(stmt).scalars().all()

    by_parent: Dict[int | None, List[models.MenuItem]] = defaultdict(list)
    lookup: Dict[int, models.MenuItem] = {}

    for item in items:
        lookup[item.id] = item
        by_parent[item.parent_id].append(item)

    def build_node(model: models.MenuItem) -> schemas.MenuItemNode:
        children = [build_node(child) for child in by_parent.get(model.id, [])]
        return schemas.MenuItemNode(
            id=model.id,
            name=model.name,
            url=model.url,
            children=children,
        )

    roots = [build_node(item) for item in by_parent.get(None, [])]
    return roots
