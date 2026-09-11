from typing import Any, Dict, List

import psycopg


class AnalyticsModel:
    
    @staticmethod
    async def get_clientes_ranking(
        db: psycopg.AsyncConnection,
        limit: int,
        offset: int
    )-> List[Dict[str, Any]]:
        query = """
            SELECT
                c.id,
                c.nombre,
                SUM(o.total) AS total_gastado,
                DENSE_RANK() OVER (ORDER BY SUM(o.total) DESC) AS ranking
            FROM clientes c
            JOIN ordenes o ON c.id = o.cliente_id
            GROUP BY c.id, c.nombre
            ORDER BY ranking
            LIMIT %s OFFSET %s;
        """
        async with db.cursor() as cur:
            await cur.execute(query, (limit, offset))
            return await cur.fetchall()
    
    @staticmethod
    async def get_acumulado_cliente(
        db: psycopg.AsyncConnection, 
        cliente_id: int
    ) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                o.id AS orden_id,
                o.fecha_orden,
                o.total,
                SUM(o.total) OVER (
                    PARTITION BY o.cliente_id 
                    ORDER BY o.fecha_orden
                ) AS acumulado_cliente
            FROM ordenes o
            WHERE o.cliente_id = %s;
        """
        async with db.cursor() as cur:
            await cur.execute(query, (cliente_id,))
            return await cur.fetchall()

    @staticmethod
    async def get_categorias_top(db: psycopg.AsyncConnection) -> List[Dict[str, Any]]:
        query = """
            WITH VentasPorCategoria AS (
                SELECT 
                    p.categoria, 
                    SUM(d.cantidad * d.precio_unitario) AS total_categoria
                FROM detalle_ordenes d
                JOIN productos p ON d.producto_id = p.id
                GROUP BY p.categoria
            ),
            PromedioGeneral AS (
                SELECT AVG(total_categoria) AS promedio FROM VentasPorCategoria
            )
            SELECT v.categoria, v.total_categoria
            FROM VentasPorCategoria v, PromedioGeneral p
            WHERE v.total_categoria > p.promedio;
        """
        async with db.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()

    @staticmethod
    async def get_productos_bajo_promedio(db: psycopg.AsyncConnection) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                p.id,
                p.nombre,
                p.categoria,
                p.precio,
                (
                    SELECT AVG(p2.precio) 
                    FROM productos p2 
                    WHERE p2.categoria = p.categoria
                ) AS promedio_categoria
            FROM productos p
            WHERE p.precio < (
                SELECT AVG(p2.precio) 
                FROM productos p2 
                WHERE p2.categoria = p.categoria
            );
        """
        async with db.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()