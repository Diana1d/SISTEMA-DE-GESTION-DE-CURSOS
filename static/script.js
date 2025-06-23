
document.addEventListener("DOMContentLoaded", function () {
    // 1. Hamburguesa menú lateral
    const hamburger = document.querySelector("#toggle-btn");
    if (hamburger) {
        hamburger.addEventListener("click", function () {
            document.querySelector("#sidebar").classList.toggle("expand");
        });
    }

    // 2. Cierre automático de flashes
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alertEl => {
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
            alert.close();
        }, 3000);
    });

    // 3. Mostrar modal si hay alertas
    // Obtiene los parámetros de la URL (por ejemplo: ?show_modal=true)
    const urlParams = new URLSearchParams(window.location.search);

    // Verifica si el parámetro show_modal está presente y es igual a "true"
    const showModal = urlParams.get("show_modal");

    // Si la condición se cumple, procede a mostrar los modales
    if (showModal === "true") {

        // Busca todos los elementos con la clase "modal-auto-show"
        const modales = document.querySelectorAll('.modal-auto-show');

        // Recorre cada modal encontrado y lo muestra
        modales.forEach(function (modalElement) {
            // Crea una nueva instancia del modal usando Bootstrap
            const modal = new bootstrap.Modal(modalElement);

            // Muestra el modal
            modal.show();
        });
    }
    // 4. Inicializar DataTable (usa jQuery)
    $(document).ready(function () {
        $('#mi-tabla').DataTable({
            pagingType: 'simple',
            responsive: true,
            language: {
                url: 'https://cdn.datatables.net/plug-ins/2.3.2/i18n/es-ES.json'
            },
        });
    });

    // 5. Mensaje al quere eliminar


    const modalEliminar = document.getElementById('modalConfirmarEliminar');
    const btnEliminar = document.getElementById('btnEliminar');

    modalEliminar.addEventListener('show.bs.modal', function (event) {
        const trigger = event.relatedTarget;
        const url = trigger.getAttribute('data-url');
        btnEliminar.setAttribute('href', url);
    });
});

/* DOCENTE */


