from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config.database import get_async_session
from products.models import Product
from products.routers import products_router
from products.schemas import ProductCreate, ProductRead, ProductUpdate


@products_router.post("/create_product", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_async_session)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@products_router.get("/get_product", response_model=ProductRead)
def get_product(id_product: int, db: Session = Depends(get_async_session)):
    return db.query(Product).filter(Product.id == id_product).first()


@products_router.post("/update_product", response_model=ProductUpdate)
def update_product(id_product: int, product_update: ProductUpdate, db: Session = Depends(get_async_session)):
    product = db.query(Product).filter(Product.id == id_product).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@products_router.delete("/delete_product")
def delete_product(id_product: int, db: Session = Depends(get_async_session)):
    product = db.query(Product).filter(Product.id == id_product).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return JSONResponse(
        content={"detail": "Product deleted successfully."},
        status_code=status.HTTP_200_OK,
    )
