import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.products.router import router as products_router
from app.orders.router import router as orders_router

app = FastAPI()

app.include_router(products_router)
app.include_router(orders_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
