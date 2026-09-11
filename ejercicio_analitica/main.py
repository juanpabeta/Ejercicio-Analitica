from typing import List

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Query

from database import get_db
from models import AnalyticsModel
from Schemas import (AcumuladoClienteResponse, ClienteRankingResponse,
                     ProductoBajoPromedioResponse, TopCategoriaResponse)

app= FastAPI(
    title="Dev Senior Code - E-commerce Analytics API",
    description="Microservicio con consultas avanzadas en PostgreSQL (Async)",
    version="1.0.0"
)

@app.get("/api/clientes/ranking", response_model=List[ClienteRankingResponse])
async def obtener_ranking_clientes(
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    offset: int = Query(0, ge=0, description="Número de registros a omitir"),
    db: psycopg.AsyncConnection = Depends(get_db)
):
    return await AnalyticsModel.get_clientes_ranking(db, limit, offset)


@app.get("/api/clientes/acumulado", response_model=List[AcumuladoClienteResponse])
async def obtener_acumulado_cliente(
    cliente_id: int = Query(..., description="ID del cliente a consultar"),
    db: psycopg.AsyncConnection = Depends(get_db)
):
    resultados = await AnalyticsModel.get_acumulado_cliente(db, cliente_id)
    if not resultados:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o sin ordenes registradas")
    return resultados

@app.get("/api/categorias/top", response_model=List[TopCategoriaResponse])
async def obtener_categorias_top(db: psycopg.AsyncConnection = Depends(get_db)):
    return await AnalyticsModel.get_categorias_top(db)

@app.get("/api/productos/bajo-promedio", response_model=List[ProductoBajoPromedioResponse])
async def obtener_productos_bajo_promedio(db: psycopg.AsyncConnection = Depends(get_db)):
    return await AnalyticsModel.get_productos_bajo_promedio(db)