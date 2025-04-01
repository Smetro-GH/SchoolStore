// Funciones para el panel de administración

// Inicialización de componentes
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Inicializar popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Inicializar modales
    var modalTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="modal"]'))
    var modalList = modalTriggerList.map(function (modalTriggerEl) {
        return new bootstrap.Modal(modalTriggerEl)
    });

    // Inicializar dropdowns
    var dropdownTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'))
    var dropdownList = dropdownTriggerList.map(function (dropdownTriggerEl) {
        return new bootstrap.Dropdown(dropdownTriggerEl)
    });

    // Inicializar la barra lateral
    initSidebar();
});

// Funciones para la barra lateral
function initSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            sidebar.classList.toggle('active');
            content.classList.toggle('active');
        });
    }

    // Cerrar la barra lateral en dispositivos móviles al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('active');
                content.classList.remove('active');
            }
        }
    });
}

// Funciones para la gestión de productos
function confirmDeleteProduct(productId) {
    if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
        window.location.href = `/admin/products/${productId}/delete`;
    }
}

function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Funciones para la gestión de pedidos
function updateOrderStatus(orderId, status) {
    fetch(`/admin/orders/${orderId}/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar el estado en la interfaz
            const statusBadge = document.querySelector(`#order-${orderId} .status-badge`);
            if (statusBadge) {
                statusBadge.className = `badge status-badge ${getStatusClass(status)}`;
                statusBadge.textContent = getStatusText(status);
            }
        } else {
            alert('Error al actualizar el estado del pedido');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar el estado del pedido');
    });
}

function getStatusClass(status) {
    const classes = {
        'pending': 'bg-warning',
        'processing': 'bg-info',
        'shipped': 'bg-primary',
        'delivered': 'bg-success',
        'cancelled': 'bg-danger'
    };
    return classes[status] || 'bg-secondary';
}

function getStatusText(status) {
    const texts = {
        'pending': 'Pendiente',
        'processing': 'Procesando',
        'shipped': 'Enviado',
        'delivered': 'Entregado',
        'cancelled': 'Cancelado'
    };
    return texts[status] || status;
}

// Funciones para la gestión de usuarios
function updateUserRole(userId, role) {
    fetch(`/admin/users/${userId}/role`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ role: role })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar el rol en la interfaz
            const roleBadge = document.querySelector(`#user-${userId} .role-badge`);
            if (roleBadge) {
                roleBadge.className = `badge role-badge ${getRoleClass(role)}`;
                roleBadge.textContent = getRoleText(role);
            }
        } else {
            alert('Error al actualizar el rol del usuario');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar el rol del usuario');
    });
}

function getRoleClass(role) {
    const classes = {
        'admin': 'bg-danger',
        'staff': 'bg-warning',
        'user': 'bg-primary'
    };
    return classes[role] || 'bg-secondary';
}

function getRoleText(role) {
    const texts = {
        'admin': 'Administrador',
        'staff': 'Personal',
        'user': 'Usuario'
    };
    return texts[role] || role;
}

// Funciones para la configuración
function saveSettings(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch(`/admin/settings/${formId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', 'Configuración guardada correctamente');
        } else {
            showAlert('danger', 'Error al guardar la configuración');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Error al guardar la configuración');
    });
}

// Funciones de utilidad
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Funciones para la validación de formularios
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Funciones para la carga de archivos
function handleFileUpload(input, previewId) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        const maxSize = 5 * 1024 * 1024; // 5MB
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];

        if (file.size > maxSize) {
            showAlert('danger', 'El archivo es demasiado grande. El tamaño máximo es 5MB.');
            input.value = '';
            return;
        }

        if (!allowedTypes.includes(file.type)) {
            showAlert('danger', 'Tipo de archivo no permitido. Solo se permiten imágenes JPG, PNG y GIF.');
            input.value = '';
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            if (preview) {
                preview.src = e.target.result;
            }
        }
        reader.readAsDataURL(file);
    }
}

// Funciones para la paginación
function changePage(page) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('page', page);
    window.location.href = `${window.location.pathname}?${urlParams.toString()}`;
}

// Funciones para la búsqueda y filtrado
function filterTable(tableId, searchInput) {
    const table = document.getElementById(tableId);
    const searchText = searchInput.value.toLowerCase();
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let found = false;

        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell.textContent.toLowerCase().indexOf(searchText) > -1) {
                found = true;
                break;
            }
        }

        row.style.display = found ? '' : 'none';
    }
}

// Funciones para la exportación de datos
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.getElementsByTagName('tr');

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        const rowData = [];

        for (let j = 0; j < cells.length; j++) {
            rowData.push(cells[j].textContent.trim());
        }

        csv.push(rowData.join(','));
    }

    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
} 