// Main JavaScript for the application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            const closeButton = message.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000); // Auto-dismiss after 5 seconds
    });

    // Dynamic checklist items (for lawyer creating/editing case)
    const addDocumentBtn = document.getElementById('addDocumentBtn');
    if (addDocumentBtn) {
        addDocumentBtn.addEventListener('click', function() {
            const documentsList = document.getElementById('documentsList');
            const index = documentsList.children.length;
            
            const documentItem = document.createElement('div');
            documentItem.className = 'document-item card mb-3';
            documentItem.innerHTML = `
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-5 mb-2">
                            <label class="form-label">Nome do Documento</label>
                            <input type="text" class="form-control" name="document_name[]" required>
                        </div>
                        <div class="col-md-6 mb-2">
                            <label class="form-label">Descrição/Instruções</label>
                            <textarea class="form-control" name="document_description[]" rows="1"></textarea>
                        </div>
                        <div class="col-md-1 d-flex align-items-end mb-2">
                            <button type="button" class="btn btn-danger remove-document">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            documentsList.appendChild(documentItem);
            
            // Add event listener to remove button
            const removeBtn = documentItem.querySelector('.remove-document');
            removeBtn.addEventListener('click', function() {
                documentsList.removeChild(documentItem);
            });
        });
    }

    // Handle client selection in create case form
    const clientSelect = document.getElementById('clientSelect');
    const newClientFields = document.getElementById('newClientFields');
    
    if (clientSelect && newClientFields) {
        clientSelect.addEventListener('change', function() {
            if (this.value === 'new') {
                newClientFields.style.display = 'block';
            } else {
                newClientFields.style.display = 'none';
            }
        });
    }
});
