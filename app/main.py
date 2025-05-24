from fastapi import FastAPI
from app.api.v1.endpoints import health
from app.api.v1.endpoints.auth import login

app = FastAPI(
    title="Marloy API",
    description="Python-based API for Marloy Café",
    version="1.0.0",
    contact={
        "name": "Felipe Cabrera",
        "email": "me@felieppe.com"
    }
)

app.include_router(health.router, prefix="/v1/health", tags=["Health"])
app.include_router(login.router, prefix="/v1/auth/login", tags=["Login"])

@app.get("/")
async def root():
    return {"message": "Welcome to Marloy Café API!"}