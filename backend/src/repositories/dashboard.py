from db.conexion_db import *
from datetime import date, datetime, timedelta


def dashboard_repositories(desde=None, hasta=None):
    conn = None
    cursor = None

    try:
        # Fechas predeterminadas: últimos 30 días.
        hoy = date.today()

        if not desde:
            desde = (hoy - timedelta(days=30)).isoformat()

        if not hasta:
            hasta = hoy.isoformat()

        # Validar las fechas.
        try:
            fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date()
            fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return {
                "Error": "Las fechas deben tener el formato AAAA-MM-DD."
            }, 400

        if fecha_desde > fecha_hasta:
            return {
                "Error": "La fecha Desde no puede ser posterior a la fecha Hasta."
            }, 400

        conn = conexion()
        cursor = conn.cursor(dictionary=True)

        # 1. Ventas totales: entradas + servicios.

        consulta_sql = """
            SELECT
                (
                    SELECT COALESCE(SUM(e.precio), 0)
                    FROM entradas e
                    JOIN compras c ON c.id = e.compra_id
                    WHERE c.fecha >= %s
                      AND c.fecha < DATE_ADD(%s, INTERVAL 1 DAY)
                      AND c.estado <> 'cancelada'
                      AND e.estado <> 'cancelada'
                )
                +
                (
                    SELECT COALESCE(
                        SUM(cs.cantidad * cs.precio_unitario), 0
                    )
                    FROM compra_servicios cs
                    JOIN compras c ON c.id = cs.compra_id
                    WHERE c.fecha >= %s
                      AND c.fecha < DATE_ADD(%s, INTERVAL 1 DAY)
                      AND c.estado <> 'cancelada'
                ) AS ventas_totales;
        """

        cursor.execute(
            consulta_sql,
            (
                fecha_desde,
                fecha_hasta,
                fecha_desde,
                fecha_hasta
            )
        )

        ventas = cursor.fetchone()

        # 2. Cantidad de entradas vendidas.

        consulta_sql = """
            SELECT COUNT(e.id) AS entradas_vendidas
            FROM entradas e
            JOIN compras c ON c.id = e.compra_id
            WHERE c.fecha >= %s
              AND c.fecha < DATE_ADD(%s, INTERVAL 1 DAY)
              AND c.estado <> 'cancelada'
              AND e.estado <> 'cancelada';
        """

        cursor.execute(
            consulta_sql,
            (fecha_desde, fecha_hasta)
        )

        entradas = cursor.fetchone()

        # 3. Entradas vendidas por género.

        consulta_sql = """
            SELECT
                g.id,
                g.nombre AS genero,
                COUNT(e.id) AS entradas_vendidas
            FROM entradas e
            JOIN compras c ON c.id = e.compra_id
            JOIN funciones f ON f.id = e.funcion_id
            JOIN pelicula_genero pg ON pg.pelicula_id = f.pelicula_id
            JOIN generos g ON g.id = pg.genero_id
            WHERE c.fecha >= %s
              AND c.fecha < DATE_ADD(%s, INTERVAL 1 DAY)
              AND c.estado <> 'cancelada'
              AND e.estado <> 'cancelada'
            GROUP BY g.id, g.nombre
            ORDER BY entradas_vendidas DESC;
        """

        cursor.execute(
            consulta_sql,
            (fecha_desde, fecha_hasta)
        )

        generos = cursor.fetchall()

        # Calcular el porcentaje de cada género.
        max_ventas = max(
            (genero["entradas_vendidas"] for genero in generos),
            default=0
        )

        for genero in generos:
            if max_ventas > 0:
                genero["porcentaje"] = round(
                    genero["entradas_vendidas"] * 100 / max_ventas,
                    1
                )
            else:
                genero["porcentaje"] = 0

        # 4. Ocupación de cada función activa.

        consulta_sql = """
            SELECT
                f.id AS funcion_id,
                p.titulo,
                s.local,
                s.nombre AS sala,
                f.inicio,
                COUNT(c.id) AS entradas_vendidas,
                (s.filas * s.columnas) AS capacidad,
                ROUND(
                    COUNT(c.id) * 100.0 /
                    NULLIF(s.filas * s.columnas, 0),
                    1
                ) AS ocupacion
            FROM funciones f
            JOIN peliculas p ON p.id = f.pelicula_id
            JOIN salas s ON s.id = f.sala_id
            LEFT JOIN entradas e
                ON e.funcion_id = f.id
                AND e.estado <> 'cancelada'
            LEFT JOIN compras c
                ON c.id = e.compra_id
                AND c.estado <> 'cancelada'
            WHERE f.estado = 'activa'
              AND f.inicio >= %s
              AND f.inicio < DATE_ADD(%s, INTERVAL 1 DAY)
            GROUP BY
                f.id,
                p.titulo,
                s.local,
                s.nombre,
                f.inicio,
                s.filas,
                s.columnas
            ORDER BY f.inicio ASC;
        """

        cursor.execute(
            consulta_sql,
            (fecha_desde, fecha_hasta)
        )

        ocupacion = cursor.fetchall()

        # 5. Calcular la ocupación promedio general.

        total_vendidas = sum(
            fila["entradas_vendidas"] for fila in ocupacion
        )

        capacidad_total = sum(
            fila["capacidad"] for fila in ocupacion
        )

        if capacidad_total > 0:
            ocupacion_promedio = round(
                (total_vendidas / capacidad_total) * 100,
                1
            )
        else:
            ocupacion_promedio = 0

        # 6. Preparar los datos para el frontend.

        datos = {
            "totales": {
                "ventas_totales": float(
                    ventas["ventas_totales"] or 0
                ),
                "entradas_vendidas": int(
                    entradas["entradas_vendidas"] or 0
                ),
                "ocupacion_promedio": ocupacion_promedio
            },
            "generos": generos,
            "ocupacion": ocupacion,
            "filtros": {
                "desde": fecha_desde.isoformat(),
                "hasta": fecha_hasta.isoformat()
            }
        }

        respuesta = {"OK": datos}, 200

    except Exception as e:
        respuesta = {"Error": str(e)}, 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return respuesta
