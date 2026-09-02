from fastapi import FastAPI

from backend.config import settings
from backend.routes import admin, auth, keys, transactions, wallets


app = FastAPI(title=settings.app_name)
app.include_router(auth.router)
app.include_router(wallets.router)
app.include_router(transactions.router)
app.include_router(keys.router)
app.include_router(admin.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "environment": settings.environment}
