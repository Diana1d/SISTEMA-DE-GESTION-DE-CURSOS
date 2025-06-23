document.addEventListener("DOMContentLoaded", function () {
    // 1. Hamburguesa menú lateral - MODIFICADO PARA FUNCIONAR CON DOCENTE
    const hamburger = document.querySelector("#toggle-btn");
    if (hamburger) {
        hamburger.addEventListener("click", function () {
            const sidebar = document.querySelector("#sidebar");
            const main = document.querySelector(".main");
            
            // Cambiamos de 'active' a 'expand' para el sidebar
            sidebar.classList.toggle("expand");
            
            // Verificamos si el main necesita la clase active
            if (main) {
                if (sidebar.classList.contains("expand")) {
                    main.classList.add("active");
                } else {
                    main.classList.remove("active");
                }
            }
        });
    }

    // 2. Cierre automático de flashes (igual que admin)
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alertEl => {
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
            alert.close();
        }, 3000);
    });

    // 3. Mostrar modal si hay alertas (igual que admin)
    const modales = document.querySelectorAll('.modal-auto-show');
    modales.forEach(function (modalElement) {
        if (modalElement.dataset.show === "true") {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    });

    // 4. Inicializar DataTable (similar pero con clase en lugar de ID)
    $('.table-datatable').DataTable({
        pagingType: 'simple',
        responsive: true,
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.3.2/i18n/es-ES.json'
        }
    });

    // 5. Mensaje al querer eliminar (versión mejorada)
    const modalEliminar = document.getElementById('modalConfirmacion');
    const btnEliminar = document.getElementById('btnConfirmar');
    
    if (modalEliminar && btnEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function (event) {
            const trigger = event.relatedTarget;
            if (trigger) {
                const url = trigger.getAttribute('data-url');
                const mensaje = trigger.getAttribute('data-message') || '¿Estás seguro de que deseas realizar esta acción?';
                
                document.getElementById('modalConfirmacionBody').textContent = mensaje;
                btnEliminar.onclick = function() {
                    if (url) window.location.href = url;
                };
            }
        });
    }

    // 6. Activar tooltips (específico de docente)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 7. Manejar dropdowns del sidebar (específico de docente) - MODIFICADO PARA MEJOR FUNCIONAMIENTO
    const dropdownTriggers = document.querySelectorAll('.sidebar-link.has-dropdown');
    dropdownTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const parentItem = this.closest('.sidebar-item');
            const dropdown = parentItem.querySelector('.sidebar-dropdown');
            
            // Cerrar otros dropdowns abiertos
            document.querySelectorAll('.sidebar-dropdown').forEach(item => {
                if (item !== dropdown) {
                    item.style.display = 'none';
                    item.previousElementSibling.classList.add('collapsed');
                    item.previousElementSibling.setAttribute('aria-expanded', 'false');
                }
            });
            
            // Alternar el actual
            if (dropdown.style.display === 'block') {
                dropdown.style.display = 'none';
                this.classList.add('collapsed');
                this.setAttribute('aria-expanded', 'false');
            } else {
                dropdown.style.display = 'block';
                this.classList.remove('collapsed');
                this.setAttribute('aria-expanded', 'true');
            }
        });
    });

    // Función global para mostrar confirmación (mantenida de docente original)
    window.mostrarConfirmacion = function(mensaje, callback) {
        const modalConfirmacion = bootstrap.Modal.getInstance(document.getElementById('modalConfirmacion')) || 
                                new bootstrap.Modal(document.getElementById('modalConfirmacion'));
        
        document.getElementById('modalConfirmacionBody').textContent = mensaje;
        document.getElementById('btnConfirmar').onclick = function() {
            if (callback) callback();
            modalConfirmacion.hide();
        };
        modalConfirmacion.show();
    };
});