-- SalesinAir · esquema normalizado (3FN)
-- aviones, pasajeros y vuelos son entidades; reservas es la tabla puente
-- (un pasajero viaja en muchos vuelos y un vuelo lleva muchos pasajeros).
CREATE TABLE aviones (
    matricula TEXT PRIMARY KEY CHECK (length(matricula) >= 4),
    modelo    TEXT NOT NULL,
    capacidad INTEGER NOT NULL CHECK (capacidad > 0)
);
CREATE TABLE pasajeros (
    documento TEXT PRIMARY KEY
              CHECK (length(documento) BETWEEN 5 AND 15 AND documento NOT GLOB '*[^0-9]*'),
    nombre    TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    correo    TEXT NOT NULL CHECK (correo LIKE '%_@_%._%')
);
CREATE TABLE vuelos (
    codigo_vuelo TEXT PRIMARY KEY,
    matricula    TEXT NOT NULL REFERENCES aviones(matricula),
    origen       TEXT NOT NULL CHECK (origen  GLOB '[A-Z][A-Z][A-Z]'),
    destino      TEXT NOT NULL CHECK (destino GLOB '[A-Z][A-Z][A-Z]'),
    fecha_salida TEXT NOT NULL
                 CHECK (fecha_salida GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]'),
    CHECK (origen <> destino),
    UNIQUE (matricula, fecha_salida)
);
CREATE TABLE reservas (
    id           INTEGER PRIMARY KEY,
    codigo_vuelo TEXT NOT NULL REFERENCES vuelos(codigo_vuelo),
    documento    TEXT NOT NULL REFERENCES pasajeros(documento),
    asiento      TEXT NOT NULL CHECK (asiento GLOB '[0-9]*[A-F]'),
    UNIQUE (codigo_vuelo, documento),
    UNIQUE (codigo_vuelo, asiento)
);
CREATE INDEX idx_reservas_documento ON reservas(documento);
