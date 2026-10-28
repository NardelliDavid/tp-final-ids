# tp-final-ids · Group 404

## Cine Paradiso: entrega del Hito 1

**Proyecto Integrador** · Introducción al Desarrollo de Software, FIUBA (Cátedra Lanzillotta, 2.º cuatrimestre 2026)
**Fecha de entrega:** 26/10/2026

Sistema web de venta de entradas para los 3 locales de Cine Paradiso: cartelera, compra de entradas y servicios con pago simulado, un QR por compra para el ingreso a la sala y un Backoffice con dashboards.

## Integrantes

- David Joel Nardelli
- Ariadna Fadda
- Eduardo Mamani
- Frank Perez
- Jerónimo Naveira
- José Toro
- Milagros Borgstrand
- Lorena Franco
- Sofía Bariego
- Valentino Carrera

## Organización del trabajo

- **Tablero Kanban con el backlog:** *Estamos usando github projects.*
- **Estrategia de ramas y convención de commits:** *Se utilizarán dos ramas principales: main y develop. Los cambios se integrarán en develop mediante Pull Requests (PR), mientras que únicamente el propietario del repositorio podrá realizar pushes directamente a main. Para desarrollar tareas específicas, se utilizarán ramas feature.*

## Contenido

La documentación del Hito 1 está en la carpeta [`docs/`](docs/).

| Archivo | Qué contiene | Ítem del Hito 1 |
|---|---|---|
| [`docs/alcance-y-supuestos.md`](docs/alcance-y-supuestos.md) | Requisitos obligatorios del enunciado, los 25 supuestos del equipo (S1–S25), funcionalidades deseables, fuera de alcance y preguntas para el tutor. | a. Hipótesis o supuestos y alcance |
| [`docs/product-backlog.md`](docs/product-backlog.md) | 38 historias de usuario (PB-01 a PB-38) con criterios de aceptación, prioridad y estimación en Story Points, más la trazabilidad con los requisitos obligatorios. | a. Backlog de producto |
| [`docs/Mockups.pdf`](docs/Mockups.pdf) | 19 pantallas: 9 del front (incluidos el email y la vista mobile) y 10 del Backoffice. | a. Mockup del sitio web |
| [`docs/endpoints.md`](docs/endpoints.md) | 36 endpoints de la API REST con verbo, ruta, rol, ejemplos JSON y errores, y su relación con cada pantalla del mockup. | c. Listado de endpoints |
| [`docs/Proyecto integrador IDS 2026.pdf`](docs/Proyecto%20integrador%20IDS%202026.pdf) | Enunciado oficial de la cátedra, usado como referencia para los requisitos obligatorios. | — |

## Orden de lectura sugerido

1. **`alcance-y-supuestos.md`**: qué hace el sistema y qué decisiones tomó el equipo.
2. **`Mockups.pdf`**: cómo se ve cada pantalla.
3. **`product-backlog.md`**: qué se va a construir y en qué orden.
4. **`endpoints.md`**: cómo se comunican el frontend y el backend.

Los documentos están referenciados entre sí: los códigos **S1–S25** remiten a los supuestos, **PB-XX** a las historias del backlog y **M-n** a la página *n* de los mockups.

## Cómo consultar los archivos

- **Markdown (`.md`)**: se ven con formato directamente en GitHub o en VS Code (vista previa con `Ctrl+Shift+V`).
- **PDF**: cualquier visor de PDF o el navegador.
- **SQL**: cualquier editor de texto. `backend/db/init_db.sql` es el único script de base de datos del proyecto. Requiere MySQL 8.0.16 o superior. Crea la base `cine_paradiso` y no borra bases ni tablas existentes: si las tablas ya existen, se detiene con un error sin modificar nada.

## Decisiones principales

- **Un único QR por compra**, mas un codigo para ingresarlo manualmente.
- La cancelación afecta a la **compra completa** y se permite hasta 2 horas antes de la función (S13, S14).
- **Máximo 6 entradas** por compra (S3).
- **Pago simulado**, confirmado por el profesor (S1).
- **3 locales y sus salas fijos y precargados** en la base, sin ABM (S6).
- Películas **importadas desde TMDB** y guardadas en MySQL (S8, S9).
- **Web responsive**, sin app Kivy (S25). Utilizamos HTML, CSS, JavaScript, Python, Flask, Jinja y de base de datos MySQL.

## Levantar el sistema

1. Abrimos una terminal dentro de **tp-final-ids**
2. En la terminal ejecutamos `python3 -m venv venv` y entramos a la carpeta del entorno virtual
3. Activamos el entorno virtual con `source venv/bin/activate` (Esto es en Linux)
4. Con el entorno virtual activado ejecutamos `pip install -r requirements.txt`
5. Abrimos otra terminal y activamos el entorno virtual, tienen que haber 2 terminales, una para levantar el backend y otra para levantar el frontend.
6. En una terminal navegamos con cd hasta la carpeta del backend y en la otra hasta la del frontend
7. En ambas terminales ejecutamos `python app.py` y se van a levantar el frontend y el backend.

Nota: en el archivo **conexion_db.py** van a tener que modificar el usuario y contraseña si corresponde para que se pueda conectar a la base de datos. El archivo **init_db.sql** contiene las tablas y datos iniciales para la creacion de la base de datos.