-- Datos de ejemplo FICTICIOS (no son personas reales).
INSERT INTO aviones VALUES
    ('HK-4501', 'Airbus A320', 180),
    ('HK-4502', 'Boeing 737-800', 162),
    ('HK-4610', 'ATR 72-600', 70);
INSERT INTO pasajeros VALUES
    ('1010101010', 'Camila Rojas',     'camila.rojas@example.com'),
    ('1020202020', 'Santiago Pérez',   'santiago.perez@example.com'),
    ('1030303030', 'Valentina Gómez',  'valentina.gomez@example.com'),
    ('1040404040', 'Mateo Díaz',       'mateo.diaz@example.com'),
    ('1050505050', 'Isabella Torres',  'isabella.torres@example.com'),
    ('1060606060', 'Daniel Herrera',   'daniel.herrera@example.com');
INSERT INTO vuelos VALUES
    ('SA101', 'HK-4501', 'BOG', 'MDE', '2026-12-01 08:00'),
    ('SA102', 'HK-4502', 'BOG', 'CTG', '2026-12-01 10:30'),
    ('SA103', 'HK-4610', 'BOG', 'CLO', '2026-12-02 07:15'),
    ('SA201', 'HK-4501', 'MDE', 'BOG', '2026-12-03 18:00'),
    ('SA202', 'HK-4502', 'CTG', 'BOG', '2026-12-04 15:20');
INSERT INTO reservas (codigo_vuelo, documento, asiento) VALUES
    ('SA101', '1010101010', '1A'), ('SA101', '1020202020', '1B'), ('SA101', '1030303030', '2A'),
    ('SA102', '1040404040', '3C'), ('SA102', '1010101010', '3D'),
    ('SA103', '1050505050', '1A'), ('SA103', '1060606060', '1B'),
    ('SA201', '1020202020', '5A'), ('SA201', '1030303030', '5B'),
    ('SA202', '1040404040', '7F');
