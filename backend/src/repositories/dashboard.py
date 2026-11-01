from db.conexion_db import *

def dashboard_repositories():
    conn = None
    cursor = None
    try:
        conn = conexion()
        cursor = conn.cursor(dictionary=True)

        # Guarda los resultados de cada consulta sql, separando servicios vendidos y otros datos
        resultados_consultas = []

        # Consulta para obtener la cantidad de servicios vendidos en el ultimo mes
        consulta_sql = """
        SELECT
            s.id,
            s.nombre,
            SUM(cs.cantidad)                      AS cantidad_vendida,
            SUM(cs.cantidad * cs.precio_unitario) AS ingresos
        FROM compra_servicios cs
        JOIN compras   c ON c.id = cs.compra_id
        JOIN servicios s ON s.id = cs.servicio_id
        WHERE c.fecha >= NOW() - INTERVAL 1 MONTH
            AND c.estado <> 'cancelada'
        GROUP BY s.id, s.nombre
        ORDER BY cantidad_vendida DESC;
        """
        cursor.execute(consulta_sql)
        resultado = cursor.fetchall()
        resultados_consultas.append(resultado)

        # Consulta para obtener la cantidad de entradas vendidas en el ultimo mes
        consulta_sql = """
        SELECT
            COUNT(e.id)                AS entradas_vendidas,
            COALESCE(SUM(e.precio), 0) AS ingresos
        FROM entradas e
        JOIN compras c ON c.id = e.compra_id
        WHERE c.fecha >= NOW() - INTERVAL 1 MONTH
            AND c.estado <> 'cancelada'
            AND e.estado <> 'cancelada';
        """
        cursor.execute(consulta_sql)
        resultado = cursor.fetchone()
        resultados_consultas.append(resultado)

        # Consulta para obtener la cantidad de ventas por genero de pelicula en el ultimo mes
        consulta_sql = """
        SELECT
            g.id,
            g.nombre                AS genero,
            COUNT(e.id)             AS entradas_vendidas,
            COALESCE(SUM(e.precio), 0) AS ingresos
        FROM entradas e
        JOIN compras         c  ON c.id  = e.compra_id
        JOIN funciones       f  ON f.id  = e.funcion_id
        JOIN pelicula_genero pg ON pg.pelicula_id = f.pelicula_id
        JOIN generos         g  ON g.id  = pg.genero_id
        WHERE c.fecha >= NOW() - INTERVAL 1 MONTH
            AND c.estado <> 'cancelada'
            AND e.estado <> 'cancelada'
        GROUP BY g.id, g.nombre
        ORDER BY entradas_vendidas DESC;
        """
        cursor.execute(consulta_sql)
        resultado = cursor.fetchall()
        resultados_consultas.append(resultado)

        # Consulta para obtener la cantidad de peliculas mas vendidas en el ultimo mes
        consulta_sql = """
        SELECT
            p.id,
            p.titulo,
            COUNT(e.id)    AS entradas_vendidas,
            SUM(e.precio)  AS ingresos
        FROM entradas e
        JOIN compras   c ON c.id = e.compra_id
        JOIN funciones f ON f.id = e.funcion_id
        JOIN peliculas p ON p.id = f.pelicula_id
        WHERE c.fecha >= NOW() - INTERVAL 1 MONTH
            AND c.estado <> 'cancelada'
            AND e.estado <> 'cancelada'
        GROUP BY p.id, p.titulo
        ORDER BY entradas_vendidas DESC
        LIMIT 10;
        """
        cursor.execute(consulta_sql)
        resultado = cursor.fetchall()
        resultados_consultas.append(resultado)

        respuesta = {"OK":resultados_consultas}, 200
    except Exception as e:
        respuesta = {"Error": str(e)}, 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return respuesta