from pydantic import BaseModel


class ShopCreate(BaseModel):
    title: str
    image_url: str | None = None


class ShopResponse(BaseModel):
    id: int
    title: str
    image_url: str | None = None

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    title: str
    price: float
    active: bool = True
    shop_id: int


class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    active: bool
    shop_id: int

    class Config:
        from_attributes = True

