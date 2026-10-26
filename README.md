# Cine Paradiso: entrega del Hito 1

**Proyecto Integrador** · Introducción al Desarrollo de Software, FIUBA (Cátedra Lanzillotta, 2.º cuatrimestre 2026)
**Fecha de entrega:** 26/10/2026

Sistema web de venta de entradas para los 3 locales de Cine Paradiso: cartelera, compra de entradas y servicios con pago simulado, un QR por compra para el ingreso a la sala y un Backoffice con dashboards. Se desarrolla con Flask (backend, frontend y Backoffice) y MySQL, sin ORM.

## Contenido

| Archivo | Qué contiene | Ítem del Hito 1 |
|---|---|---|
| [`alcance-y-supuestos.md`](alcance-y-supuestos.md) | Requisitos obligatorios del enunciado, los 25 supuestos del equipo (S1–S25), funcionalidades deseables, fuera de alcance y preguntas para el tutor. | a. Hipótesis o supuestos y alcance |
| [`product-backlog.md`](product-backlog.md) | 38 historias de usuario (PB-01 a PB-38) con criterios de aceptación, prioridad y estimación en Story Points, más la trazabilidad con los requisitos obligatorios. | a. Backlog de producto |
| [`Mockups.pdf`](Mockups.pdf) | 19 pantallas: 9 del front (incluidos el email y la vista mobile) y 10 del Backoffice. | a. Mockup del sitio web |
| [`init_db.sql`](Tablas.sql) | Script MySQL de creación de las 12 tablas y carga inicial (locales, salas, butacas, géneros y administrador). | b. Esquema de tablas |
| [`endpoints.md`](endpoints.md) | 36 endpoints de la API REST con verbo, ruta, rol, ejemplos JSON y errores, y su relación con cada pantalla del mockup. | c. Listado de endpoints |
| [`Proyecto integrador IDS 2026.pdf`](Proyecto%20integrador%20IDS%202026.pdf) | Enunciado oficial de la cátedra, usado como referencia para los requisitos obligatorios. | — |

## Orden de lectura sugerido

1. **`alcance-y-supuestos.md`**: qué hace el sistema y qué decisiones tomó el equipo.
2. **`Mockups.pdf`**: cómo se ve cada pantalla.
3. **`product-backlog.md`**: qué se va a construir y en qué orden.
4. **`endpoints.md`**: cómo se comunican el frontend y el backend.
5. **`init_db.sql`**: cómo se guardan los datos.

Los documentos están referenciados entre sí: los códigos **S1–S25** remiten a los supuestos, **PB-XX** a las historias del backlog y **M-n** a la página *n* de los mockups.

## Cómo consultar los archivos

- **Markdown (`.md`)**: se ven con formato directamente en GitHub o en VS Code (vista previa con `Ctrl+Shift+V`).
- **PDF**: cualquier visor de PDF o el navegador.
- **SQL**: cualquier editor de texto. Requiere MySQL 8.0.16 o superior. Crea la base `cine_paradiso` y no borra bases ni tablas existentes.

## Decisiones principales

- **Un único QR por compra**, con un token aleatorio de un solo uso (S16, S17).
- La cancelación afecta a la **compra completa** y se permite hasta 2 horas antes de la función (S13, S14).
- **Máximo 6 entradas** por compra (S3).
- **Pago simulado**, confirmado por el profesor (S1).
- **3 locales y sus salas fijos y precargados** en la base, sin ABM (S6).
- Películas **importadas desde TMDB** y guardadas en MySQL (S8, S9).
- **Web responsive**, sin app Kivy (S25).

