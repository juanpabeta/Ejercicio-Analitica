CREATE TABLE clientes(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR (100) UNIQUE NOT NULL,
    fecha_registro DATE DEFAULT CURRENT_DATE
);

CREATE TABLE PRODUCTOS(
    id SERIAL  PRIMARY Key,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR (100) NOT NULL,
    precio NUMERIC (10, 2) NOT NULL
);

CREATE TABLE ordenes (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    fecha_orden TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total NUMERIC(10, 2) NOT NULL
);

CREATE TABLE detalle_ordenes (
    id SERIAL PRIMARY KEY,
    orden_id INT REFERENCES ordenes(id),
    producto_id INT REFERENCES productos(id),
    cantidad INT NOT NULL,
    precio_unitario NUMERIC(10, 2) NOT NULL
);

INSERT INTO clientes (nombre, email) VALUES
('Ana Gomez', 'ana@example.com'),
('Carlos Ruiz', 'carlos@example.com'),
('Maria Lopez', 'maria@example.com'),
('Juan Perez', 'juan@example.com');

INSERT INTO productos (nombre, categoria, precio) VALUES
('Laptop Pro', 'Electronica', 1200.00),
('Smartphone X', 'Electronica', 800.00),
('Teclado Mecanico', 'Accesorios', 100.00),
('Mouse Inalambrico', 'Accesorios', 50.00),
('Monitor 4K', 'Electronica', 400.00);

INSERT INTO ordenes (cliente_id, fecha_orden, total) VALUES
(1, '2026-01-10 10:00:00', 1300.00),
(1, '2026-02-15 14:30:00', 850.00),
(2, '2026-01-20 11:15:00', 100.00),
(3, '2026-02-01 09:00:00', 2000.00),
(1, '2026-03-01 16:45:00', 50.00);

INSERT INTO detalle_ordenes (orden_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 1, 1200.00), (1, 4, 2, 50.00),
(2, 2, 1, 800.00),  (2, 4, 1, 50.00),
(3, 3, 1, 100.00),
(4, 1, 1, 1200.00), (4, 2, 1, 800.00),
(5, 4, 1, 50.00);
