from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import health, proveedores, insumos, clientes, maquinas, registro_consumos, tecnicos, mantenimientos, users
from app.api.v1.endpoints.auth import login
from app.api.v1.endpoints.reportes import facturacion_mensual, insumos_mas_consumidos, tecnicos_mas_mantenimientos, clientes_mas_maquinas

app = FastAPI(
    title="Marloy API",
    description="Python-based API for Marloy Café",
    version="1.0.0",
    contact={
        "name": "Felipe Cabrera",
        "email": "me@felieppe.com"
    }
)

origins = [
    "http://localhost:3000",
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(health.router, prefix="/v1/health", tags=["Health"])
app.include_router(login.router, prefix="/v1/auth/login", tags=["Autenticación"])
app.include_router(proveedores.router, prefix="/v1/proveedores", tags=["Proveedores"])
app.include_router(insumos.router, prefix="/v1/insumos", tags=["Insumos"])
app.include_router(clientes.router, prefix="/v1/clientes", tags=["Clientes"])
app.include_router(maquinas.router, prefix="/v1/maquinas", tags=["Maquinas"])
app.include_router(tecnicos.router, prefix="/v1/tecnicos", tags=["Tecnicos"])
app.include_router(mantenimientos.router, prefix="/v1/mantenimientos", tags=["Mantenimientos"])
app.include_router(registro_consumos.router, prefix="/v1/registro-consumos", tags=["Registros de Consumo"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])

app.include_router(facturacion_mensual.router, prefix="/v1/reportes/facturacion-mensual", tags=["Reportes"])
app.include_router(insumos_mas_consumidos.router, prefix="/v1/reportes/insumos-mas-consumidos", tags=["Reportes"])
app.include_router(tecnicos_mas_mantenimientos.router, prefix="/v1/reportes/tecnicos-mas-mantenimientos", tags=["Reportes"])
app.include_router(clientes_mas_maquinas.router, prefix="/v1/reportes/clientes-mas-maquinas", tags=["Reportes"])

@app.get("/", summary="Root Endpoint", tags=["Root"])
async def root():
    return {"message": "Welcome to Marloy Café API!"}