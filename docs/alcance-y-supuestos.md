# Cine Paradiso: alcance y supuestos

## 1. Supuestos

###  Resumen de supuestos

| Supuesto | Tema |
|---|---|
| S1 | Pago simulado |
| S2 | Comprobante de compra por email |
| S3 | Máximo de 6 entradas por compra |
| S4 | Precio por función |
| S5 | Servicios opcionales sin stock |
| S6 | Locales y salas fijos y precargados |
| S7 | Identificación de butacas |
| S8 | Importación de películas a MySQL |
| S9 | TMDB en español y clasificación manual |
| S10 | Período de cartelera |
| S11 | Creación manual de funciones |
| S12 | Reglas de las funciones |
| S13 | Cancelación hasta 2 horas antes |
| S14 | Cancelación de la compra completa |
| S15 | Cancelación con autenticación y confirmación |
| S16 | Un único QR por compra |
| S17 | Token aleatorio de un solo uso |
| S18 | Solo los administradores validan QR |
| S19 | Ventana de validación del QR |
| S20 | Registro de clientes |
| S21 | Administrador creado en la inicialización |
| S22 | Perfil y películas vistas |
| S23 | Sin reservas temporales de butacas |
| S24 | Moneda, zona horaria e idioma |
| S25 | Web responsive |

### Compra y pago

**S1. Pago simulado.** *(Confirmado por el profesor.)*
Los pagos son siempre simulados. No se integran pasarelas de pago reales (Mercado Pago, tarjetas). Al confirmar el checkout, la compra queda como pagada.
*Por qué:* el enunciado no pide pagos, e integrar una pasarela real agrega mucha complejidad y riesgo.

**S2. Comprobante de compra por email.**
Se envía por email un comprobante de compra con las entradas, los servicios, los precios, el total y el código QR de la compra. No se requiere factura fiscal (AFIP/ARCA).

**S3. Máximo de 6 entradas por compra.**
Cada compra incluye entre 1 y 6 entradas.
*Por qué:* es lo habitual en un cine (ir con amigos o en familia), y el límite evita abusos.

**S4. Precio por función.**
El precio se establece por función, y todas las butacas de esa función cuestan lo mismo. La experiencia "VIP" se vende como servicio, que es lo que propone el enunciado.
*Por qué:* permite, por ejemplo, que una función de matiné sea más barata, sin complicar el modelo.

**S5. Servicios opcionales, sin control de stock.**
Los servicios adicionales son opcionales, se compran junto con las entradas y no tienen control de stock.
*Por qué:* así hay un solo flujo de compra.

### Locales, salas y películas

**S6. Locales y salas fijos y precargados.**
Los 3 locales y sus salas son fijos: se precargan en MySQL con el script SQL y no se crean, modifican ni eliminan desde el sistema. No hay ABM de locales ni de salas.
*Por qué:* el enunciado dice que el cine "tiene" 3 locales, como un dato fijo. Lo que el administrador configura es qué película se proyecta en cada sala.

**S7. Identificación de las butacas.**
Las filas se identifican con letras y las columnas con números (por ejemplo, C7). Las salas tienen una distribución rectangular y todas las butacas son del mismo tipo.
*Por qué:* permite dibujar la sala como una grilla, algo fácil de hacer en HTML sin JavaScript.

**S8. Importación de películas a MySQL.**
El administrador importa las películas desde una API externa y las guarda en MySQL. Después puede modificar la sinopsis y el póster. La cartelera consulta nuestra base de datos, no la API externa.
*Por qué:* si la API se cae o se agota la cuota gratuita, la cartelera sigue funcionando. Además, es más rápido.

**S9. TMDB en español y clasificación manual.**
Se usa TMDB y se le pide la información en español. El administrador elige a mano la clasificación por edades.
*Por qué:* TMDB devuelve los datos en español. OMDb los devuelve en inglés y con la clasificación de Estados Unidos (PG-13, R), que no corresponde a la Argentina.

**S10. Período de cartelera.**
Cada película tiene un período de cartelera con fecha de inicio y fecha de fin. Las funciones tienen que programarse dentro de ese período.

### Funciones

**S11. Creación manual de funciones.**
El administrador crea a mano cada función, indicando la película, la sala, la fecha y hora (en un único campo `DATETIME`) y el precio.

**S12. Reglas de las funciones.**

- Tienen que respetar el período de cartelera de la película.
- No pueden superponerse en la misma sala.
- Tienen que dejar 20 minutos de limpieza entre una proyección y la siguiente.

### Cancelaciones

**S13. Cancelación hasta 2 horas antes.**
Una compra se puede cancelar hasta 2 horas antes del inicio de la función.

**S14. Cancelación de la compra completa.**
La cancelación afecta a la compra completa, con todas sus entradas y servicios. Las butacas se liberan y el QR de la compra se invalida. Como el pago es simulado (S1), no hay devolución real de dinero: la compra solo cambia de estado.

**S15. Cancelación con autenticación y confirmación.**
El botón del correo abre una página de Cine Paradiso, donde el cliente tiene que autenticarse y confirmar la cancelación. **Abrir el enlace no cancela la compra automáticamente.**
*Por qué:* si el enlace cancelara directamente, cualquiera que viera el mail (o un antivirus que revisa los enlaces) podría cancelar la compra sin querer.

### Códigos QR

**S16. Un único QR por compra.** *(Decisión definitiva del grupo.)*
Cada compra tiene un único código QR, que cubre todas sus entradas. Al validarlo, la compra completa queda como utilizada y todas sus entradas ingresan juntas. Si se cancela la compra, el QR deja de ser válido (S14).

**S17. Token aleatorio de un solo uso.**
Cada compra tiene un token aleatorio, único y seguro, generado en Python, que es lo que se codifica en el QR. El backend verifica que cada QR se pueda usar una sola vez.
*Por qué:* si el QR tuviera un número correlativo (1, 2, 3...), cualquiera podría fabricar QR falsos.

**S18. Solo los administradores validan QR.**
Solamente los administradores pueden escanear y validar códigos QR, desde el Backoffice. No se agrega un rol de "boletero".

**S19. Ventana de validación.**
Los QR se pueden validar desde 60 minutos antes hasta 30 minutos después del inicio de la función.

### Usuarios

**S20. Registro de clientes.**
Los clientes se registran con nombre, correo electrónico (único) y contraseña. La contraseña se guarda protegida con un hash seguro. El backend asigna el rol cliente.

**S21. Administrador creado en la inicialización.**
La cuenta del administrador se crea al inicializar el sistema, con la contraseña protegida con un hash seguro. No hay registro público de administradores.

**S22. Perfil y películas vistas.**

- El perfil muestra todas las compras del usuario con sus estados ("consumos").
- Una película aparece como **vista** si se validó el QR de al menos una compra del usuario para esa película.

**Limitación:** este criterio **no prueba que el comprador haya asistido en persona**. El QR habilita el ingreso de toda la compra, así que la película figura como vista para el comprador aunque hayan ingresado solo sus acompañantes.

### Concurrencia y configuración

**S23. Sin reservas temporales de butacas.**
No hay reservas temporales: las butacas se asignan al confirmar la compra. MySQL tiene que impedir ventas duplicadas, incluso cuando dos compras se hacen al mismo tiempo.
*Por qué:* las reservas con temporizador ("tenés 10 minutos") son complejas. La base de datos puede garantizar por sí sola que una butaca no se venda dos veces.

**S24. Moneda, zona horaria e idioma.**
Moneda: pesos argentinos (ARS). Zona horaria: Argentina. Idioma: español.

**S25. Web responsive.**
Se desarrolla una web responsive con Flask, HTML, CSS, Jinja2 y Bootstrap, que se adapta a computadoras, tablets y celulares. No se desarrolla una app con Kivy.
*Por qué:* así hay un solo frontend en lugar de dos.

## Dentro del alcance


### Cliente
- El Cliente podra entrar a la aplicacion, ver las peliculas disponibles y los servicios sin tener una cuenta registrada
- El Cliente podra crearse una cuenta, ingresar a la cuenta creada y tambien podra eliminarla
- El cliente podra elegir las peliculas disponibles, los asientos y servicios q desee consumir
- El cliente podra ver el resumen de sus compras con detalle de q servicios se consumieron, q peliculas vio en que fecha y cuantos asientos reservo por funcion

### Desarrollador

- Podra entrar al backoffice para programar las peliculas
- Podra dar de baja servicios o peliculas

### Fuera de alcance

Lo siguiente **no** se va a desarrollar. Surge de los supuestos anteriores:

- Pagos reales 
- Factura fiscal 
- Recuperación de contraseña.
- Verificación de email al registrarse.
- Reserva temporal de butacas 
- Promociones y descuentos
- Butacas especiales, como accesibles o dobles
