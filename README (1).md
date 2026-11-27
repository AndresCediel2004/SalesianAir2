# SalesinAir (aerolínea de pasajeros)

**App:** https://salesianair.onrender.com  
**Repositorio:** https://github.com/AndresCediel2004/SalesianAir.git

**Necesidad:** Consultar por código la información de cada vuelo y registrar a los pasajeros que viajan en él, para saber cuántos asientos quedan. **Quién decide:** Jefe de operaciones de vuelo. **Tipo de SI:** TPS y MIS.

## Componentes del sistema de información

- **hardware:** Computadores del mostrador de la aerolínea y el servidor donde corre la app
- **software:** App Solara, módulo datos.py y el motor SQLite (tablas pasajeros, aviones, vuelos y reservas)
- **datos:** Una fila de reservas = un pasajero con asiento en un vuelo; cada vuelo usa un avión de la flota
- **personas:** Agente de mostrador que registra, analista que consolida, jefe de operaciones que decide
- **tic:** La red de la aerolínea y el navegador por el que se abre la app

## Proceso

1. El agente consulta un vuelo, una reserva o a un pasajero por su código o documento
2. Registra al pasajero y su asiento
3. La app consolida la ocupación por vuelo
4. El jefe de operaciones revisa el reporte y ajusta la operación

## Cómo se usa


1. En "Consultar", la persona escribe un código de vuelo (SA101), un código de reserva (R00001) o el documento de un pasajero. Por vuelo ve origen, destino, salida, avión y asientos reservados; por reserva o documento ve los vuelos y asientos de ese pasajero.
2. En el reporte escribe un código de vuelo (SA101) o una ciudad de origen (BOG) y ve la ocupación (reservados frente a la capacidad del avión); con eso el jefe de operaciones decide si refuerza un vuelo o cambia el avión.
3. En "Registrar pasajero en un vuelo", el agente escribe código del vuelo, documento, nombre, correo y asiento, y pulsa Guardar. La app avisa "Registrado" y muestra el código de reserva, o "Rechazado" con el motivo (campo vacío, vuelo inexistente o lleno, asiento ocupado).
4. Si el registro no se puede hacer, no se guarda nada: la operación es de todo o nada.


## Datos personales (Ley 1581 de 2012)


El sistema guarda datos personales mínimos de los pasajeros: número de documento, nombre y correo electrónico, solo para identificar quién viaja en cada vuelo y en qué asiento (finalidad). No se piden teléfonos, direcciones ni datos sensibles.
Según la Ley 1581 de 2012 de Colombia, quien trata datos personales debe informar la finalidad, pedir autorización y proteger la información; el titular puede conocer, actualizar y pedir que se suprima su dato.
Los pasajeros de la semilla son FICTICIOS. Esta app es pública y no tiene inicio de sesión: no escriba datos reales de nadie. La base (base.db) no se sube a GitHub y la consulta pública no muestra nombres ni documentos.


## Correr en su equipo

```
conda activate si2026
solara run app.py
```
