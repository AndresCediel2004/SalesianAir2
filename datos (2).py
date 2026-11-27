"""Capa de datos de SalesinAir: funciones con ?, sin pantallas."""
import re
import sqlite3
from pathlib import Path

AQUI = Path(__file__).parent  # la carpeta de este archivo; nunca una ruta fija de su equipo


def conectar():
    """Abre base.db. Si no existe (p. ej. en la nube), la crea con esquema.sql y semilla.sql."""
    ruta = AQUI / "base.db"
    nueva = not ruta.exists()
    conn = sqlite3.connect(ruta, timeout=10, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")  # que SQLite revise las llaves foráneas
    if nueva:
        try:
            conn.executescript((AQUI / "esquema.sql").read_text(encoding="utf-8"))
            conn.executescript((AQUI / "semilla.sql").read_text(encoding="utf-8"))
            conn.commit()
        except (sqlite3.Error, OSError):
            conn.close()
            ruta.unlink(missing_ok=True)  # no dejar una base a medias: se recrea en el próximo intento
            raise
    return conn


COLUMNAS_CONSULTA = {
    "vuelo": ["Vuelo", "Origen", "Destino", "Salida", "Matrícula", "Avión", "Capacidad", "Reservados"],
    "reserva": ["Reserva", "Vuelo", "Origen", "Destino", "Salida", "Avión", "Asiento"],
    "documento": ["Reserva", "Vuelo", "Origen", "Destino", "Salida", "Avión", "Asiento"],
}
_POR_DOCUMENTO = """SELECT 'R' || printf('%05d', r.id), v.codigo_vuelo, v.origen, v.destino,
                     v.fecha_salida, a.modelo, r.asiento
              FROM reservas r
              JOIN vuelos v ON v.codigo_vuelo = r.codigo_vuelo
              JOIN aviones a ON a.matricula = v.matricula
              WHERE r.documento = ?
              ORDER BY v.fecha_salida"""
_POR_RESERVA = """SELECT 'R' || printf('%05d', r.id), v.codigo_vuelo, v.origen, v.destino,
                     v.fecha_salida, a.modelo, r.asiento
              FROM reservas r
              JOIN vuelos v ON v.codigo_vuelo = r.codigo_vuelo
              JOIN aviones a ON a.matricula = v.matricula
              WHERE r.id = ?"""


def tipo_de_busqueda(termino):
    """Adivina qué escribió la persona: 'documento' (solo dígitos), 'reserva' (R00001) o 'vuelo' (SA101)."""
    t = str(termino).strip().upper()
    if re.fullmatch(r"\d{5,15}", t):
        return "documento"
    if re.fullmatch(r"R\d{1,9}", t):
        return "reserva"
    return "vuelo"


def consultar(conn, termino):
    """Consulta (TPS): por código de vuelo, código de reserva o documento del pasajero.
    No devuelve nombres ni correos: la consulta es pública."""
    t = str(termino).strip().upper()
    tipo = tipo_de_busqueda(t)
    try:
        if tipo == "documento":
            return conn.execute(_POR_DOCUMENTO, (t,)).fetchall()
        if tipo == "reserva":
            return conn.execute(_POR_RESERVA, (int(t[1:]),)).fetchall()
        sql = """SELECT v.codigo_vuelo, v.origen, v.destino, v.fecha_salida,
                        a.matricula, a.modelo, a.capacidad, COUNT(r.id) AS reservados
                 FROM vuelos v
                 JOIN aviones a ON a.matricula = v.matricula
                 LEFT JOIN reservas r ON r.codigo_vuelo = v.codigo_vuelo
                 WHERE v.codigo_vuelo = ?
                 GROUP BY v.codigo_vuelo, a.matricula"""
        return conn.execute(sql, (t,)).fetchall()
    except sqlite3.Error as error:
        print("No se pudo consultar:", error)
        return []


def reportar(conn, codigo):
    """Reporte (MIS): ocupación por vuelo. 'codigo' es un código de vuelo (SA101) o una ciudad de origen (BOG)."""
    sql = """SELECT v.codigo_vuelo, v.origen, v.destino, v.fecha_salida,
                    COUNT(r.id) AS reservados, a.capacidad,
                    ROUND(100.0 * COUNT(r.id) / a.capacidad, 1) AS ocupacion
             FROM vuelos v
             JOIN aviones a ON a.matricula = v.matricula
             LEFT JOIN reservas r ON r.codigo_vuelo = v.codigo_vuelo
             WHERE v.codigo_vuelo = ? OR v.origen = ?
             GROUP BY v.codigo_vuelo, v.origen, v.destino, v.fecha_salida, a.capacidad
             ORDER BY v.fecha_salida"""
    c = str(codigo).strip().upper()
    try:
        return conn.execute(sql, (c, c)).fetchall()
    except sqlite3.Error as error:
        print("No se pudo generar el reporte:", error)
        return []


def codigo_de_reserva(conn, codigo_vuelo, documento):
    """Código (R00011) de la reserva de un pasajero en un vuelo, o '' si no existe."""
    fila = conn.execute("SELECT 'R' || printf('%05d', id) FROM reservas WHERE codigo_vuelo = ? AND documento = ?",
                        (codigo_vuelo, documento)).fetchone()
    return fila[0] if fila else ""


def registrar(conn, codigo_vuelo, documento, nombre, correo, asiento):
    """Registro (TPS): guarda al pasajero (si es nuevo) y su reserva, todo o nada.
    True si la base acepta el registro; False (y avisa por qué) si no se pudo."""
    try:
        vuelo = conn.execute(
            """SELECT a.capacidad,
                      (SELECT COUNT(*) FROM reservas r WHERE r.codigo_vuelo = v.codigo_vuelo)
               FROM vuelos v JOIN aviones a ON a.matricula = v.matricula
               WHERE v.codigo_vuelo = ?""", (codigo_vuelo,)).fetchone()
        if vuelo is None:
            print("Rechazado: el vuelo", codigo_vuelo, "no existe")
            return False
        if vuelo[1] >= vuelo[0]:
            print("Rechazado: el vuelo", codigo_vuelo, "está lleno")
            return False
        # Un pasajero que ya existe conserva sus datos: nadie los reescribe desde el formulario.
        conn.execute("""INSERT INTO pasajeros (documento, nombre, correo) VALUES (?, ?, ?)
                        ON CONFLICT(documento) DO NOTHING""", (documento, nombre, correo))
        conn.execute("""INSERT INTO reservas (codigo_vuelo, documento, asiento)
                        VALUES (?, ?, ?)""", (codigo_vuelo, documento, asiento))
        conn.commit()
        return True
    except sqlite3.Error as error:  # IntegrityError, base bloqueada, disco lleno...: se avisa, no se esconde
        conn.rollback()
        print("Rechazado por la base:", error)
        return False
