CREATE DATABASE IF NOT EXISTS `marloy` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'marloy'@'%' IDENTIFIED BY 'marloy';
GRANT ALL PRIVILEGES ON `marloy`.* TO 'marloy'@'%';
FLUSH PRIVILEGES;

USE `marloy`;

-- Tabla para gestionar usuarios del sistema
CREATE TABLE IF NOT EXISTS login (
    correo VARCHAR(255) PRIMARY KEY,
    contraseña VARCHAR(255) NOT NULL,
    es_administrador BOOLEAN NOT NULL DEFAULT FALSE
);

-- Tabla para los proveedores de insumos
CREATE TABLE IF NOT EXISTS proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    contacto VARCHAR(255)
);

-- Tabla para los insumos (leche en polvo, canela, chocolate, café, etc.)
CREATE TABLE IF NOT EXISTS insumos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    tipo VARCHAR(100),
    precio_unitario DECIMAL(10, 2) NOT NULL,
    id_proveedor INT NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id)
);

-- Tabla para los clientes de las máquinas expendedoras
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(50),
    correo VARCHAR(255) UNIQUE
);

-- Tabla para las máquinas expendedoras
-- Una máquina sólo puede estar asignada a un cliente y una ubicación a la vez
CREATE TABLE IF NOT EXISTS maquinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    id_cliente INT NOT NULL,
    ubicacion_cliente VARCHAR(255) NOT NULL,
    costo_alquiler_mensual DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    UNIQUE (id_cliente, ubicacion_cliente)
);

-- Tabla para el registro de consumos de insumos por máquina y fecha
CREATE TABLE IF NOT EXISTS registro_consumo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_maquina INT NOT NULL,
    id_insumo INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Los consumos deben registrarse con fecha para facturación
    cantidad_usada DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_maquina) REFERENCES maquinas(id),
    FOREIGN KEY (id_insumo) REFERENCES insumos(id)
);

-- Tabla para los técnicos que realizan mantenimientos
CREATE TABLE IF NOT EXISTS tecnicos (
    ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(50)
);

-- Tabla para registrar los mantenimientos realizados
-- Un técnico no debe estar asignado a dos mantenimientos simultáneos (en el mismo día y hora, si se registra)
CREATE TABLE IF NOT EXISTS mantenimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_maquina INT NOT NULL,
    ci_tecnico VARCHAR(20) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    FOREIGN KEY (id_maquina) REFERENCES maquinas(id),
    FOREIGN KEY (ci_tecnico) REFERENCES tecnicos(ci),
    UNIQUE (ci_tecnico, fecha)
);

-- 3. Datos Maestros (Datos de ejemplo para poblar las tablas)
-- -----------------------------------------------------------

-- Usuarios
INSERT INTO login (correo, contraseña, es_administrador) VALUES
('admin@marloy.com', 'adminpass', TRUE),
('user@marloy.com', 'userpass', FALSE);

-- Proveedores
INSERT INTO proveedores (nombre, contacto) VALUES
('Distribuidora Café Max', 'contacto@cafemax.com'),
('Lácteos del Campo', 'leche@campo.com'),
('Saborizantes Gourmet', 'info@gourmet.net');

-- Insumos
INSERT INTO insumos (descripcion, tipo, precio_unitario, id_proveedor) VALUES
('Café Tostado Grano', 'Café', 0.15, 1),
('Leche en Polvo Premium', 'Lácteo', 0.10, 2),
('Chocolate en Polvo', 'Saborizante', 0.08, 3),
('Canela en Polvo', 'Saborizante', 0.05, 3),
('Azúcar Blanca', 'Endulzante', 0.02, 1);

-- Clientes
INSERT INTO clientes (nombre, direccion, telefono, correo) VALUES
('Oficinas Centrales ABC', 'Av. 18 de Julio 1234, Montevideo', '22345678', 'abc@cliente.com'),
('Fábrica XYZ', 'Ruta 5 Km 20, Canelones', '23001234', 'xyz@cliente.com'),
('Tienda Retail Express', 'Calle Principal 567, Pando', '24567890', 'retail@cliente.com');

-- Máquinas
INSERT INTO maquinas (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual) VALUES
('CM-Pro 5000', 1, 'Hall Principal', 150.00),
('CM-Home Mini', 1, 'Cocina Piso 3', 80.00),
('CM-Industrial 8000', 2, 'Comedor Planta Baja', 200.00),
('CM-Pro 5000', 3, 'Entrada Tienda', 150.00);

-- Técnicos
INSERT INTO tecnicos (ci, nombre, apellido, telefono) VALUES
('1234567-8', 'Ana', 'García', '099123456'),
('8765432-1', 'Luis', 'Fernández', '098765432'),
('5555555-0', 'Marta', 'Rodríguez', '091000111');

-- Registros de Consumo (ejemplos)
INSERT INTO registro_consumo (id_maquina, id_insumo, fecha, cantidad_usada) VALUES
(1, 1, '2025-05-01 09:00:00', 100), -- Café
(1, 2, '2025-05-01 09:00:00', 50),  -- Leche
(1, 3, '2025-05-02 10:30:00', 30),  -- Chocolate
(1, 1, '2025-05-15 11:00:00', 120); -- Café

-- Para máquina 3 (Fábrica XYZ, Comedor Planta Baja)
INSERT INTO registro_consumo (id_maquina, id_insumo, fecha, cantidad_usada) VALUES
(3, 1, '2025-05-01 14:00:00', 200),
(3, 2, '2025-05-01 14:00:00', 100),
(3, 5, '2025-05-03 08:15:00', 80);

-- Mantenimientos (ejemplos)
INSERT INTO mantenimientos (id_maquina, ci_tecnico, tipo, fecha, observaciones) VALUES
(1, '1234567-8', 'Preventivo', '2025-05-10 10:00:00', 'Limpieza general y revisión de filtros.'),
(3, '8765432-1', 'Asistencia', '2025-05-12 15:30:00', 'Falla en dispensador de leche.'),
(4, '1234567-8', 'Preventivo', '2025-05-10 14:00:00', 'Revisión de conexiones eléctricas.');
