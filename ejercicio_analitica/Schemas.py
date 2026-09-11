from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ClienteRankingResponse (BaseModel):
    id: int
    nombre: str
    total_gastado: Decimal
    ranking: int

class AcumuladoClienteResponse(BaseModel):
    orden_id: int
    fecha_orden: datetime
    total: Decimal
    acumulado_cliente: Decimal

class TopCategoriaResponse(BaseModel):
    categoria: str
    total_categoria: Decimal

class ProductoBajoPromedioResponse(BaseModel):
    id: int
    nombre: str
    categoria: str
    precio: Decimal
    promedio_categoria: Decimal