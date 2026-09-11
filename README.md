# Ejerecicio Practico Senior Backend Developer

Una api que analiza los clientes, ventas y categorías para una compañia de electronica, esta construido con **FastAPI** y **PostgreSQL**. Utiliza window functions, CTEs y subconsultas para obtener métricas de clientes, categorías y productos.

## Características

- API con FastAPI y `psycopg` (PostgreSQL async)
- Consultas analíticas
- Validación de respuestas con Pydantic
- Configuración de base de datos mediante variables de entorno

## Estructura del proyecto

```
ejercicio_analitica/
├── main.py          # Endpoints de la API
├── database.py      # Conexión async a PostgreSQL
├── models.py        # Consultas SQL analíticas
├── Schemas.py       # Modelos Pydantic de respuesta
├── script.sql       # Esquema y datos de ejemplo
└── .env             # Variables de entorno para la conexión a la base de datos
```



## Instalación

1. Clona o descarga el repositorio.
2. Configura las variables de entorno. Crea un archivo `.env` dentro de `ejercicio_analitica/` con:
  ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME= Nombre_de_la_base_de_datos
   DB_USER=tu_nombre
   DB_PASSWORD=tu_contraseña
  ```

## Ejecución

Desde la carpeta `ejercicio_analitica/`:

```cmd
uvicorn main:app --reload
```

La API estará disponible en el puerto: `http://127.0.0.1:8000`.

Documentación interactiva:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`



## Modelo de datos

El esquema representa un e-commerce con cuatro tablas:


| Tabla             | Descripción                         |
| ----------------- | ----------------------------------- |
| `clientes`        | Usuarios registrados                |
| `productos`       | Catálogo de productos por categoría |
| `ordenes`         | Compras realizadas por cada cliente |
| `detalle_ordenes` | Líneas de detalle de cada orden     |




## Endpoints



### `GET /api/clientes/ranking`

Ranking de clientes por total gastado, usando `DENSE_RANK()`.


| Parámetro | Tipo | Default | Descripción           |
| --------- | ---- | ------- | --------------------- |
| `limit`   | int  | 10      | Cantidad de registros |
| `offset`  | int  | 0       | Registros a omitir    |


**Ejemplo:** `GET /api/clientes/ranking?limit=5&offset=0`

---



### `GET /api/clientes/acumulado`

Total acumulado de compras de un cliente a lo largo del tiempo, usando window functions.


| Parámetro    | Tipo | Requerido | Descripción    |
| ------------ | ---- | --------- | -------------- |
| `cliente_id` | int  | Sí        | ID del cliente |


**Ejemplo:** `GET /api/clientes/acumulado?cliente_id=1`

Retorna `404` si el cliente no existe o no tiene órdenes.

---



### `GET /api/categorias/top`

Categorías cuyo total de ventas supera el promedio general, usando CTEs.

**Ejemplo:** `GET /api/categorias/top`

---



### `GET /api/productos/bajo-promedio`

Productos cuyo precio está por debajo del promedio de su categoría, usando subconsultas correlacionadas.

**Ejemplo:** `GET /api/productos/bajo-promedio`

## Consultas SQL utilizadas

- **Window functions:** `DENSE_RANK()`, `SUM() OVER (PARTITION BY ... ORDER BY ...)`
- **CTEs:** agregación por categoría y comparación con promedio general
- **Subconsultas:** promedio de precio por categoría



## Notas

- El archivo `.env` contiene credenciales sensibles y está excluido del control de versiones.
- El script `script.sql` incluye datos de ejemplo para probar los endpoints sin cargar datos adicionales.

