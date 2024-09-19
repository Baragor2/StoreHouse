from fastapi import FastAPI

from app.products.router import router as products_router

app = FastAPI()

app.include_router(products_router)
