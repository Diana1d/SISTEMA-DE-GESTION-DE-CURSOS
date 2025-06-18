
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
    if (alerts.length > 0) {
        const myModal = new bootstrap.Modal(document.getElementById('modalNuevoUsuario'));
        myModal.show();
    }

    // 4. Inicializar DataTable (usa jQuery)
    $('#mi-tabla').DataTable({
        pagingType: 'simple',
        responsive: true,
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.3.2/i18n/es-ES.json'
        },
    })

    // 5. Mensaje al quere eliminar


    const modalEliminar = document.getElementById('modalConfirmarEliminar');
    const btnEliminar = document.getElementById('btnEliminar');

    modalEliminar.addEventListener('show.bs.modal', function (event) {
        const trigger = event.relatedTarget;
        const url = trigger.getAttribute('data-url');
        btnEliminar.setAttribute('href', url);
    });


});

