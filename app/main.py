from fastapi import FastAPI
from app.api.v1.endpoints import health, proveedores, insumos, clientes, maquinas, registro_consumos, tecnicos, mantenimientos
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
app.include_router(proveedores.router, prefix="/v1/proveedores", tags=["Proveedores"])
app.include_router(insumos.router, prefix="/v1/insumos", tags=["Insumos"])
app.include_router(clientes.router, prefix="/v1/clientes", tags=["Clientes"])
app.include_router(maquinas.router, prefix="/v1/maquinas", tags=["Maquinas"])
app.include_router(tecnicos.router, prefix="/v1/tecnicos", tags=["Tecnicos"])
app.include_router(mantenimientos.router, prefix="/v1/mantenimientos", tags=["Mantenimientos"])
app.include_router(registro_consumos.router, prefix="/v1/registro-consumos", tags=["Registros de Consumo"])

@app.get("/")
async def root():
    return {"message": "Welcome to Marloy Café API!"}