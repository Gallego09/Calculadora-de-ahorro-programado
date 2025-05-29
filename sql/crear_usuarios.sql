CREATE TABLE IF NOT EXISTS usuarios (
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento_identidad BIGINT PRIMARY KEY,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);