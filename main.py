from typing import List

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


products: List[Product] = []  # хранение элементов без БД


@app.get("/products/", response_model=List[Product], tags=["Products"])
def list_products(
    skip: int = Query(0, description="Количество пропускаемых товаров"),
    limit: int = Query(10, description="Максимальное число товаров для выдачи"),
):
    # Возвращаем срез списка
    return products[skip : skip + limit]


@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
def get_product(product_id: int = Path(..., description="ID товара для получения")):
    # Ищем товар по ID
    for p in products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")


@app.post(
    "/products/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
)
def create_product(product: ProductCreate):
    # Создаем новый товар с новым ID
    new_id = len(products) + 1
    new_product = Product(id=new_id, **product.dict())
    products.append(new_product)
    return new_product


@app.put("/products/{product_id}", response_model=Product, tags=["Products"])
def update_product(
    product_id: int = Path(..., description="ID товара для обновления"),
    product: ProductCreate = ...,
):
    # Обновляем существующий товар
    for i, p in enumerate(products):
        if p.id == product_id:
            updated = Product(id=product_id, **product.dict())
            products[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete(
    "/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"]
)
def delete_product(product_id: int = Path(..., description="ID товара для удаления")):
    # Удаляем товар по ID
    for i, p in enumerate(products):
        if p.id == product_id:
            products.pop(i)
            return  # 204 No Content
    raise HTTPException(status_code=404, detail="Product not found")
