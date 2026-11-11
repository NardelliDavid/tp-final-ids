const botonNuevoServicio = document.querySelector(".boton-nuevo-servicio");
const formularioServicio = document.querySelector("#formulario-servicio");
const formulario = document.querySelector("#form-nuevo-servicio");
const botonCancelar = document.querySelector("#cancelar-servicio");
const tituloFormulario = document.querySelector("#titulo-formulario");

const botonesEditar = document.querySelectorAll(".boton-editar");
const formulariosEliminar = document.querySelectorAll(".form-eliminar-servicio");

// Guardamos la ruta original para crear servicios
const urlCrear = formulario.dataset.urlCrear;

// Mostrar el formulario para crear un servicio
botonNuevoServicio.addEventListener("click", function() {
    formulario.reset();

    tituloFormulario.textContent = "Nuevo servicio";
    formulario.action = urlCrear;

    formularioServicio.hidden = false;
});

// Ocultar el formulario
botonCancelar.addEventListener("click", function() {
    formularioServicio.hidden = true;
    formulario.reset();
});

// Editar un servicio
botonesEditar.forEach(function(boton) {
    boton.addEventListener("click", function() {

        const id = boton.dataset.id;
        const nombre = boton.dataset.nombre;
        const descripcion = boton.dataset.descripcion;
        const precio = boton.dataset.precio;

        tituloFormulario.textContent = "Editar servicio";

        document.querySelector("#nombre").value = nombre;
        document.querySelector("#descripcion").value = descripcion;
        document.querySelector("#precio").value = precio;

        formulario.action = "/admin/servicios/editar/" + id;

        formularioServicio.hidden = false;

        // Llevar la pantalla hasta el formulario
        formularioServicio.scrollIntoView({ behavior: "smooth" });
    });
});

// Confirmar antes de eliminar un servicio
formulariosEliminar.forEach(function(formularioEliminar) {
    formularioEliminar.addEventListener("submit", function(evento) {

        const confirmar = confirm(
            "¿Estás segura de que querés eliminar este servicio?"
        );

        if (!confirmar) {
            evento.preventDefault();
        }
    });
});