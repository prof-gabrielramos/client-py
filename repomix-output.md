This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.github/
  workflows/
    close-issues.yml
    publish.yml
    testing.yml
android_sms_gateway/
  __init__.py
  ahttp.py
  client.py
  constants.py
  domain.py
  encryption.py
  enums.py
  http.py
sms-gateway-web/
  templates/
    base.html
    contacts.html
    dashboard.html
    login.html
    messages.html
    send.html
    settings.html
    webhooks.html
  app.py
  README.md
  requirements.txt
  run.py
tests/
  test_client.py
  test_domain.py
  test_encryption.py
.flake8
.gitignore
.isort.cfg
LICENSE
Makefile
Pipfile
pyproject.toml
README.md
requirements.txt
```

# Files

## File: sms-gateway-web/templates/base.html
````html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SMS Gateway{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #007BFF;
            --success-color: #28A745;
            --warning-color: #FFC107;
            --danger-color: #DC3545;
            --light-bg: #F8F9FA;
            --dark-text: #212529;
        }
        
        body {
            font-family: 'Inter', 'Roboto', sans-serif;
            background-color: var(--light-bg);
            color: var(--dark-text);
        }
        
        .navbar {
            background-color: var(--primary-color) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: 600;
        }
        
        .card {
            border: none;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 24px;
        }
        
        .card-header {
            background-color: white;
            border-bottom: 1px solid #e9ecef;
            border-radius: 12px 12px 0 0 !important;
            padding: 16px 24px;
        }
        
        .card-body {
            padding: 24px;
        }
        
        .btn {
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-success {
            background-color: var(--success-color);
            border-color: var(--success-color);
        }
        
        .btn-warning {
            background-color: var(--warning-color);
            border-color: var(--warning-color);
        }
        
        .btn-danger {
            background-color: var(--danger-color);
            border-color: var(--danger-color);
        }
        
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .status-pending {
            background-color: #fff3cd;
            color: #856404;
        }
        
        .status-processed {
            background-color: #cce5ff;
            color: #004085;
        }
        
        .status-sent {
            background-color: #d4edda;
            color: #155724;
        }
        
        .status-delivered {
            background-color: #d1ecf1;
            color: #0c5460;
        }
        
        .status-failed {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .sidebar {
            background-color: white;
            min-height: calc(100vh - 76px);
            border-right: 1px solid #e9ecef;
        }
        
        .sidebar .nav-link {
            color: var(--dark-text);
            padding: 12px 20px;
            border-radius: 8px;
            margin: 4px 8px;
            transition: all 0.2s;
        }
        
        .sidebar .nav-link:hover {
            background-color: var(--light-bg);
            color: var(--primary-color);
        }
        
        .sidebar .nav-link.active {
            background-color: var(--primary-color);
            color: white;
        }
        
        .main-content {
            padding: 24px;
        }
        
        .stats-card {
            text-align: center;
            padding: 20px;
        }
        
        .stats-number {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .stats-label {
            color: #6c757d;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .form-control, .form-select {
            border-radius: 8px;
            border: 1px solid #ced4da;
            padding: 12px 16px;
        }
        
        .form-control:focus, .form-select:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        }
        
        .alert {
            border-radius: 8px;
            border: none;
        }
        
        .table {
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .table th {
            background-color: var(--light-bg);
            border-bottom: 1px solid #dee2e6;
            font-weight: 600;
            color: var(--dark-text);
        }
        
        .loading {
            display: none;
        }
        
        .loading.show {
            display: inline-block;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="fas fa-sms me-2"></i>
                SMS Gateway
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/settings">
                            <i class="fas fa-cog me-1"></i>
                            Configurações
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 sidebar">
                <nav class="nav flex-column pt-3">
                    <a class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}" href="/">
                        <i class="fas fa-tachometer-alt me-2"></i>
                        Dashboard
                    </a>
                    <a class="nav-link {% if request.endpoint == 'send_page' %}active{% endif %}" href="/send">
                        <i class="fas fa-paper-plane me-2"></i>
                        Enviar SMS
                    </a>
                    <a class="nav-link {% if request.endpoint == 'messages' %}active{% endif %}" href="/messages">
                        <i class="fas fa-envelope me-2"></i>
                        Mensagens
                    </a>
                    <a class="nav-link {% if request.endpoint == 'contacts' %}active{% endif %}" href="/contacts">
                        <i class="fas fa-address-book me-2"></i>
                        Contatos
                    </a>
                    <a class="nav-link {% if request.endpoint == 'webhooks' %}active{% endif %}" href="/webhooks">
                        <i class="fas fa-webhook me-2"></i>
                        Webhooks
                    </a>
                </nav>
            </div>

            <!-- Main Content -->
            <div class="col-md-9 col-lg-10 main-content">
                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        {% for category, message in messages %}
                            <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}

                {% block content %}{% endblock %}
            </div>
        </div>
    </div>

    <!-- Toast Container -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <div id="toast" class="toast" role="alert">
            <div class="toast-header">
                <i class="fas fa-info-circle text-primary me-2"></i>
                <strong class="me-auto">Notificação</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body" id="toast-body">
                <!-- Toast message will be inserted here -->
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Utility functions
        function showToast(message, type = 'info') {
            const toast = document.getElementById('toast');
            const toastBody = document.getElementById('toast-body');
            const toastHeader = toast.querySelector('.toast-header i');
            
            toastBody.textContent = message;
            
            // Update icon and color based on type
            toastHeader.className = `fas me-2 ${
                type === 'success' ? 'fa-check-circle text-success' :
                type === 'error' ? 'fa-exclamation-circle text-danger' :
                type === 'warning' ? 'fa-exclamation-triangle text-warning' :
                'fa-info-circle text-primary'
            }`;
            
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
        }

        function formatPhoneNumber(phone) {
            // Simple Brazilian phone number formatting
            const cleaned = phone.replace(/\D/g, '');
            if (cleaned.length === 11) {
                return `(${cleaned.slice(0,2)}) ${cleaned.slice(2,7)}-${cleaned.slice(7)}`;
            } else if (cleaned.length === 10) {
                return `(${cleaned.slice(0,2)}) ${cleaned.slice(2,6)}-${cleaned.slice(6)}`;
            }
            return phone;
        }

        function getStatusBadge(status) {
            const statusMap = {
                'Pending': { class: 'status-pending', text: 'Pendente' },
                'Processed': { class: 'status-processed', text: 'Processando' },
                'Sent': { class: 'status-sent', text: 'Enviado' },
                'Delivered': { class: 'status-delivered', text: 'Entregue' },
                'Failed': { class: 'status-failed', text: 'Falhou' }
            };
            
            const statusInfo = statusMap[status] || { class: 'status-pending', text: status };
            return `<span class="status-badge ${statusInfo.class}">${statusInfo.text}</span>`;
        }

        function formatDateTime(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString('pt-BR');
        }
    </script>
    
    {% block scripts %}{% endblock %}
</body>
</html>
````

## File: sms-gateway-web/templates/contacts.html
````html
{% extends "base.html" %}

{% block title %}Contatos - SMS Gateway{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">Contatos</h1>
    <button class="btn btn-primary" onclick="showAddContactModal()">
        <i class="fas fa-plus me-2"></i>
        Adicionar Contato
    </button>
</div>

<div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">
            <i class="fas fa-address-book me-2"></i>
            Lista de Contatos
        </h5>
        <div class="input-group input-group-sm" style="width: 250px;">
            <span class="input-group-text">
                <i class="fas fa-search"></i>
            </span>
            <input type="text" class="form-control" id="searchInput" placeholder="Buscar por nome ou número..." 
                   onkeyup="filterContacts()">
        </div>
    </div>
    <div class="card-body">
        {% if contacts %}
            <div class="table-responsive">
                <table class="table table-hover" id="contactsTable">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Telefone</th>
                            <th>Grupo</th>
                            <th>Notas</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for contact in contacts %}
                        <tr data-id="{{ loop.index }}" data-name="{{ contact[0].lower() }}" data-phone="{{ contact[1].lower() }}">
                            <td>{{ contact[0] }}</td>
                            <td>{{ contact[1] }}</td>
                            <td>{{ contact[2] if contact[2] else '-' }}</td>
                            <td>
                                <div class="text-truncate" style="max-width: 200px;" title="{{ contact[3] if contact[3] else '' }}">
                                    {{ contact[3] if contact[3] else '-' }}
                                </div>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary" onclick="showEditContactModal('{{ loop.index }}')">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger" onclick="showDeleteContactModal('{{ loop.index }}')">
                                    <i class="fas fa-trash"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-info" onclick="sendMessageToContact('{{ loop.index }}')">
                                    <i class="fas fa-paper-plane"></i>
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="text-center py-5">
                <i class="fas fa-address-book fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">Nenhum contato encontrado</h5>
                <p class="text-muted">Adicione contatos para enviar mensagens rapidamente.</p>
                <button class="btn btn-primary" onclick="showAddContactModal()">
                    <i class="fas fa-plus me-2"></i>
                    Adicionar Primeiro Contato
                </button>
            </div>
        {% endif %}
    </div>
</div>

<!-- Add Contact Modal -->
<div class="modal fade" id="addContactModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Adicionar Novo Contato</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="addContactForm">
                    <div class="mb-3">
                        <label for="addName" class="form-label">Nome *</label>
                        <input type="text" class="form-control" id="addName" required>
                    </div>
                    <div class="mb-3">
                        <label for="addPhone" class="form-label">Número de Telefone *</label>
                        <input type="tel" class="form-control" id="addPhone" placeholder="+5511999999999" required>
                        <div class="form-text">
                            Digite o número no formato internacional (+55...) ou nacional.
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="addGroup" class="form-label">Grupo</label>
                        <input type="text" class="form-control" id="addGroup" placeholder="Ex: Família, Trabalho">
                    </div>
                    <div class="mb-3">
                        <label for="addNotes" class="form-label">Notas</label>
                        <textarea class="form-control" id="addNotes" rows="3" placeholder="Informações adicionais sobre o contato"></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-primary" id="saveAddContactBtn" onclick="saveNewContact()">
                    <i class="fas fa-save me-2"></i>
                    Salvar Contato
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Edit Contact Modal -->
<div class="modal fade" id="editContactModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Editar Contato</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="editContactForm">
                    <input type="hidden" id="editContactId">
                    <div class="mb-3">
                        <label for="editName" class="form-label">Nome *</label>
                        <input type="text" class="form-control" id="editName" required>
                    </div>
                    <div class="mb-3">
                        <label for="editPhone" class="form-label">Número de Telefone *</label>
                        <input type="tel" class="form-control" id="editPhone" required>
                        <div class="form-text">
                            Digite o número no formato internacional (+55...) ou nacional.
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="editGroup" class="form-label">Grupo</label>
                        <input type="text" class="form-control" id="editGroup">
                    </div>
                    <div class="mb-3">
                        <label for="editNotes" class="form-label">Notas</label>
                        <textarea class="form-control" id="editNotes" rows="3"></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-primary" id="saveEditContactBtn" onclick="saveEditedContact()">
                    <i class="fas fa-save me-2"></i>
                    Salvar Alterações
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Delete Contact Modal -->
<div class="modal fade" id="deleteContactModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title">
                    <i class="fas fa-trash me-2"></i>
                    Excluir Contato
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <input type="hidden" id="deleteContactId">
                <p>Você tem certeza que deseja excluir este contato?</p>
                <p><strong id="deleteContactName"></strong>: <span id="deleteContactPhone"></span></p>
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Esta ação não pode ser desfeita.
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteBtn" onclick="deleteContact()">
                    <i class="fas fa-trash me-2"></i>
                    Excluir
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Filter contacts
    function filterContacts() {
        const searchText = document.getElementById('searchInput').value.toLowerCase();
        const rows = document.querySelectorAll('#contactsTable tbody tr');
        
        rows.forEach(row => {
            const name = row.dataset.name;
            const phone = row.dataset.phone;
            const show = searchText === '' || name.includes(searchText) || phone.includes(searchText);
            row.style.display = show ? '' : 'none';
        });
    }

    // Show add contact modal
    function showAddContactModal() {
        const modal = new bootstrap.Modal(document.getElementById('addContactModal'));
        document.getElementById('addContactForm').reset();
        modal.show();
    }

    // Save new contact
    function saveNewContact() {
        const form = document.getElementById('addContactForm');
        const saveBtn = document.getElementById('saveAddContactBtn');
        
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        const data = {
            name: document.getElementById('addName').value,
            phone: document.getElementById('addPhone').value,
            group: document.getElementById('addGroup').value || '',
            notes: document.getElementById('addNotes').value || ''
        };
        
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Salvando...';
        
        fetch('/api/contacts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro ao adicionar contato: ' + result.error, 'error');
                return;
            }
            
            showToast('Contato adicionado com sucesso!', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('addContactModal'));
            modal.hide();
            location.reload();
        })
        .catch(error => {
            showToast('Erro ao adicionar contato: ' + error.message, 'error');
        })
        .finally(() => {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>Salvar Contato';
        });
    }

    // Show edit contact modal
    function showEditContactModal(contactId) {
        const modal = new bootstrap.Modal(document.getElementById('editContactModal'));
        const row = document.querySelector(`#contactsTable tr[data-id="${contactId}"]`);
        
        document.getElementById('editContactId').value = contactId;
        document.getElementById('editName').value = row.cells[0].textContent;
        document.getElementById('editPhone').value = row.cells[1].textContent;
        document.getElementById('editGroup').value = row.cells[2].textContent === '-' ? '' : row.cells[2].textContent;
        document.getElementById('editNotes').value = row.cells[3].textContent === '-' ? '' : row.cells[3].textContent;
        
        modal.show();
    }

    // Save edited contact
    function saveEditedContact() {
        const form = document.getElementById('editContactForm');
        const saveBtn = document.getElementById('saveEditContactBtn');
        
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        const contactId = document.getElementById('editContactId').value;
        const data = {
            name: document.getElementById('editName').value,
            phone: document.getElementById('editPhone').value,
            group: document.getElementById('editGroup').value || '',
            notes: document.getElementById('editNotes').value || ''
        };
        
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Salvando...';
        
        fetch(`/api/contacts/${contactId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro ao atualizar contato: ' + result.error, 'error');
                return;
            }
            
            showToast('Contato atualizado com sucesso!', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('editContactModal'));
            modal.hide();
            location.reload();
        })
        .catch(error => {
            showToast('Erro ao atualizar contato: ' + error.message, 'error');
        })
        .finally(() => {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>Salvar Alterações';
        });
    }

    // Show delete contact modal
    function showDeleteContactModal(contactId) {
        const modal = new bootstrap.Modal(document.getElementById('deleteContactModal'));
        const row = document.querySelector(`#contactsTable tr[data-id="${contactId}"]`);
        
        document.getElementById('deleteContactId').value = contactId;
        document.getElementById('deleteContactName').textContent = row.cells[0].textContent;
        document.getElementById('deleteContactPhone').textContent = row.cells[1].textContent;
        
        modal.show();
    }

    // Delete contact
    function deleteContact() {
        const contactId = document.getElementById('deleteContactId').value;
        const deleteBtn = document.getElementById('confirmDeleteBtn');
        
        deleteBtn.disabled = true;
        deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Excluindo...';
        
        fetch(`/api/contacts/${contactId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro ao excluir contato: ' + result.error, 'error');
                return;
            }
            
            showToast('Contato excluído com sucesso!', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('deleteContactModal'));
            modal.hide();
            location.reload();
        })
        .catch(error => {
            showToast('Erro ao excluir contato: ' + error.message, 'error');
        })
        .finally(() => {
            deleteBtn.disabled = false;
            deleteBtn.innerHTML = '<i class="fas fa-trash me-2"></i>Excluir';
        });
    }

    // Send message to contact
    function sendMessageToContact(contactId) {
        const row = document.querySelector(`#contactsTable tr[data-id="${contactId}"]`);
        const phoneNumber = row.cells[1].textContent;
        
        // Redirect to send page with pre-filled phone number
        window.location.href = `/send?phone=${encodeURIComponent(phoneNumber)}`;
    }
</script>
{% endblock %}
````

## File: sms-gateway-web/templates/dashboard.html
````html
{% extends "base.html" %}

{% block title %}Dashboard - SMS Gateway{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">Dashboard</h1>
    <a href="/send" class="btn btn-primary">
        <i class="fas fa-paper-plane me-2"></i>
        Enviar SMS
    </a>
</div>

<!-- Statistics Cards -->
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card">
            <div class="card-body stats-card">
                <div class="stats-number text-primary">{{ stats.get('Pending', 0) + stats.get('Processed', 0) }}</div>
                <div class="stats-label">Pendentes</div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body stats-card">
                <div class="stats-number text-success">{{ stats.get('Sent', 0) + stats.get('Delivered', 0) }}</div>
                <div class="stats-label">Enviadas</div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body stats-card">
                <div class="stats-number text-info">{{ stats.get('Delivered', 0) }}</div>
                <div class="stats-label">Entregues</div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body stats-card">
                <div class="stats-number text-danger">{{ stats.get('Failed', 0) }}</div>
                <div class="stats-label">Falharam</div>
            </div>
        </div>
    </div>
</div>

<!-- Charts Row -->
<div class="row mb-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-chart-line me-2"></i>
                    Status das Mensagens (Últimos 7 dias)
                </h5>
            </div>
            <div class="card-body">
                <canvas id="statusChart" height="100"></canvas>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-chart-pie me-2"></i>
                    Distribuição
                </h5>
            </div>
            <div class="card-body">
                <canvas id="distributionChart"></canvas>
            </div>
        </div>
    </div>
</div>

<!-- Recent Messages -->
<div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">
            <i class="fas fa-clock me-2"></i>
            Mensagens Recentes
        </h5>
        <a href="/messages" class="btn btn-outline-primary btn-sm">Ver Todas</a>
    </div>
    <div class="card-body">
        {% if recent_messages %}
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Mensagem</th>
                            <th>Destinatários</th>
                            <th>Status</th>
                            <th>Data</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for message in recent_messages %}
                        <tr>
                            <td>
                                <div class="text-truncate" style="max-width: 200px;" title="{{ message[1] }}">
                                    {{ message[1] }}
                                </div>
                            </td>
                            <td>
                                <span class="badge bg-secondary">Múltiplos</span>
                            </td>
                            <td>
                                <span class="status-badge status-{{ message[3].lower() }}">
                                    {% if message[3] == 'Pending' %}Pendente
                                    {% elif message[3] == 'Processed' %}Processando
                                    {% elif message[3] == 'Sent' %}Enviado
                                    {% elif message[3] == 'Delivered' %}Entregue
                                    {% elif message[3] == 'Failed' %}Falhou
                                    {% else %}{{ message[3] }}
                                    {% endif %}
                                </span>
                            </td>
                            <td>
                                <small class="text-muted">{{ message[4] }}</small>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary" onclick="viewMessageDetails('{{ message[0] }}')">
                                    <i class="fas fa-eye"></i>
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="text-center py-4">
                <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">Nenhuma mensagem encontrada</h5>
                <p class="text-muted">Comece enviando sua primeira mensagem SMS.</p>
                <a href="/send" class="btn btn-primary">
                    <i class="fas fa-paper-plane me-2"></i>
                    Enviar Primeira Mensagem
                </a>
            </div>
        {% endif %}
    </div>
</div>

<!-- Message Details Modal -->
<div class="modal fade" id="messageModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Detalhes da Mensagem</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="messageModalBody">
                <div class="text-center">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Status Chart
    const statusCtx = document.getElementById('statusChart').getContext('2d');
    const statusData = JSON.parse('{{ stats|tojson|safe }}');
    
    new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: ['Pendentes', 'Enviadas', 'Entregues', 'Falharam'],
            datasets: [{
                data: [
                    (statusData.Pending || 0) + (statusData.Processed || 0),
                    statusData.Sent || 0,
                    statusData.Delivered || 0,
                    statusData.Failed || 0
                ],
                backgroundColor: [
                    '#FFC107',
                    '#007BFF',
                    '#28A745',
                    '#DC3545'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Distribution Chart
    const distributionCtx = document.getElementById('distributionChart').getContext('2d');
    
    new Chart(distributionCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(statusData),
            datasets: [{
                data: Object.values(statusData),
                backgroundColor: [
                    '#FFC107',
                    '#007BFF',
                    '#28A745',
                    '#17A2B8',
                    '#DC3545'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // View message details
    function viewMessageDetails(messageId) {
        const modal = new bootstrap.Modal(document.getElementById('messageModal'));
        const modalBody = document.getElementById('messageModalBody');
        
        modalBody.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Carregando...</span></div></div>';
        
        modal.show();
        
        fetch('/api/message/' + messageId)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    modalBody.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>' + data.error + '</div>';
                    return;
                }
                
                let recipientsHtml = '';
                if (data.recipients && data.recipients.length > 0) {
                    recipientsHtml = data.recipients.map(recipient => 
                        '<tr><td>' + formatPhoneNumber(recipient.phoneNumber) + '</td><td>' + getStatusBadge(recipient.state) + '</td><td>' + (recipient.error || '-') + '</td></tr>'
                    ).join('');
                }
                
                modalBody.innerHTML = '<div class="row"><div class="col-md-6"><h6>Informações da Mensagem</h6><p><strong>ID:</strong> ' + data.id + '</p><p><strong>Status:</strong> ' + getStatusBadge(data.state) + '</p><p><strong>Mensagem:</strong></p><div class="bg-light p-3 rounded">' + (data.message || 'N/A') + '</div></div><div class="col-md-6"><h6>Destinatários</h6><div class="table-responsive"><table class="table table-sm"><thead><tr><th>Telefone</th><th>Status</th><th>Erro</th></tr></thead><tbody>' + recipientsHtml + '</tbody></table></div></div></div>';
            })
            .catch(error => {
                modalBody.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>Erro ao carregar detalhes: ' + error.message + '</div>';
            });
    }

    // Auto-refresh dashboard every 30 seconds
    setInterval(function() {
        location.reload();
    }, 30000);
</script>
{% endblock %}
````

## File: sms-gateway-web/templates/login.html
````html
{% extends "base.html" %}

{% block title %}Login - SMS Gateway{% endblock %}

{% block content %}
<div class="d-flex justify-content-center align-items-center" style="min-height: calc(100vh - 200px);">
    <div class="card" style="width: 100%; max-width: 400px;">
        <div class="card-header text-center">
            <h5 class="card-title mb-0">
                <i class="fas fa-lock me-2"></i>
                Login
            </h5>
        </div>
        <div class="card-body">
            <form method="POST" action="{{ url_for('login') }}">
                <div class="mb-3">
                    <label for="username" class="form-label">Usuário</label>
                    <input type="text" class="form-control" id="username" name="username" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Senha</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </div>
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-sign-in-alt me-2"></i>
                        Entrar
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Focus on username field when page loads
    document.getElementById('username').focus();
</script>
{% endblock %}
````

## File: sms-gateway-web/templates/messages.html
````html
{% extends "base.html" %}

{% block title %}Mensagens - SMS Gateway{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">Mensagens</h1>
    <a href="/send" class="btn btn-primary">
        <i class="fas fa-paper-plane me-2"></i>
        Enviar SMS
    </a>
</div>

<div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">
            <i class="fas fa-envelope me-2"></i>
            Histórico de Mensagens
        </h5>
        <div class="d-flex gap-2">
            <button class="btn btn-outline-primary btn-sm" onclick="refreshMessages()">
                <i class="fas fa-sync-alt me-2"></i>
                Atualizar
            </button>
            <div class="input-group input-group-sm" style="width: 200px;">
                <span class="input-group-text">
                    <i class="fas fa-search"></i>
                </span>
                <input type="text" class="form-control" id="searchInput" placeholder="Buscar..." 
                       onkeyup="filterMessages()">
            </div>
        </div>
    </div>
    <div class="card-body">
        <div class="row mb-3">
            <div class="col-md-3">
                <select class="form-select" id="statusFilter" onchange="filterMessages()">
                    <option value="">Todos os Status</option>
                    <option value="pending">Pendentes</option>
                    <option value="processed">Processando</option>
                    <option value="sent">Enviados</option>
                    <option value="delivered">Entregues</option>
                    <option value="failed">Falharam</option>
                </select>
            </div>
            <div class="col-md-3">
                <select class="form-select" id="dateFilter" onchange="filterMessages()">
                    <option value="">Todas as Datas</option>
                    <option value="today">Hoje</option>
                    <option value="yesterday">Ontem</option>
                    <option value="last7days">Últimos 7 Dias</option>
                    <option value="last30days">Últimos 30 Dias</option>
                </select>
            </div>
            <div class="col-md-6 text-end">
                <div class="form-check form-switch d-inline-block mt-2">
                    <input class="form-check-input" type="checkbox" id="autoRefresh" checked>
                    <label class="form-check-label" for="autoRefresh">Atualização automática</label>
                </div>
            </div>
        </div>

        <div id="messagesTableContainer">
            {% if messages %}
                <div class="table-responsive">
                    <table class="table table-hover" id="messagesTable">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Mensagem</th>
                                <th>Destinatários</th>
                                <th>Status</th>
                                <th>Data</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for message in messages %}
                            <tr data-id="{{ message[0] }}" data-status="{{ message[3].lower() }}" data-date="{{ message[4] }}">
                                <td>{{ message[0] }}</td>
                                <td>
                                    <div class="text-truncate" style="max-width: 200px;" title="{{ message[1] }}">
                                        {{ message[1] }}
                                    </div>
                                </td>
                                <td>
                                    <span class="badge bg-secondary">Múltiplos</span>
                                </td>
                                <td>
                                    <span class="status-badge status-{{ message[3].lower() }}">
                                        {% if message[3] == 'Pending' %}Pendente
                                        {% elif message[3] == 'Processed' %}Processando
                                        {% elif message[3] == 'Sent' %}Enviado
                                        {% elif message[3] == 'Delivered' %}Entregue
                                        {% elif message[3] == 'Failed' %}Falhou
                                        {% else %}{{ message[3] }}
                                        {% endif %}
                                    </span>
                                </td>
                                <td>
                                    <small class="text-muted">{{ message[4] }}</small>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-outline-primary" onclick="viewMessageDetails('{{ message[0] }}')">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button class="btn btn-sm btn-outline-info" onclick="resendMessage('{{ message[0] }}')">
                                        <i class="fas fa-redo"></i>
                                    </button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                <div class="row mt-3">
                    <div class="col-md-6">
                        <nav aria-label="Page navigation">
                            <ul class="pagination">
                                <li class="page-item {% if current_page == 1 %}disabled{% endif %}">
                                    <a class="page-link" href="?page={{ current_page - 1 }}" aria-label="Previous">
                                        <span aria-hidden="true">&laquo;</span>
                                    </a>
                                </li>
                                {% for p in range(1, total_pages + 1) %}
                                <li class="page-item {% if p == current_page %}active{% endif %}">
                                    <a class="page-link" href="?page={{ p }}">{{ p }}</a>
                                </li>
                                {% endfor %}
                                <li class="page-item {% if current_page == total_pages %}disabled{% endif %}">
                                    <a class="page-link" href="?page={{ current_page + 1 }}" aria-label="Next">
                                        <span aria-hidden="true">&raquo;</span>
                                    </a>
                                </li>
                            </ul>
                        </nav>
                    </div>
                    <div class="col-md-6 text-md-end mt-2">
                        <p class="text-muted">Mostrando {{ start_index }}-{{ end_index }} de {{ total_messages }} mensagens</p>
                    </div>
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">Nenhuma mensagem encontrada</h5>
                    <p class="text-muted">Comece enviando sua primeira mensagem SMS.</p>
                    <a href="/send" class="btn btn-primary">
                        <i class="fas fa-paper-plane me-2"></i>
                        Enviar Primeira Mensagem
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>

<!-- Message Details Modal -->
<div class="modal fade" id="messageModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Detalhes da Mensagem</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="messageModalBody">
                <div class="text-center">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Resend Modal -->
<div class="modal fade" id="resendModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Reenviar Mensagem</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="resendModalBody">
                <div class="text-center">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-primary" id="confirmResendBtn">
                    <i class="fas fa-redo me-2"></i>
                    Reenviar
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    let autoRefreshInterval = setInterval(refreshMessages, 30000);

    // Toggle auto refresh
    document.getElementById('autoRefresh').addEventListener('change', function() {
        if (this.checked) {
            autoRefreshInterval = setInterval(refreshMessages, 30000);
        } else {
            clearInterval(autoRefreshInterval);
        }
    });

    // Refresh messages
    function refreshMessages() {
        fetch('/api/messages')
            .then(response => response.json())
            .then(data => {
                // Update messages table
                const container = document.getElementById('messagesTableContainer');
                if (data.messages && data.messages.length > 0) {
                    let html = `
                        <div class="table-responsive">
                            <table class="table table-hover" id="messagesTable">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Mensagem</th>
                                        <th>Destinatários</th>
                                        <th>Status</th>
                                        <th>Data</th>
                                        <th>Ações</th>
                                    </tr>
                                </thead>
                                <tbody>
                    `;
                    
                    data.messages.forEach(message => {
                        html += `
                            <tr data-id="${message[0]}" data-status="${message[3].toLowerCase()}" data-date="${message[4]}">
                                <td>${message[0]}</td>
                                <td>
                                    <div class="text-truncate" style="max-width: 200px;" title="${message[1]}">
                                        ${message[1]}
                                    </div>
                                </td>
                                <td>
                                    <span class="badge bg-secondary">Múltiplos</span>
                                </td>
                                <td>
                                    <span class="status-badge status-${message[3].toLowerCase()}">
                                        ${translateStatus(message[3])}
                                    </span>
                                </td>
                                <td>
                                    <small class="text-muted">${message[4]}</small>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-outline-primary" onclick="viewMessageDetails('${message[0]}')">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button class="btn btn-sm btn-outline-info" onclick="resendMessage('${message[0]}')">
                                        <i class="fas fa-redo"></i>
                                    </button>
                                </td>
                            </tr>
                        `;
                    });
                    
                    html += `
                                </tbody>
                            </table>
                        </div>
                    `;
                    
                    if (data.pagination) {
                        html += `
                            <div class="row mt-3">
                                <div class="col-md-6">
                                    <nav aria-label="Page navigation">
                                        <ul class="pagination">
                                            <li class="page-item ${data.pagination.current_page === 1 ? 'disabled' : ''}">
                                                <a class="page-link" href="?page=${data.pagination.current_page - 1}" aria-label="Previous">
                                                    <span aria-hidden="true">&laquo;</span>
                                                </a>
                                            </li>
                        `;
                        
                        for (let p = 1; p <= data.pagination.total_pages; p++) {
                            html += `
                                <li class="page-item ${p === data.pagination.current_page ? 'active' : ''}">
                                    <a class="page-link" href="?page=${p}">${p}</a>
                                </li>
                            `;
                        }
                        
                        html += `
                                            <li class="page-item ${data.pagination.current_page === data.pagination.total_pages ? 'disabled' : ''}">
                                                <a class="page-link" href="?page=${data.pagination.current_page + 1}" aria-label="Next">
                                                    <span aria-hidden="true">&raquo;</span>
                                                </a>
                                            </li>
                                        </ul>
                                    </nav>
                                </div>
                                <div class="col-md-6 text-md-end mt-2">
                                    <p class="text-muted">Mostrando ${data.pagination.start_index}-${data.pagination.end_index} de ${data.pagination.total_messages} mensagens</p>
                                </div>
                            </div>
                        `;
                    }
                    
                    container.innerHTML = html;
                } else {
                    container.innerHTML = `
                        <div class="text-center py-5">
                            <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                            <h5 class="text-muted">Nenhuma mensagem encontrada</h5>
                            <p class="text-muted">Comece enviando sua primeira mensagem SMS.</p>
                            <a href="/send" class="btn btn-primary">
                                <i class="fas fa-paper-plane me-2"></i>
                                Enviar Primeira Mensagem
                            </a>
                        </div>
                    `;
                }
                
                showToast('Lista de mensagens atualizada', 'info');
            })
            .catch(error => {
                showToast('Erro ao atualizar mensagens: ' + error.message, 'error');
            });
    }

    // Translate status to Portuguese
    function translateStatus(status) {
        const statusMap = {
            'Pending': 'Pendente',
            'Processed': 'Processando',
            'Sent': 'Enviado',
            'Delivered': 'Entregue',
            'Failed': 'Falhou'
        };
        return statusMap[status] || status;
    }

    // Filter messages
    function filterMessages() {
        const searchText = document.getElementById('searchInput').value.toLowerCase();
        const statusFilter = document.getElementById('statusFilter').value;
        const dateFilter = document.getElementById('dateFilter').value;
        
        const rows = document.querySelectorAll('#messagesTable tbody tr');
        
        // Calculate date boundaries
        const now = new Date();
        let dateStart = null;
        let dateEnd = null;
        
        if (dateFilter === 'today') {
            dateStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            dateEnd = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
        } else if (dateFilter === 'yesterday') {
            dateStart = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1);
            dateEnd = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        } else if (dateFilter === 'last7days') {
            dateStart = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7);
            dateEnd = now;
        } else if (dateFilter === 'last30days') {
            dateStart = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 30);
            dateEnd = now;
        }
        
        rows.forEach(row => {
            const id = row.cells[0].textContent.toLowerCase();
            const message = row.cells[1].textContent.toLowerCase();
            const status = row.dataset.status;
            const dateStr = row.dataset.date;
            let show = true;
            
            // Apply search filter
            if (searchText && !id.includes(searchText) && !message.includes(searchText)) {
                show = false;
            }
            
            // Apply status filter
            if (statusFilter && status !== statusFilter) {
                show = false;
            }
            
            // Apply date filter
            if (dateFilter && dateStart && dateEnd) {
                const date = new Date(dateStr);
                if (date < dateStart || date > dateEnd) {
                    show = false;
                }
            }
            
            row.style.display = show ? '' : 'none';
        });
    }

    // View message details
    function viewMessageDetails(messageId) {
        const modal = new bootstrap.Modal(document.getElementById('messageModal'));
        const modalBody = document.getElementById('messageModalBody');
        
        modalBody.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Carregando...</span></div></div>';
        
        modal.show();
        
        fetch('/api/message/' + messageId)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    modalBody.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>' + data.error + '</div>';
                    return;
                }
                
                let recipientsHtml = '';
                if (data.recipients && data.recipients.length > 0) {
                    recipientsHtml = data.recipients.map(recipient => 
                        '<tr><td>' + formatPhoneNumber(recipient.phoneNumber) + '</td><td>' + getStatusBadge(recipient.state) + '</td><td>' + (recipient.error || '-') + '</td></tr>'
                    ).join('');
                }
                
                modalBody.innerHTML = '<div class="row"><div class="col-md-6"><h6>Informações da Mensagem</h6><p><strong>ID:</strong> ' + data.id + '</p><p><strong>Status:</strong> ' + getStatusBadge(data.state) + '</p><p><strong>Mensagem:</strong></p><div class="bg-light p-3 rounded">' + (data.message || 'N/A') + '</div></div><div class="col-md-6"><h6>Destinatários</h6><div class="table-responsive"><table class="table table-sm"><thead><tr><th>Telefone</th><th>Status</th><th>Erro</th></tr></thead><tbody>' + recipientsHtml + '</tbody></table></div></div></div>';
            })
            .catch(error => {
                modalBody.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>Erro ao carregar detalhes: ' + error.message + '</div>';
            });
    }

    // Resend message
    function resendMessage(messageId) {
        const modal = new bootstrap.Modal(document.getElementById('resendModal'));
        const modalBody = document.getElementById('resendModalBody');
        const confirmBtn = document.getElementById('confirmResendBtn');
        
        modalBody.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Carregando...</span></div></div>';
        confirmBtn.disabled = true;
        
        modal.show();
        
        fetch('/api/message/' + messageId)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    modalBody.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>' + data.error + '</div>';
                    return;
                }
                
                modalBody.innerHTML = `
                    <p>Você está prestes a reenviar esta mensagem para todos os destinatários originais.</p>
                    <div class="mb-3">
                        <label class="form-label fw-bold">Mensagem:</label>
                        <div class="bg-light p-3 rounded">${data.message || 'N/A'}</div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-bold">Destinatários:</label>
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Telefone</th>
                                        <th>Status Original</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.recipients.map(recipient => 
                                        `<tr><td>${formatPhoneNumber(recipient.phoneNumber)}</td><td>${getStatusBadge(recipient.state)}</td></tr>`
                                    ).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Esta ação criará uma nova mensagem com os mesmos parâmetros da original.
                    </div>
                `;
                
                confirmBtn.disabled = false;
                confirmBtn.onclick = function() {
                    confirmResend(messageId, data);
                };
            })
            .catch(error => {
                modalBody.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>Erro ao carregar detalhes: ' + error.message + '</div>';
            });
    }

    // Confirm resend
    function confirmResend(messageId, originalData) {
        const confirmBtn = document.getElementById('confirmResendBtn');
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Reenviando...';
        
        // Prepare data for resend
        const data = {
            message: originalData.message,
            phone_numbers: originalData.recipients.map(r => r.phoneNumber),
            with_delivery_report: originalData.withDeliveryReport || false
        };
        
        if (originalData.simNumber) {
            data.sim_number = originalData.simNumber;
        }
        
        if (originalData.ttl) {
            data.ttl = originalData.ttl;
        }
        
        // Send request
        fetch('/api/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro ao reenviar: ' + result.error, 'error');
                return;
            }
            
            showToast('Mensagem reenviada com sucesso! ID: ' + result.id, 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('resendModal'));
            modal.hide();
            refreshMessages();
        })
        .catch(error => {
            showToast('Erro ao reenviar mensagem: ' + error.message, 'error');
        })
        .finally(() => {
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = '<i class="fas fa-redo me-2"></i>Reenviar';
        });
    }
</script>
{% endblock %}
````

## File: sms-gateway-web/templates/send.html
````html
{% extends "base.html" %}

{% block title %}Enviar SMS - SMS Gateway{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">Enviar SMS</h1>
    <a href="/messages" class="btn btn-outline-primary">
        <i class="fas fa-envelope me-2"></i>
        Ver Mensagens
    </a>
</div>

<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-paper-plane me-2"></i>
                    Nova Mensagem SMS
                </h5>
            </div>
            <div class="card-body">
                <form id="smsForm">
                    <!-- Message Text -->
                    <div class="mb-3">
                        <label for="message" class="form-label">Mensagem</label>
                        <textarea class="form-control" id="message" name="message" rows="4" 
                                  placeholder="Digite sua mensagem aqui..." required maxlength="1600"></textarea>
                        <div class="form-text">
                            <span id="charCount">0</span>/1600 caracteres
                        </div>
                    </div>

                    <!-- Phone Numbers -->
                    <div class="mb-3">
                        <label for="phoneNumbers" class="form-label">Números de Telefone</label>
                        <textarea class="form-control" id="phoneNumbers" name="phoneNumbers" rows="3" 
                                  placeholder="Digite os números separados por vírgula ou quebra de linha&#10;Exemplo: +5511999999999, +5511888888888" required></textarea>
                        <div class="form-text">
                            Digite os números no formato internacional (+55...) ou nacional, separados por vírgula ou quebra de linha.
                        </div>
                    </div>

                    <!-- Advanced Options -->
                    <div class="card mb-3">
                        <div class="card-header">
                            <button class="btn btn-link p-0 text-decoration-none" type="button" 
                                    data-bs-toggle="collapse" data-bs-target="#advancedOptions">
                                <i class="fas fa-cog me-2"></i>
                                Opções Avançadas
                                <i class="fas fa-chevron-down ms-2"></i>
                            </button>
                        </div>
                        <div class="collapse" id="advancedOptions">
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <div class="form-check">
                                                <input class="form-check-input" type="checkbox" id="deliveryReport" 
                                                       name="deliveryReport" checked>
                                                <label class="form-check-label" for="deliveryReport">
                                                    Relatório de Entrega
                                                </label>
                                            </div>
                                            <div class="form-text">
                                                Receber confirmação quando a mensagem for entregue
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="simNumber" class="form-label">SIM Card</label>
                                            <select class="form-select" id="simNumber" name="simNumber">
                                                <option value="">Automático</option>
                                                <option value="1">SIM 1</option>
                                                <option value="2">SIM 2</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="ttl" class="form-label">TTL (segundos)</label>
                                            <input type="number" class="form-control" id="ttl" name="ttl" 
                                                   placeholder="Tempo limite para envio" min="1" max="86400">
                                            <div class="form-text">
                                                Tempo limite em segundos (máximo 24 horas)
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-primary" id="sendBtn">
                            <i class="fas fa-paper-plane me-2"></i>
                            Enviar SMS
                        </button>
                        <button type="button" class="btn btn-outline-secondary" onclick="clearForm()">
                            <i class="fas fa-eraser me-2"></i>
                            Limpar
                        </button>
                        <button type="button" class="btn btn-outline-info" onclick="previewMessage()">
                            <i class="fas fa-eye me-2"></i>
                            Visualizar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <div class="col-lg-4">
        <!-- Quick Contacts -->
        <div class="card mb-3">
            <div class="card-header">
                <h6 class="card-title mb-0">
                    <i class="fas fa-address-book me-2"></i>
                    Contatos Rápidos
                </h6>
            </div>
            <div class="card-body">
                {% if contacts %}
                    <div class="list-group list-group-flush">
                        {% for contact in contacts[:10] %}
                        <div class="list-group-item d-flex justify-content-between align-items-center p-2">
                            <div>
                                <div class="fw-bold">{{ contact[0] }}</div>
                                <small class="text-muted">{{ contact[1] }}</small>
                            </div>
                            <button class="btn btn-sm btn-outline-primary" 
                                    onclick="addContact('{{ contact[1] }}')">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                        {% endfor %}
                    </div>
                    {% if contacts|length > 10 %}
                    <div class="text-center mt-2">
                        <a href="/contacts" class="btn btn-sm btn-outline-secondary">
                            Ver todos os contatos
                        </a>
                    </div>
                    {% endif %}
                {% else %}
                    <div class="text-center py-3">
                        <i class="fas fa-address-book fa-2x text-muted mb-2"></i>
                        <p class="text-muted mb-2">Nenhum contato encontrado</p>
                        <a href="/contacts" class="btn btn-sm btn-primary">
                            Adicionar Contatos
                        </a>
                    </div>
                {% endif %}
            </div>
        </div>

        <!-- Message Templates -->
        <div class="card">
            <div class="card-header">
                <h6 class="card-title mb-0">
                    <i class="fas fa-file-text me-2"></i>
                    Templates
                </h6>
            </div>
            <div class="card-body">
                <div class="list-group list-group-flush">
                    <button class="list-group-item list-group-item-action p-2" 
                            onclick="useTemplate('Olá! Esta é uma mensagem de teste do SMS Gateway.')">
                        <div class="fw-bold">Mensagem de Teste</div>
                        <small class="text-muted">Template básico para testes</small>
                    </button>
                    <button class="list-group-item list-group-item-action p-2" 
                            onclick="useTemplate('Lembrete: Você tem um compromisso agendado para hoje.')">
                        <div class="fw-bold">Lembrete</div>
                        <small class="text-muted">Template para lembretes</small>
                    </button>
                    <button class="list-group-item list-group-item-action p-2" 
                            onclick="useTemplate('Obrigado por entrar em contato conosco. Retornaremos em breve.')">
                        <div class="fw-bold">Resposta Automática</div>
                        <small class="text-muted">Template para respostas</small>
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Preview Modal -->
<div class="modal fade" id="previewModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Visualizar Mensagem</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="mb-3">
                    <label class="form-label fw-bold">Mensagem:</label>
                    <div class="bg-light p-3 rounded" id="previewMessage"></div>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Destinatários:</label>
                    <div id="previewRecipients"></div>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Configurações:</label>
                    <ul class="list-unstyled" id="previewSettings"></ul>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                <button type="button" class="btn btn-primary" onclick="sendFromPreview()">
                    <i class="fas fa-paper-plane me-2"></i>
                    Enviar Agora
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Success Modal -->
<div class="modal fade" id="successModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-success text-white">
                <h5 class="modal-title">
                    <i class="fas fa-check-circle me-2"></i>
                    Mensagem Enviada
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="successModalBody">
                <!-- Success content will be inserted here -->
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                <a href="/messages" class="btn btn-primary">Ver Mensagens</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Character counter
    document.getElementById('message').addEventListener('input', function() {
        const charCount = this.value.length;
        document.getElementById('charCount').textContent = charCount;
        
        if (charCount > 1600) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
        }
    });

    // Add contact to phone numbers
    function addContact(phoneNumber) {
        const phoneNumbersField = document.getElementById('phoneNumbers');
        const currentNumbers = phoneNumbersField.value.trim();
        
        if (currentNumbers) {
            phoneNumbersField.value = currentNumbers + ', ' + phoneNumber;
        } else {
            phoneNumbersField.value = phoneNumber;
        }
        
        showToast('Contato adicionado aos destinatários', 'success');
    }

    // Use template
    function useTemplate(templateText) {
        document.getElementById('message').value = templateText;
        document.getElementById('message').dispatchEvent(new Event('input'));
        showToast('Template aplicado', 'success');
    }

    // Clear form
    function clearForm() {
        document.getElementById('smsForm').reset();
        document.getElementById('charCount').textContent = '0';
        showToast('Formulário limpo', 'info');
    }

    // Preview message
    function previewMessage() {
        const message = document.getElementById('message').value.trim();
        const phoneNumbers = document.getElementById('phoneNumbers').value.trim();
        
        if (!message || !phoneNumbers) {
            showToast('Preencha a mensagem e os números de telefone', 'warning');
            return;
        }

        // Parse phone numbers
        const numbers = phoneNumbers.split(/[,\n]/).map(n => n.trim()).filter(n => n);
        
        // Update preview modal
        document.getElementById('previewMessage').textContent = message;
        
        const recipientsHtml = numbers.map(num => 
            '<span class="badge bg-secondary me-1 mb-1">' + formatPhoneNumber(num) + '</span>'
        ).join('');
        document.getElementById('previewRecipients').innerHTML = recipientsHtml;
        
        // Settings
        const deliveryReport = document.getElementById('deliveryReport').checked;
        const simNumber = document.getElementById('simNumber').value;
        const ttl = document.getElementById('ttl').value;
        
        let settingsHtml = '<li><i class="fas fa-check-circle text-success me-2"></i>Relatório de entrega: ' + (deliveryReport ? 'Sim' : 'Não') + '</li>';
        if (simNumber) {
            settingsHtml += '<li><i class="fas fa-sim-card text-info me-2"></i>SIM Card: ' + simNumber + '</li>';
        }
        if (ttl) {
            settingsHtml += '<li><i class="fas fa-clock text-warning me-2"></i>TTL: ' + ttl + ' segundos</li>';
        }
        
        document.getElementById('previewSettings').innerHTML = settingsHtml;
        
        const modal = new bootstrap.Modal(document.getElementById('previewModal'));
        modal.show();
    }

    // Send from preview
    function sendFromPreview() {
        const previewModal = bootstrap.Modal.getInstance(document.getElementById('previewModal'));
        previewModal.hide();
        sendMessage();
    }

    // Send message
    function sendMessage() {
        const form = document.getElementById('smsForm');
        const sendBtn = document.getElementById('sendBtn');
        
        // Validate form
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const message = document.getElementById('message').value.trim();
        const phoneNumbers = document.getElementById('phoneNumbers').value.trim();
        
        if (!message || !phoneNumbers) {
            showToast('Preencha todos os campos obrigatórios', 'warning');
            return;
        }

        // Parse phone numbers
        const numbers = phoneNumbers.split(/[,\n]/).map(n => n.trim()).filter(n => n);
        
        if (numbers.length === 0) {
            showToast('Adicione pelo menos um número de telefone', 'warning');
            return;
        }

        // Prepare data
        const data = {
            message: message,
            phone_numbers: numbers,
            with_delivery_report: document.getElementById('deliveryReport').checked
        };

        const simNumber = document.getElementById('simNumber').value;
        if (simNumber) {
            data.sim_number = parseInt(simNumber);
        }

        const ttl = document.getElementById('ttl').value;
        if (ttl) {
            data.ttl = parseInt(ttl);
        }

        // Show loading state
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';

        // Send request
        fetch('/api/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro: ' + result.error, 'error');
                return;
            }

            // Show success modal
            const successModalBody = document.getElementById('successModalBody');
            successModalBody.innerHTML = `
                <div class="mb-3">
                    <p><strong>ID da Mensagem:</strong> ${result.id}</p>
                    <p><strong>Status:</strong> ${getStatusBadge(result.state)}</p>
                    <p><strong>Destinatários:</strong> ${result.recipients.length}</p>
                </div>
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    Sua mensagem foi enviada com sucesso! Você pode acompanhar o status na página de mensagens.
                </div>
            `;

            const successModal = new bootstrap.Modal(document.getElementById('successModal'));
            successModal.show();

            // Clear form
            clearForm();
        })
        .catch(error => {
            showToast('Erro ao enviar mensagem: ' + error.message, 'error');
        })
        .finally(() => {
            // Reset button state
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Enviar SMS';
        });
    }

    // Form submit handler
    document.getElementById('smsForm').addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });
</script>
````

## File: sms-gateway-web/templates/settings.html
````html
{% extends "base.html" %}

{% block title %}Configurações - SMS Gateway{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">Configurações</h1>
    <button class="btn btn-primary" onclick="saveSettings()">
        <i class="fas fa-save me-2"></i>
        Salvar Alterações
    </button>
</div>

<div class="row">
    <div class="col-lg-8">
        <!-- Gateway Connection Settings -->
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-link me-2"></i>
                    Conexão com o Gateway
                </h5>
            </div>
            <div class="card-body">
                <form id="gatewaySettingsForm">
                    <div class="mb-3">
                        <label for="gatewayUrl" class="form-label">URL do Gateway *</label>
                        <input type="url" class="form-control" id="gatewayUrl" value="{{ settings.gateway_url }}" 
                               placeholder="http://192.168.1.100:8080" required>
                        <div class="form-text">
                            URL completa do seu gateway SMS Android (incluindo http:// e porta)
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="apiKey" class="form-label">Chave API</label>
                                <input type="password" class="form-control" id="apiKey" value="{{ settings.api_key }}" 
                                       placeholder="Sua chave de API">
                                <div class="form-text">
                                    Chave de API para autenticação com o gateway (se configurado)
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="deviceId" class="form-label">ID do Dispositivo</label>
                                <input type="text" class="form-control" id="deviceId" value="{{ settings.device_id }}" 
                                       placeholder="ID único do dispositivo">
                                <div class="form-text">
                                    ID único para identificar este cliente no gateway
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="verifySsl" 
                                   {% if settings.verify_ssl %}checked{% endif %}>
                            <label class="form-check-label" for="verifySsl">
                                Verificar Certificado SSL
                            </label>
                        </div>
                        <div class="form-text">
                            Desative se estiver usando um certificado autoassinado no gateway
                        </div>
                    </div>
                    <div class="mb-3">
                        <button type="button" class="btn btn-outline-primary" onclick="testConnection()">
                            <i class="fas fa-plug me-2"></i>
                            Testar Conexão
                        </button>
                        <div id="connectionTestResult" class="mt-2"></div>
                    </div>
                </form>
            </div>
        </div>

        <!-- Application Settings -->
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-cog me-2"></i>
                    Configurações da Aplicação
                </h5>
            </div>
            <div class="card-body">
                <form id="appSettingsForm">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="defaultCountryCode" class="form-label">Código do País Padrão</label>
                                <input type="text" class="form-control" id="defaultCountryCode" 
                                       value="{{ settings.default_country_code }}" placeholder="+55">
                                <div class="form-text">
                                    Código do país a ser adicionado automaticamente a números sem formato internacional
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="messagesPerPage" class="form-label">Mensagens por Página</label>
                                <select class="form-select" id="messagesPerPage">
                                    <option value="10" {% if settings.messages_per_page == 10 %}selected{% endif %}>10</option>
                                    <option value="25" {% if settings.messages_per_page == 25 %}selected{% endif %}>25</option>
                                    <option value="50" {% if settings.messages_per_page == 50 %}selected{% endif %}>50</option>
                                    <option value="100" {% if settings.messages_per_page == 100 %}selected{% endif %}>100</option>
                                </select>
                                <div class="form-text">
                                    Número de mensagens exibidas por página na lista de mensagens
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="autoRefreshDashboard" 
                                   {% if settings.auto_refresh_dashboard %}checked{% endif %}>
                            <label class="form-check-label" for="autoRefreshDashboard">
                                Atualização Automática do Dashboard
                            </label>
                        </div>
                        <div class="form-text">
                            Atualiza automaticamente o dashboard e a lista de mensagens a cada 30 segundos
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <div class="col-lg-4">
        <!-- Security Settings -->
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-lock me-2"></i>
                    Segurança
                </h5>
            </div>
            <div class="card-body">
                <form id="securitySettingsForm">
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="requireAuth" 
                                   {% if settings.require_auth %}checked{% endif %}>
                            <label class="form-check-label" for="requireAuth">
                                Exigir Autenticação
                            </label>
                        </div>
                        <div class="form-text">
                            Protege o acesso à interface web com login e senha
                        </div>
                    </div>
                    <div id="authSettings" {% if settings.require_auth %}style="display: block;"{% else %}style="display: none;"{% endif %}>
                        <div class="mb-3">
                            <label for="username" class="form-label">Nome de Usuário</label>
                            <input type="text" class="form-control" id="username" value="{{ settings.username }}" 
                                   {% if settings.require_auth %}required{% endif %}>
                        </div>
                        <div class="mb-3">
                            <label for="currentPassword" class="form-label">Senha Atual</label>
                            <input type="password" class="form-control" id="currentPassword" placeholder="Digite a senha atual para alterá-la">
                            <div class="form-text">
                                Deixe em branco para manter a senha atual
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="newPassword" class="form-label">Nova Senha</label>
                            <input type="password" class="form-control" id="newPassword" placeholder="Digite apenas se quiser alterar">
                        </div>
                        <div class="mb-3">
                            <label for="confirmPassword" class="form-label">Confirmar Nova Senha</label>
                            <input type="password" class="form-control" id="confirmPassword" placeholder="Confirme a nova senha">
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <!-- About Card -->
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-info-circle me-2"></i>
                    Sobre
                </h5>
            </div>
            <div class="card-body">
                <h6>SMS Gateway Web Client</h6>
                <p class="text-muted">Versão: {{ app_version }}</p>
                <p class="mb-3">Interface web para o Android SMS Gateway, permitindo o envio e gerenciamento de mensagens SMS através de um dispositivo Android conectado.</p>
                <div class="d-grid gap-2">
                    <a href="https://github.com/android-sms-gateway/client-py" class="btn btn-outline-primary btn-sm" target="_blank">
                        <i class="fab fa-github me-2"></i>
                        Repositório GitHub
                    </a>
                    <a href="https://github.com/android-sms-gateway/client-py/issues" class="btn btn-outline-danger btn-sm" target="_blank">
                        <i class="fas fa-bug me-2"></i>
                        Reportar Problema
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Show/hide auth settings based on requireAuth checkbox
    document.getElementById('requireAuth').addEventListener('change', function() {
        const authSettings = document.getElementById('authSettings');
        const username = document.getElementById('username');
        
        if (this.checked) {
            authSettings.style.display = 'block';
            username.setAttribute('required', 'required');
        } else {
            authSettings.style.display = 'none';
            username.removeAttribute('required');
        }
    });

    // Test gateway connection
    function testConnection() {
        const testResult = document.getElementById('connectionTestResult');
        testResult.innerHTML = '<div class="spinner-border spinner-border-sm text-primary me-2" role="status"><span class="visually-hidden">Testando...</span></div> Testando conexão...';
        
        const gatewayUrl = document.getElementById('gatewayUrl').value;
        const apiKey = document.getElementById('apiKey').value;
        const verifySsl = document.getElementById('verifySsl').checked;
        
        const data = {
            gateway_url: gatewayUrl,
            api_key: apiKey,
            verify_ssl: verifySsl
        };
        
        fetch('/api/test-connection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                testResult.innerHTML = '<div class="alert alert-success mt-2"><i class="fas fa-check-circle me-2"></i> Conexão bem-sucedida! O gateway respondeu corretamente.</div>';
            } else {
                testResult.innerHTML = '<div class="alert alert-danger mt-2"><i class="fas fa-exclamation-circle me-2"></i> Falha na conexão: ' + result.error + '</div>';
            }
        })
        .catch(error => {
            testResult.innerHTML = '<div class="alert alert-danger mt-2"><i class="fas fa-exclamation-circle me-2"></i> Erro ao testar conexão: ' + error.message + '</div>';
        });
    }

    // Save settings
    function saveSettings() {
        const gatewaySettingsForm = document.getElementById('gatewaySettingsForm');
        const appSettingsForm = document.getElementById('appSettingsForm');
        const securitySettingsForm = document.getElementById('securitySettingsForm');
        
        // Validate forms
        if (!gatewaySettingsForm.checkValidity() || !appSettingsForm.checkValidity() || !securitySettingsForm.checkValidity()) {
            gatewaySettingsForm.reportValidity();
            appSettingsForm.reportValidity();
            securitySettingsForm.reportValidity();
            return;
        }
        
        // Validate passwords match if new password is provided
        const requireAuth = document.getElementById('requireAuth').checked;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (requireAuth && newPassword && newPassword !== confirmPassword) {
            showToast('As senhas não coincidem!', 'error');
            document.getElementById('newPassword').classList.add('is-invalid');
            document.getElementById('confirmPassword').classList.add('is-invalid');
            return;
        }
        
        // Clear validation
        document.getElementById('newPassword').classList.remove('is-invalid');
        document.getElementById('confirmPassword').classList.remove('is-invalid');
        
        // Prepare data
        const data = {
            gateway_url: document.getElementById('gatewayUrl').value,
            api_key: document.getElementById('apiKey').value,
            device_id: document.getElementById('deviceId').value,
            verify_ssl: document.getElementById('verifySsl').checked,
            default_country_code: document.getElementById('defaultCountryCode').value,
            messages_per_page: parseInt(document.getElementById('messagesPerPage').value),
            auto_refresh_dashboard: document.getElementById('autoRefreshDashboard').checked,
            require_auth: requireAuth
        };
        
        if (requireAuth) {
            data.username = document.getElementById('username').value;
            
            // Only include password fields if new password is provided
            if (newPassword) {
                data.current_password = document.getElementById('currentPassword').value;
                data.new_password = newPassword;
            }
        }
        
        // Show loading state
        const saveBtn = document.querySelector('.btn-primary[onclick="saveSettings()"]');
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Salvando...';
        
        fetch('/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro ao salvar configurações: ' + result.error, 'error');
                return;
            }
            
            showToast('Configurações salvas com sucesso!', 'success');
            
            // If authentication was enabled or password changed, warn user about session
            if (requireAuth && (newPassword || result.auth_changed)) {
                setTimeout(() => {
                    showToast('Sua sessão pode expirar devido às alterações de autenticação. Faça login novamente se necessário.', 'warning');
                }, 1000);
            }
        })
        .catch(error => {
            showToast('Erro ao salvar configurações: ' + error.message, 'error');
        })
        .finally(() => {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>Salvar Alterações';
        });
    }
</script>
{% endblock %}
````

## File: sms-gateway-web/templates/webhooks.html
````html
{% extends "base.html" %}

{% block title %}Webhooks - SMS Gateway{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">Webhooks</h1>
    <button class="btn btn-primary" onclick="showAddWebhookModal()">
        <i class="fas fa-plus me-2"></i>
        Adicionar Webhook
    </button>
</div>

<div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">
            <i class="fas fa-webhook me-2"></i>
            Webhooks Configurados
        </h5>
        <div class="input-group input-group-sm" style="width: 250px;">
            <span class="input-group-text">
                <i class="fas fa-search"></i>
            </span>
            <input type="text" class="form-control" id="searchInput" placeholder="Buscar por nome ou URL..." 
                   onkeyup="filterWebhooks()">
        </div>
    </div>
    <div class="card-body">
        {% if webhooks %}
            <div class="table-responsive">
                <table class="table table-hover" id="webhooksTable">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>URL</th>
                            <th>Eventos</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for webhook in webhooks %}
                        <tr data-id="{{ loop.index }}" data-name="{{ webhook[0].lower() }}" data-url="{{ webhook[1].lower() }}">
                            <td>{{ webhook[0] }}</td>
                            <td>
                                <div class="text-truncate" style="max-width: 250px;" title="{{ webhook[1] }}">
                                    {{ webhook[1] }}
                                </div>
                            </td>
                            <td>
                                {% set events = webhook[2].split(',') %}
                                {% for event in events %}
                                    <span class="badge bg-info me-1">{{ event.strip() }}</span>
                                {% endfor %}
                            </td>
                            <td>
                                <span class="status-badge {% if webhook[3] %}status-sent{% else %}status-failed{% endif %}">
                                    {% if webhook[3] %}Ativo{% else %}Inativo{% endif %}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary" onclick="showEditWebhookModal('{{ loop.index }}')">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger" onclick="showDeleteWebhookModal('{{ loop.index }}')">
                                    <i class="fas fa-trash"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-info" onclick="testWebhook('{{ loop.index }}')">
                                    <i class="fas fa-plug"></i>
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="text-center py-5">
                <i class="fas fa-webhook fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">Nenhum webhook configurado</h5>
                <p class="text-muted">Adicione webhooks para receber notificações sobre eventos de mensagens.</p>
                <button class="btn btn-primary" onclick="showAddWebhookModal()">
                    <i class="fas fa-plus me-2"></i>
                    Adicionar Primeiro Webhook
                </button>
            </div>
        {% endif %}
    </div>
</div>

<!-- Add Webhook Modal -->
<div class="modal fade" id="addWebhookModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Adicionar Novo Webhook</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="addWebhookForm">
                    <div class="mb-3">
                        <label for="addName" class="form-label">Nome *</label>
                        <input type="text" class="form-control" id="addName" required>
                        <div class="form-text">
                            Um nome descritivo para identificar este webhook
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="addUrl" class="form-label">URL de Destino *</label>
                        <input type="url" class="form-control" id="addUrl" placeholder="https://example.com/webhook" required>
                        <div class="form-text">
                            URL completa para onde os dados do webhook serão enviados
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Eventos *</label>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input event-checkbox" type="checkbox" id="addEventMessageSent" value="message.sent">
                                    <label class="form-check-label" for="addEventMessageSent">
                                        Mensagem Enviada
                                    </label>
                                </div>
                                <div class="form-text">
                                    Disparado quando uma mensagem é enviada com sucesso para o gateway
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input event-checkbox" type="checkbox" id="addEventMessageDelivered" value="message.delivered">
                                    <label class="form-check-label" for="addEventMessageDelivered">
                                        Mensagem Entregue
                                    </label>
                                </div>
                                <div class="form-text">
                                    Disparado quando uma mensagem é confirmada como entregue ao destinatário
                                </div>
                            </div>
                        </div>
                        <div class="row mt-2">
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input event-checkbox" type="checkbox" id="addEventMessageFailed" value="message.failed">
                                    <label class="form-check-label" for="addEventMessageFailed">
                                        Falha no Envio
                                    </label>
                                </div>
                                <div class="form-text">
                                    Disparado quando uma mensagem falha ao ser enviada ou entregue
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input event-checkbox" type="checkbox" id="addEventMessageReceived" value="message.received">
                                    <label class="form-check-label" for="addEventMessageReceived">
                                        Mensagem Recebida
                                    </label>
                                </div>
                                <div class="form-text">
                                    Disparado quando uma nova mensagem SMS é recebida (se suportado pelo gateway)
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="addHeaders" class="form-label">Cabeçalhos HTTP Personalizados (JSON)</label>
                        <textarea class="form-control" id="addHeaders" rows="3" placeholder='{
  "Authorization": "Bearer your_token",
  "X-Custom-Header": "value"
}'></textarea>
                        <div class="form-text">
                            Objeto JSON com cabeçalhos HTTP personalizados para incluir nas requisições do webhook
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="addEnabled" checked>
                            <label class="form-check-label" for="addEnabled">
                                Ativado
                            </label>
                        </div>
                        <div class="form-text">
                            Desative para pausar temporariamente este webhook sem excluí-lo
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-primary" id="saveAddWebhookBtn" onclick="saveNewWebhook()">
                    <i class="fas fa-save me-2"></i>
                    Salvar Webhook
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Edit Webhook Modal -->
<div class="modal fade" id="editWebhookModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Editar Webhook</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="editWebhookForm">
                    <input type="hidden" id="editWebhookId">
                    <div class="mb-3">
                        <label for="editName" class="form-label">Nome *</label>
                        <input type="text" class="form-control" id="editName" required>
                        <div class="form-text">
                            Um nome descritivo para identificar este webhook
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="editUrl" class="form-label">URL de Destino *</label>
                        <input type="url" class="form-control" id="editUrl" required>
                        <div class="form-text">
                            URL completa para onde os dados do webhook serão enviados
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Eventos *</label>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input event-checkbox" type="checkbox" id="editEventMessageSent" value="message.sent">
                                    <label class="form-check-label" for="editEventMessageSent">
                                        Mensagem Enviada
                                    </label>
                                </div>
                                <div class="form-text">
                                    Disparado quando uma mensagem é enviada com sucesso para o gateway
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input event-checkbox" type="checkbox" id="editEventMessageDelivered" value="message.delivered">
                                    <label class="form-check-label" for="editEventMessageDelivered">
                                        Mensagem Entregue
                                    </label>
                                </div>
                                <div class="form-text">
                                    Disparado quando uma mensagem é confirmada como entregue ao destinatário
                                </div>
                            </div>
                        </div>
                        <div class="row mt-2">
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input event-checkbox" type="checkbox" id="editEventMessageFailed" value="message.failed">
                                    <label class="form-check-label" for="editEventMessageFailed">
                                        Falha no Envio
                                    </label>
                                </div>
                                <div class="form-text">
                                    Disparado quando uma mensagem falha ao ser enviada ou entregue
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input event-checkbox" type="checkbox" id="editEventMessageReceived" value="message.received">
                                    <label class="form-check-label" for="editEventMessageReceived">
                                        Mensagem Recebida
                                    </label>
                                </div>
                                <div class="form-text">
                                    Disparado quando uma nova mensagem SMS é recebida (se suportado pelo gateway)
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="editHeaders" class="form-label">Cabeçalhos HTTP Personalizados (JSON)</label>
                        <textarea class="form-control" id="editHeaders" rows="3"></textarea>
                        <div class="form-text">
                            Objeto JSON com cabeçalhos HTTP personalizados para incluir nas requisições do webhook
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="editEnabled">
                            <label class="form-check-label" for="editEnabled">
                                Ativado
                            </label>
                        </div>
                        <div class="form-text">
                            Desative para pausar temporariamente este webhook sem excluí-lo
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-primary" id="saveEditWebhookBtn" onclick="saveEditedWebhook()">
                    <i class="fas fa-save me-2"></i>
                    Salvar Alterações
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Delete Webhook Modal -->
<div class="modal fade" id="deleteWebhookModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title">
                    <i class="fas fa-trash me-2"></i>
                    Excluir Webhook
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <input type="hidden" id="deleteWebhookId">
                <p>Você tem certeza que deseja excluir este webhook?</p>
                <p><strong id="deleteWebhookName"></strong></p>
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Esta ação não pode ser desfeita.
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteBtn" onclick="deleteWebhook()">
                    <i class="fas fa-trash me-2"></i>
                    Excluir
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Test Webhook Modal -->
<div class="modal fade" id="testWebhookModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Testar Webhook</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <input type="hidden" id="testWebhookId">
                <p>Enviar uma requisição de teste para o webhook <strong id="testWebhookName"></strong>?</p>
                <p>URL: <span id="testWebhookUrl" class="text-break"></span></p>
                <div class="mb-3">
                    <label for="testEvent" class="form-label">Evento de Teste</label>
                    <select class="form-select" id="testEvent">
                        <option value="message.sent">Mensagem Enviada</option>
                        <option value="message.delivered">Mensagem Entregue</option>
                        <option value="message.failed">Falha no Envio</option>
                        <option value="message.received">Mensagem Recebida</option>
                    </select>
                </div>
                <div id="testResult" class="mt-3"></div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                <button type="button" class="btn btn-primary" id="confirmTestBtn" onclick="sendTestWebhook()">
                    <i class="fas fa-plug me-2"></i>
                    Enviar Teste
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Filter webhooks
    function filterWebhooks() {
        const searchText = document.getElementById('searchInput').value.toLowerCase();
        const rows = document.querySelectorAll('#webhooksTable tbody tr');
        
        rows.forEach(row => {
            const name = row.dataset.name;
            const url = row.dataset.url;
            const show = searchText === '' || name.includes(searchText) || url.includes(searchText);
            row.style.display = show ? '' : 'none';
        });
    }

    // Show add webhook modal
    function showAddWebhookModal() {
        const modal = new bootstrap.Modal(document.getElementById('addWebhookModal'));
        document.getElementById('addWebhookForm').reset();
        modal.show();
    }

    // Save new webhook
    function saveNewWebhook() {
        const form = document.getElementById('addWebhookForm');
        const saveBtn = document.getElementById('saveAddWebhookBtn');
        
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        // Get selected events
        const eventCheckboxes = document.querySelectorAll('#addWebhookForm .event-checkbox:checked');
        const events = Array.from(eventCheckboxes).map(cb => cb.value);
        
        if (events.length === 0) {
            showToast('Selecione pelo menos um evento para o webhook', 'warning');
            return;
        }
        
        const data = {
            name: document.getElementById('addName').value,
            url: document.getElementById('addUrl').value,
            events: events,
            headers: document.getElementById('addHeaders').value || '{}',
            enabled: document.getElementById('addEnabled').checked
        };
        
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Salvando...';
        
        fetch('/api/webhooks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro ao adicionar webhook: ' + result.error, 'error');
                return;
            }
            
            showToast('Webhook adicionado com sucesso!', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('addWebhookModal'));
            modal.hide();
            location.reload();
        })
        .catch(error => {
            showToast('Erro ao adicionar webhook: ' + error.message, 'error');
        })
        .finally(() => {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>Salvar Webhook';
        });
    }

    // Show edit webhook modal
    function showEditWebhookModal(webhookId) {
        const modal = new bootstrap.Modal(document.getElementById('editWebhookModal'));
        const row = document.querySelector(`#webhooksTable tr[data-id="${webhookId}"]`);
        
        document.getElementById('editWebhookId').value = webhookId;
        document.getElementById('editName').value = row.cells[0].textContent;
        document.getElementById('editUrl').value = row.cells[1].textContent;
        document.getElementById('editEnabled').checked = row.cells[3].textContent.trim() === 'Ativo';
        
        // Reset all event checkboxes
        document.querySelectorAll('#editWebhookForm .event-checkbox').forEach(cb => {
            cb.checked = false;
        });
        
        // Set event checkboxes based on row data
        const eventsText = row.cells[2].textContent;
        if (eventsText.includes('Mensagem Enviada')) {
            document.getElementById('editEventMessageSent').checked = true;
        }
        if (eventsText.includes('Mensagem Entregue')) {
            document.getElementById('editEventMessageDelivered').checked = true;
        }
        if (eventsText.includes('Falha no Envio')) {
            document.getElementById('editEventMessageFailed').checked = true;
        }
        if (eventsText.includes('Mensagem Recebida')) {
            document.getElementById('editEventMessageReceived').checked = true;
        }
        
        // Fetch headers data (assuming it's stored somewhere)
        document.getElementById('editHeaders').value = '';
        fetch(`/api/webhooks/${webhookId}`)
            .then(response => response.json())
            .then(data => {
                if (data.headers) {
                    document.getElementById('editHeaders').value = data.headers;
                }
            })
            .catch(error => {
                console.error('Error fetching webhook details:', error);
            });
        
        modal.show();
    }

    // Save edited webhook
    function saveEditedWebhook() {
        const form = document.getElementById('editWebhookForm');
        const saveBtn = document.getElementById('saveEditWebhookBtn');
        
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        // Get selected events
        const eventCheckboxes = document.querySelectorAll('#editWebhookForm .event-checkbox:checked');
        const events = Array.from(eventCheckboxes).map(cb => cb.value);
        
        if (events.length === 0) {
            showToast('Selecione pelo menos um evento para o webhook', 'warning');
            return;
        }
        
        const webhookId = document.getElementById('editWebhookId').value;
        const data = {
            name: document.getElementById('editName').value,
            url: document.getElementById('editUrl').value,
            events: events,
            headers: document.getElementById('editHeaders').value || '{}',
            enabled: document.getElementById('editEnabled').checked
        };
        
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Salvando...';
        
        fetch(`/api/webhooks/${webhookId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro ao atualizar webhook: ' + result.error, 'error');
                return;
            }
            
            showToast('Webhook atualizado com sucesso!', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('editWebhookModal'));
            modal.hide();
            location.reload();
        })
        .catch(error => {
            showToast('Erro ao atualizar webhook: ' + error.message, 'error');
        })
        .finally(() => {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>Salvar Alterações';
        });
    }

    // Show delete webhook modal
    function showDeleteWebhookModal(webhookId) {
        const modal = new bootstrap.Modal(document.getElementById('deleteWebhookModal'));
        const row = document.querySelector(`#webhooksTable tr[data-id="${webhookId}"]`);
        
        document.getElementById('deleteWebhookId').value = webhookId;
        document.getElementById('deleteWebhookName').textContent = row.cells[0].textContent;
        
        modal.show();
    }

    // Delete webhook
    function deleteWebhook() {
        const webhookId = document.getElementById('deleteWebhookId').value;
        const deleteBtn = document.getElementById('confirmDeleteBtn');
        
        deleteBtn.disabled = true;
        deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Excluindo...';
        
        fetch(`/api/webhooks/${webhookId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                showToast('Erro ao excluir webhook: ' + result.error, 'error');
                return;
            }
            
            showToast('Webhook excluído com sucesso!', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('deleteWebhookModal'));
            modal.hide();
            location.reload();
        })
        .catch(error => {
            showToast('Erro ao excluir webhook: ' + error.message, 'error');
        })
        .finally(() => {
            deleteBtn.disabled = false;
            deleteBtn.innerHTML = '<i class="fas fa-trash me-2"></i>Excluir';
        });
    }

    // Test webhook
    function testWebhook(webhookId) {
        const modal = new bootstrap.Modal(document.getElementById('testWebhookModal'));
        const row = document.querySelector(`#webhooksTable tr[data-id="${webhookId}"]`);
        
        document.getElementById('testWebhookId').value = webhookId;
        document.getElementById('testWebhookName').textContent = row.cells[0].textContent;
        document.getElementById('testWebhookUrl').textContent = row.cells[1].textContent;
        document.getElementById('testResult').innerHTML = '';
        
        modal.show();
    }

    // Send test webhook
    function sendTestWebhook() {
        const webhookId = document.getElementById('testWebhookId').value;
        const testEvent = document.getElementById('testEvent').value;
        const testBtn = document.getElementById('confirmTestBtn');
        const testResult = document.getElementById('testResult');
        
        testBtn.disabled = true;
        testBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';
        testResult.innerHTML = '<div class="spinner-border spinner-border-sm text-primary me-2" role="status"><span class="visually-hidden">Enviando...</span></div> Enviando requisição de teste...';
        
        const data = {
            event: testEvent
        };
        
        fetch(`/api/webhooks/${webhookId}/test`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                testResult.innerHTML = '<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i> Teste bem-sucedido! O webhook respondeu com status ' + result.status_code + '.</div>';
                if (result.response) {
                    testResult.innerHTML += '<div class="mt-2"><strong>Resposta:</strong> <pre class="bg-light p-2 rounded">' + JSON.stringify(result.response, null, 2) + '</pre></div>';
                }
            } else {
                testResult.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i> Falha no teste: ' + result.error + '</div>';
                if (result.status_code) {
                    testResult.innerHTML += '<div class="mt-2"><strong>Código de Status:</strong> ' + result.status_code + '</div>';
                }
                if (result.response) {
                    testResult.innerHTML += '<div class="mt-2"><strong>Resposta de Erro:</strong> <pre class="bg-light p-2 rounded">' + JSON.stringify(result.response, null, 2) + '</pre></div>';
                }
            }
        })
        .catch(error => {
            testResult.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i> Erro ao enviar teste: ' + error.message + '</div>';
        })
        .finally(() => {
            testBtn.disabled = false;
            testBtn.innerHTML = '<i class="fas fa-plug me-2"></i>Enviar Teste';
        });
    }
</script>
{% endblock %}
````

## File: sms-gateway-web/app.py
````python
import os
import json
import logging
import sqlite3
import hashlib
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from android_sms_gateway.client import AndroidSmsGatewayClient

app = Flask(__name__)
app.secret_key = os.urandom(24)
Bootstrap(app)

# Configuration
CONFIG_DIR = os.path.expanduser("~/.sms-gateway-web")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DB_FILE = os.path.join(CONFIG_DIR, "database.db")
APP_VERSION = "1.0.0"

# Default configuration
DEFAULT_CONFIG = {
    "gateway_url": "http://192.168.1.100:8080",
    "api_key": "",
    "device_id": "web-client",
    "verify_ssl": False,
    "default_country_code": "+55",
    "messages_per_page": 25,
    "auto_refresh_dashboard": True,
    "require_auth": False,
    "username": "admin",
    "password_hash": "",
    "session_timeout": 30  # minutes
}

# Ensure config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

# Load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with default config to ensure all keys exist
                return {**DEFAULT_CONFIG, **config}
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

# Save configuration
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving config: {e}")
        return False

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            message TEXT,
            recipients TEXT,
            state TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # Contacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT UNIQUE,
            group_name TEXT,
            notes TEXT
        )
    ''')
    
    # Webhooks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS webhooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT,
            events TEXT,
            headers TEXT,
            enabled INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize app
config = load_config()
init_db()

# SMS Gateway Client
def get_sms_client():
    return AndroidSmsGatewayClient(
        base_url=config['gateway_url'],
        api_key=config['api_key'] if config['api_key'] else None,
        device_id=config['device_id'],
        verify_ssl=config['verify_ssl']
    )

# Authentication decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if config['require_auth'] and 'user' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == config['username'] and check_password_hash(config['password_hash'], password):
            session['user'] = username
            session['login_time'] = datetime.datetime.now().isoformat()
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
            return redirect(url_for('login'))
    
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('login_time', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# Dashboard
@app.route('/')
@login_required
def dashboard():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get message stats
    cursor.execute("SELECT state, COUNT(*) FROM messages GROUP BY state")
    stats_data = cursor.fetchall()
    stats = {state: count for state, count in stats_data}
    
    # Get recent messages (last 10)
    cursor.execute("SELECT id, message, recipients, state, created_at FROM messages ORDER BY created_at DESC LIMIT 10")
    recent_messages = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', stats=stats, recent_messages=recent_messages)

# Send SMS page
@app.route('/send', methods=['GET', 'POST'])
@login_required
def send_page():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM contacts ORDER BY name")
    contacts = cursor.fetchall()
    conn.close()
    
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message')
        phone_numbers = data.get('phone_numbers', [])
        with_delivery_report = data.get('with_delivery_report', False)
        sim_number = data.get('sim_number')
        ttl = data.get('ttl')
        
        # Format phone numbers with default country code if needed
        formatted_numbers = []
        country_code = config.get('default_country_code', '+55')
        for number in phone_numbers:
            number = number.strip()
            if number and not number.startswith('+'):
                if not number.startswith(country_code):
                    number = country_code + number.lstrip('0')
                formatted_numbers.append(number)
            elif number:
                formatted_numbers.append(number)
        
        if not formatted_numbers:
            return jsonify({'error': 'Nenhum número de telefone fornecido'}), 400
            
        try:
            client = get_sms_client()
            options = {
                'with_delivery_report': with_delivery_report
            }
            if sim_number:
                options['sim_number'] = int(sim_number)
            if ttl:
                options['ttl'] = int(ttl)
                
            response = client.send_sms(formatted_numbers, message, **options)
            
            # Store message in database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO messages (id, message, recipients, state, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (response.id, message, json.dumps(formatted_numbers), response.state, now, now)
            )
            conn.commit()
            conn.close()
            
            return jsonify({
                'id': response.id,
                'state': response.state,
                'recipients': formatted_numbers
            })
        except Exception as e:
            logging.error(f"Error sending SMS: {e}")
            return jsonify({'error': str(e)}), 500
            
    return render_template('send.html', contacts=contacts)

# Messages page
@app.route('/messages')
@login_required
def messages():
    page = int(request.args.get('page', 1))
    per_page = config.get('messages_per_page', 25)
    offset = (page - 1) * per_page
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    total_pages = (total_messages + per_page - 1) // per_page
    
    cursor.execute("SELECT id, message, recipients, state, created_at FROM messages ORDER BY created_at DESC LIMIT ? OFFSET ?", (per_page, offset))
    messages_data = cursor.fetchall()
    
    start_index = offset + 1
    end_index = min(offset + per_page, total_messages)
    
    conn.close()
    
    return render_template(
        'messages.html', 
        messages=messages_data,
        current_page=page,
        total_pages=total_pages,
        start_index=start_index,
        end_index=end_index,
        total_messages=total_messages
    )

# Contacts page
@app.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.args.get('action', 'add')
        data = request.get_json()
        
        if action == 'add':
            name = data.get('name')
            phone = data.get('phone')
            group = data.get('group', '')
            notes = data.get('notes', '')
            
            try:
                cursor.execute(
                    "INSERT INTO contacts (name, phone, group_name, notes) VALUES (?, ?, ?, ?)",
                    (name, phone, group, notes)
                )
                conn.commit()
                return jsonify({'success': True, 'id': cursor.lastrowid})
            except sqlite3.IntegrityError:
                return jsonify({'error': 'Este número de telefone já está registrado'}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
                
        elif action == 'edit':
            contact_id = request.args.get('id')
            name = data.get('name')
            phone = data.get('phone')
            group = data.get('group', '')
            notes = data.get('notes', '')
            
            try:
                cursor.execute(
                    "UPDATE contacts SET name = ?, phone = ?, group_name = ?, notes = ? WHERE id = ?",
                    (name, phone, group, notes, contact_id)
                )
                conn.commit()
                return jsonify({'success': True})
            except sqlite3.IntegrityError:
                return jsonify({'error': 'Este número de telefone já está registrado em outro contato'}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
                
        elif action == 'delete':
            contact_id = request.args.get('id')
            try:
                cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
                conn.commit()
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
    
    cursor.execute("SELECT name, phone, group_name, notes FROM contacts ORDER BY name")
    contacts_data = cursor.fetchall()
    conn.close()
    
    return render_template('contacts.html', contacts=contacts_data)

# Settings page
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    global config
    
    if request.method == 'POST':
        data = request.get_json()
        new_config = config.copy()
        
        # Update configuration from request
        for key in ['gateway_url', 'api_key', 'device_id', 'default_country_code']:
            new_config[key] = data.get(key, new_config[key])
            
        new_config['verify_ssl'] = data.get('verify_ssl', False)
        new_config['messages_per_page'] = data.get('messages_per_page', 25)
        new_config['auto_refresh_dashboard'] = data.get('auto_refresh_dashboard', True)
        new_config['require_auth'] = data.get('require_auth', False)
        
        auth_changed = False
        if new_config['require_auth']:
            new_config['username'] = data.get('username', new_config['username'])
            
            new_password = data.get('new_password', '')
            if new_password:
                current_password = data.get('current_password', '')
                if config['password_hash'] and not check_password_hash(config['password_hash'], current_password):
                    return jsonify({'error': 'Senha atual incorreta'}), 400
                    
                new_config['password_hash'] = generate_password_hash(new_password)
                auth_changed = True
        
        if save_config(new_config):
            config = new_config
            return jsonify({'success': True, 'auth_changed': auth_changed})
        else:
            return jsonify({'error': 'Falha ao salvar configurações'}), 500
    
    return render_template('settings.html', settings=config, app_version=APP_VERSION)

# Webhooks page
@app.route('/webhooks', methods=['GET', 'POST'])
@login_required
def webhooks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.args.get('action', 'add')
        data = request.get_json()
        
        if action == 'add':
            name = data.get('name')
            url = data.get('url')
            events = ','.join(data.get('events', []))
            headers = data.get('headers', '{}')
            enabled = data.get('enabled', True)
            
            try:
                cursor.execute(
                    "INSERT INTO webhooks (name, url, events, headers, enabled) VALUES (?, ?, ?, ?, ?)",
                    (name, url, events, headers, 1 if enabled else 0)
                )
                conn.commit()
                return jsonify({'success': True, 'id': cursor.lastrowid})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
                
        elif action == 'edit':
            webhook_id = request.args.get('id')
            name = data.get('name')
            url = data.get('url')
            events = ','.join(data.get('events', []))
            headers = data.get('headers', '{}')
            enabled = data.get('enabled', True)
            
            try:
                cursor.execute(
                    "UPDATE webhooks SET name = ?, url = ?, events = ?, headers = ?, enabled = ? WHERE id = ?",
                    (name, url, events, headers, 1 if enabled else 0, webhook_id)
                )
                conn.commit()
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
                
        elif action == 'delete':
            webhook_id = request.args.get('id')
            try:
                cursor.execute("DELETE FROM webhooks WHERE id = ?", (webhook_id,))
                conn.commit()
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
                
        elif action == 'test':
            webhook_id = request.args.get('id')
            event_type = data.get('event', 'message.sent')
            
            try:
                cursor.execute("SELECT url, headers FROM webhooks WHERE id = ?", (webhook_id,))
                webhook = cursor.fetchone()
                if not webhook:
                    return jsonify({'error': 'Webhook não encontrado'}), 404
                    
                url = webhook[0]
                headers = json.loads(webhook[1]) if webhook[1] else {}
                
                # Create test payload
                test_payload = {
                    'event': event_type,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'test': True,
                    'data': {
                        'message_id': 'TEST-' + str(os.urandom(4).hex()),
                        'phone_number': '+5511999999999',
                        'message': 'Esta é uma mensagem de teste do SMS Gateway Web Client',
                        'status': event_type.split('.')[1] if '.' in event_type else 'sent'
                    }
                }
                
                import requests
                response = requests.post(url, json=test_payload, headers=headers, timeout=10)
                
                return jsonify({
                    'success': True,
                    'status_code': response.status_code,
                    'response': response.text[:500]  # Limit response text to avoid huge data
                })
            except requests.exceptions.RequestException as e:
                return jsonify({
                    'success': False,
                    'error': str(e),
                    'status_code': getattr(e.response, 'status_code', None),
                    'response': getattr(e.response, 'text', '')[:500]
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
            finally:
                conn.close()
    
    cursor.execute("SELECT name, url, events, enabled FROM webhooks ORDER BY name")
    webhooks_data = cursor.fetchall()
    conn.close()
    
    return render_template('webhooks.html', webhooks=webhooks_data)

# API endpoint to get messages
@app.route('/api/messages', methods=['GET'])
@login_required
def api_messages():
    page = int(request.args.get('page', 1))
    per_page = config.get('messages_per_page', 25)
    offset = (page - 1) * per_page
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    total_pages = (total_messages + per_page - 1) // per_page
    
    cursor.execute("SELECT id, message, recipients, state, created_at FROM messages ORDER BY created_at DESC LIMIT ? OFFSET ?", (per_page, offset))
    messages_data = cursor.fetchall()
    
    start_index = offset + 1
    end_index = min(offset + per_page, total_messages)
    
    conn.close()
    
    return jsonify({
        'messages': messages_data,
        'pagination': {
            'current_page': page,
            'total_pages': total_pages,
            'start_index': start_index,
            'end_index': end_index,
            'total_messages': total_messages
        }
    })

# API endpoint to get message details
@app.route('/api/message/<message_id>', methods=['GET'])
@login_required
def api_message_details(message_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, message, recipients, state, created_at FROM messages WHERE id = ?", (message_id,))
    message = cursor.fetchone()
    
    if not message:
        conn.close()
        return jsonify({'error': 'Mensagem não encontrada'}), 404
        
    # Parse recipients
    try:
        recipients = json.loads(message[2])
    except:
        recipients = []
        
    # For simplicity, mock recipient status since we don't have real per-recipient status in DB
    recipient_data = []
    for phone in recipients:
        recipient_data.append({
            'phoneNumber': phone,
            'state': message[3],  # Use overall message state
            'error': '' if message[3] != 'Failed' else 'Falha na entrega'
        })
    
    conn.close()
    
    return jsonify({
        'id': message[0],
        'message': message[1],
        'state': message[3],
        'createdAt': message[4],
        'recipients': recipient_data,
        'withDeliveryReport': True  # Mocked for demo
    })

# API endpoint to send SMS
@app.route('/api/send', methods=['POST'])
@login_required
def api_send():
    data = request.get_json()
    message = data.get('message')
    phone_numbers = data.get('phone_numbers', [])
    with_delivery_report = data.get('with_delivery_report', False)
    sim_number = data.get('sim_number')
    ttl = data.get('ttl')
    
    # Format phone numbers with default country code if needed
    formatted_numbers = []
    country_code = config.get('default_country_code', '+55')
    for number in phone_numbers:
        number = number.strip()
        if number and not number.startswith('+'):
            if not number.startswith(country_code):
                number = country_code + number.lstrip('0')
            formatted_numbers.append(number)
        elif number:
            formatted_numbers.append(number)
    
    if not formatted_numbers:
        return jsonify({'error': 'Nenhum número de telefone fornecido'}), 400
        
    try:
        client = get_sms_client()
        options = {
            'with_delivery_report': with_delivery_report
        }
        if sim_number:
            options['sim_number'] = int(sim_number)
        if ttl:
            options['ttl'] = int(ttl)
            
        response = client.send_sms(formatted_numbers, message, **options)
        
        # Store message in database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO messages (id, message, recipients, state, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (response.id, message, json.dumps(formatted_numbers), response.state, now, now)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'id': response.id,
            'state': response.state,
            'recipients': formatted_numbers
        })
    except Exception as e:
        logging.error(f"Error sending SMS: {e}")
        return jsonify({'error': str(e)}), 500

# API endpoint to test connection
@app.route('/api/test-connection', methods=['POST'])
@login_required
def api_test_connection():
    data = request.get_json()
    gateway_url = data.get('gateway_url', config['gateway_url'])
    api_key = data.get('api_key', config['api_key'])
    verify_ssl = data.get('verify_ssl', config['verify_ssl'])
    
    try:
        client = AndroidSmsGatewayClient(
            base_url=gateway_url,
            api_key=api_key if api_key else None,
            device_id=config['device_id'],
            verify_ssl=verify_ssl
        )
        # Simple ping or status check - assuming the client has a method to test connection
        # For now, we'll simulate it since the actual client might not have this
        import requests
        response = requests.get(gateway_url, timeout=5, verify=verify_ssl)
        if response.status_code == 200:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': f'Resposta inesperada: {response.status_code}'})
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'Falha na conexão: {str(e)}'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro inesperado: {str(e)}'})
````

## File: sms-gateway-web/README.md
````markdown
# SMS Gateway Web Client

A web-based interface for the Android SMS Gateway, replicating the functionality of the Python client for sending and managing SMS messages through a clean dashboard.

## Features

- Send SMS messages to individual or multiple recipients
- View message history and delivery status
- Manage SMS gateway connection settings
- Simple contact management for frequent recipients
- Webhook support for event notifications

## Installation

1. **Clone the Repository** (if applicable) or ensure all files are in the `sms-gateway-web` directory.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python run.py
   ```
   You can specify host and port if needed:
   ```bash
   python run.py --host 0.0.0.0 --port 5000
   ```

4. **Access the Web Interface**:
   Open your browser and navigate to `http://localhost:5000` (or the host/port you specified).

## Configuration

- The first time you run the application, a configuration directory will be created at `~/.sms-gateway-web/` with a `config.json` file and a local database.
- You can configure the gateway connection settings, authentication requirements, and other preferences through the web interface under "Settings".

## Usage

- **Dashboard**: View recent messages and statistics.
- **Send SMS**: Compose and send messages to one or more recipients.
- **Messages**: Browse message history with status information.
- **Contacts**: Manage frequently used recipient information.
- **Webhooks**: Configure webhooks for event notifications (message sent, delivered, failed, etc.).
- **Settings**: Configure gateway connection and application preferences.

## Security

- Authentication can be enabled in the settings to protect access to the web interface.
- Configuration data and local message history are stored in `~/.sms-gateway-web/`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have feature requests, please file an issue on the GitHub repository or contact the maintainers.
````

## File: sms-gateway-web/requirements.txt
````
flask==2.0.1
flask-bootstrap==3.3.7.1
werkzeug==2.0.1
requests==2.26.0
android-sms-gateway-client==0.1.0
````

## File: sms-gateway-web/run.py
````python
import os
import sys
import argparse

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the SMS Gateway Web Client')
    parser.add_argument('--host', default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()
    
    app.run(host=args.host, port=args.port, debug=args.debug)
````

## File: requirements.txt
````
sqlite3
base64
flask
werkzeug
requests
````

## File: .github/workflows/close-issues.yml
````yaml
name: Close inactive issues
on:
  schedule:
    - cron: "30 1 * * *"

jobs:
  close-issues:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - uses: actions/stale@v5
        with:
          days-before-issue-stale: 7
          days-before-issue-close: 7
          days-before-pr-close: -1
          days-before-pr-stale: -1
          stale-issue-message: "This issue is stale because it has been open for 7 days with no activity."
          close-issue-message: "This issue was closed because it has been inactive for 7 days since being marked as stale."
          stale-issue-label: "stale"
          exempt-all-assignees: true
          repo-token: ${{ secrets.GITHUB_TOKEN }}
````

## File: android_sms_gateway/encryption.py
````python
import abc
import base64
import typing as t


class BaseEncryptor(abc.ABC):
    def __init__(self, passphrase: str, *, iterations: int) -> None:
        self.passphrase = passphrase
        self.iterations = iterations

    @abc.abstractmethod
    def encrypt(self, cleartext: str) -> str:
        ...

    @abc.abstractmethod
    def decrypt(self, encrypted: str) -> str:
        ...


_Encryptor: t.Optional[t.Type[BaseEncryptor]] = None


try:
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA1
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad

    class AESEncryptor(BaseEncryptor):
        def encrypt(self, cleartext: str) -> str:
            saltBytes = self._generate_salt()
            key = self._generate_key(saltBytes, self.iterations)

            cipher = AES.new(key, AES.MODE_CBC, iv=saltBytes)

            encrypted_bytes = cipher.encrypt(pad(cleartext.encode(), AES.block_size))

            salt = base64.b64encode(saltBytes).decode("utf-8")
            encrypted = base64.b64encode(encrypted_bytes).decode("utf-8")

            return f"$aes-256-cbc/pbkdf2-sha1$i={self.iterations}${salt}${encrypted}"

        def decrypt(self, encrypted: str) -> str:
            chunks = encrypted.split("$")

            if len(chunks) < 5:
                raise ValueError("Invalid encryption format")

            if chunks[1] != "aes-256-cbc/pbkdf2-sha1":
                raise ValueError("Unsupported algorithm")

            params = self._parse_params(chunks[2])
            if "i" not in params:
                raise ValueError("Missing iteration count")

            iterations = int(params["i"])
            salt = base64.b64decode(chunks[-2])
            encrypted_bytes = base64.b64decode(chunks[-1])

            key = self._generate_key(salt, iterations)
            cipher = AES.new(key, AES.MODE_CBC, iv=salt)

            decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

            return decrypted_bytes.decode("utf-8")

        def _generate_salt(self) -> bytes:
            return get_random_bytes(16)

        def _generate_key(self, salt: bytes, iterations: int) -> bytes:
            return PBKDF2(
                self.passphrase,
                salt,
                count=iterations,
                dkLen=32,
                hmac_hash_module=SHA1,
            )

        def _parse_params(self, params: str) -> t.Dict[str, str]:
            return {k: v for k, v in [p.split("=") for p in params.split(",")]}

    _Encryptor = AESEncryptor
except ImportError:
    ...


def Encryptor(passphrase: str, *, iterations: int = 75_000) -> BaseEncryptor:
    if _Encryptor is None:
        raise ImportError("Please install cryptodome")

    return _Encryptor(passphrase, iterations=iterations)
````

## File: tests/test_client.py
````python
import os
import pytest
from requests import HTTPError

from android_sms_gateway.client import APIClient
from android_sms_gateway.constants import DEFAULT_URL
from android_sms_gateway.domain import Webhook
from android_sms_gateway.enums import WebhookEvent
from android_sms_gateway.http import RequestsHttpClient


@pytest.fixture
def client():
    """
    A fixture providing an instance of `APIClient` for use in tests.

    The client is created using the values of the following environment variables:

    - `API_LOGIN` (defaults to `"test"`)
    - `API_PASSWORD` (defaults to `"test"`)
    - `API_BASE_URL` (defaults to `constants.DEFAULT_URL`)

    The client is yielded from the fixture, and automatically closed when the
    test is finished.

    :yields: An instance of `APIClient`.
    """
    with RequestsHttpClient() as h, APIClient(
        os.environ.get("API_LOGIN") or "test",
        os.environ.get("API_PASSWORD") or "test",
        base_url=os.environ.get("API_BASE_URL") or DEFAULT_URL,
        http=h,
    ) as c:
        yield c


@pytest.mark.skipif(
    not all(
        [
            os.environ.get("API_LOGIN"),
            os.environ.get("API_PASSWORD"),
        ]
    ),
    reason="API credentials are not set in the environment variables",
)
class TestAPIClient:
    def test_webhook_create(self, client: APIClient):
        """
        Tests that a webhook can be successfully created using the client.

        It creates a webhook, and then asserts that the created webhook matches the
        expected values.

        :param client: An instance of `APIClient`.
        """
        item = Webhook(
            id="webhook_123",
            url="https://example.com/webhook",
            event=WebhookEvent.SMS_RECEIVED,
        )

        created = client.create_webhook(item)

        assert created.id == "webhook_123"
        assert created.url == "https://example.com/webhook"
        assert created.event == WebhookEvent.SMS_RECEIVED

    def test_webhook_create_invalid_url(self, client: APIClient):
        """
        Tests that attempting to create a webhook with an invalid URL raises an
        `HTTPError`.

        The test creates a webhook with an invalid URL, and then asserts that an
        `HTTPError` is raised.

        :param client: An instance of `APIClient`.
        """
        with pytest.raises(HTTPError):
            client.create_webhook(
                Webhook(None, url="not_a_url", event=WebhookEvent.SMS_RECEIVED)
            )

    def test_webhook_get(self, client: APIClient):
        """
        Tests that the `get_webhooks` method retrieves a non-empty list of webhooks
        and that it contains a webhook with the expected ID, URL, and event type.

        :param client: An instance of `APIClient`.
        """

        webhooks = client.get_webhooks()

        assert len(webhooks) > 0

        assert any(
            [
                webhook.id == "webhook_123"
                and webhook.url == "https://example.com/webhook"
                and webhook.event == WebhookEvent.SMS_RECEIVED
                for webhook in webhooks
            ]
        )

    def test_webhook_delete(self, client: APIClient):
        """
        Tests that a webhook can be successfully deleted using the client.

        It deletes a webhook with a specific ID and then asserts that the list of
        webhooks does not contain a webhook with that ID.

        :param client: An instance of `APIClient`.
        """

        client.delete_webhook("webhook_123")

        webhooks = client.get_webhooks()

        assert not any([webhook.id == "webhook_123" for webhook in webhooks])
````

## File: tests/test_encryption.py
````python
import pytest

from android_sms_gateway.encryption import AESEncryptor


def test_decrypt():
    passphrase = "passphrase"
    cleartext = "hello"
    encrypted = "$aes-256-cbc/pbkdf2-sha1$i=75000$obSTW6ittQvTtdAxonQKIw==$g3QFAC9CtBcPxoKlouqsyQ=="
    encryptor = AESEncryptor(passphrase, iterations=75000)

    decrypted = encryptor.decrypt(encrypted)

    assert cleartext == decrypted


def test_encrypt_decrypt():
    passphrase = "correcthorsebatterystaple"
    encryptor = AESEncryptor(passphrase, iterations=1000)
    cleartext = "The quick brown fox jumps over the lazy dog"
    encrypted = encryptor.encrypt(cleartext)
    decrypted = encryptor.decrypt(encrypted)
    assert cleartext == decrypted


def test_invalid_format_error():
    passphrase = "correcthorsebatterystaple"
    encryptor = AESEncryptor(passphrase, iterations=1000)
    with pytest.raises(ValueError, match="Invalid encryption format"):
        encryptor.decrypt("invalid$format$string")


def test_unsupported_algorithm_error():
    passphrase = "correcthorsebatterystaple"
    encryptor = AESEncryptor(passphrase, iterations=1000)
    with pytest.raises(ValueError, match="Unsupported algorithm"):
        encryptor.decrypt("$unsupported-algorithm$i=0$salt$data")


def test_missing_iteration_count_error():
    passphrase = "correcthorsebatterystaple"
    encryptor = AESEncryptor(passphrase, iterations=1000)
    with pytest.raises(ValueError, match="Missing iteration count"):
        encryptor.decrypt("$aes-256-cbc/pbkdf2-sha1$x=0$salt$data")
````

## File: .flake8
````
[flake8]
max-line-length = 88
extend-ignore = E203 E501
````

## File: .gitignore
````
# File created using '.gitignore Generator' for Visual Studio Code: https://bit.ly/vscode-gig
# Created by https://www.toptal.com/developers/gitignore/api/windows,visualstudiocode,linux,macos,python
# Edit at https://www.toptal.com/developers/gitignore?templates=windows,visualstudiocode,linux,macos,python

### Linux ###
*~

# temporary files which can be created if a process still has a handle open of a deleted file
.fuse_hidden*

# KDE directory preferences
.directory

# Linux trash folder which might appear on any partition or disk
.Trash-*

# .nfs files are created when an open file is removed but is still being accessed
.nfs*

### macOS ###
# General
.DS_Store
.AppleDouble
.LSOverride

# Icon must end with two \r
Icon

# Thumbnails
._*

# Files that might appear in the root of a volume
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent

# Directories potentially created on remote AFP share
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk

### macOS Patch ###
# iCloud generated files
*.icloud

### Python ###
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

### Python Patch ###
# Poetry local configuration file - https://python-poetry.org/docs/configuration/#local-configuration
poetry.toml

# ruff
.ruff_cache/

# LSP config files
pyrightconfig.json

### VisualStudioCode ###
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
!.vscode/*.code-snippets

# Local History for Visual Studio Code
.history/

# Built Visual Studio Code Extensions
*.vsix

### VisualStudioCode Patch ###
# Ignore all local history of files
.history
.ionide

### Windows ###
# Windows thumbnail cache files
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db

# Dump file
*.stackdump

# Folder config file
[Dd]esktop.ini

# Recycle Bin used on file shares
$RECYCLE.BIN/

# Windows Installer files
*.cab
*.msi
*.msix
*.msm
*.msp

# Windows shortcuts
*.lnk

# End of https://www.toptal.com/developers/gitignore/api/windows,visualstudiocode,linux,macos,python

# Custom rules (everything added below won't be overriden by 'Generate .gitignore File' if you use 'Update' option)
````

## File: .isort.cfg
````
[settings]
profile = black
````

## File: LICENSE
````
Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
````

## File: .github/workflows/publish.yml
````yaml
# This workflow will upload a Python Package when a release is created

name: Upload Python Package

on:
  release:
    types: [published]

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/android-sms-gateway
    permissions:
      id-token: write

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.x"

      - name: Install pipenv
        run: |
          python -m pip install --upgrade pipenv

      - name: Install dependencies
        run: |
          pipenv install --deploy --dev

      - name: Build package
        run: |
          sed -i 's|VERSION = ".*"|VERSION = "'${GITHUB_REF_NAME:1}'"|g' ./android_sms_gateway/constants.py
          pipenv run python -m build

      - name: Publish package
        uses: pypa/gh-action-pypi-publish@release/v1
````

## File: android_sms_gateway/__init__.py
````python
from .ahttp import AsyncHttpClient
from .client import APIClient, AsyncAPIClient
from .constants import VERSION
from .domain import Message, MessageState, RecipientState
from .encryption import Encryptor
from .http import HttpClient

__all__ = (
    "APIClient",
    "AsyncAPIClient",
    "AsyncHttpClient",
    "HttpClient",
    "Message",
    "MessageState",
    "RecipientState",
    "Encryptor",
)

__version__ = VERSION
````

## File: android_sms_gateway/ahttp.py
````python
import abc
import typing as t


class AsyncHttpClient(t.Protocol):
    @abc.abstractmethod
    async def get(
        self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
    ) -> dict: ...

    @abc.abstractmethod
    async def post(
        self, url: str, payload: dict, *, headers: t.Optional[t.Dict[str, str]] = None
    ) -> dict: ...

    @abc.abstractmethod
    async def delete(
        self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
    ) -> None:
        """
        Sends a DELETE request to the specified URL.

        Args:
            url: The URL to send the DELETE request to.
            headers: Optional dictionary of HTTP headers to send with the request.

        Returns:
            None
        """

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


DEFAULT_CLIENT: t.Optional[t.Type[AsyncHttpClient]] = None


try:
    import aiohttp

    class AiohttpAsyncHttpClient(AsyncHttpClient):
        def __init__(self, session: t.Optional[aiohttp.ClientSession] = None) -> None:
            self._session = session

        async def __aenter__(self):
            if self._session is not None:
                raise ValueError("Session already initialized")

            self._session = await aiohttp.ClientSession().__aenter__()

            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if self._session is None:
                return

            await self._session.close()
            self._session = None

        async def get(
            self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
        ) -> dict:
            if self._session is None:
                raise ValueError("Session not initialized")

            async with self._session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

        async def post(
            self,
            url: str,
            payload: dict,
            *,
            headers: t.Optional[t.Dict[str, str]] = None,
        ) -> dict:
            if self._session is None:
                raise ValueError("Session not initialized")

            async with self._session.post(
                url, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                return await response.json()

        async def delete(
            self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
        ) -> None:
            if self._session is None:
                raise ValueError("Session not initialized")

            async with self._session.delete(url, headers=headers) as response:
                response.raise_for_status()

    DEFAULT_CLIENT = AiohttpAsyncHttpClient
except ImportError:
    pass

try:
    import httpx

    class HttpxAsyncHttpClient(AsyncHttpClient):
        def __init__(self, client: t.Optional[httpx.AsyncClient] = None) -> None:
            self._client = client

        async def __aenter__(self):
            if self._client is not None:
                raise ValueError("Client already initialized")

            self._client = await httpx.AsyncClient().__aenter__()

            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if self._client is None:
                return

            await self._client.aclose()
            self._client = None

        async def get(
            self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
        ) -> dict:
            if self._client is None:
                raise ValueError("Client not initialized")

            response = await self._client.get(url, headers=headers)

            return response.raise_for_status().json()

        async def post(
            self,
            url: str,
            payload: dict,
            *,
            headers: t.Optional[t.Dict[str, str]] = None,
        ) -> dict:
            if self._client is None:
                raise ValueError("Client not initialized")

            response = await self._client.post(url, headers=headers, json=payload)

            return response.raise_for_status().json()

        async def delete(
            self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
        ) -> None:
            if self._client is None:
                raise ValueError("Client not initialized")

            response = await self._client.delete(url, headers=headers)
            response.raise_for_status()

    DEFAULT_CLIENT = HttpxAsyncHttpClient
except ImportError:
    pass


def get_client() -> AsyncHttpClient:
    if DEFAULT_CLIENT is None:
        raise ImportError("Please install aiohttp or httpx")

    return DEFAULT_CLIENT()
````

## File: android_sms_gateway/constants.py
````python
VERSION = "1.0.0"

DEFAULT_URL = "https://api.sms-gate.app/3rdparty/v1"
````

## File: android_sms_gateway/enums.py
````python
import enum


class ProcessState(enum.Enum):
    Pending = "Pending"
    Processed = "Processed"
    Sent = "Sent"
    Delivered = "Delivered"
    Failed = "Failed"


class WebhookEvent(enum.Enum):
    """
    Webhook events that can be sent by the server.
    """

    SMS_RECEIVED = "sms:received"
    """Triggered when an SMS is received."""

    SMS_SENT = "sms:sent"
    """Triggered when an SMS is sent."""

    SMS_DELIVERED = "sms:delivered"
    """Triggered when an SMS is delivered."""

    SMS_FAILED = "sms:failed"
    """Triggered when an SMS processing fails."""

    SYSTEM_PING = "system:ping"
    """Triggered when the device pings the server."""
````

## File: android_sms_gateway/http.py
````python
import abc
import typing as t


class HttpClient(t.Protocol):
    @abc.abstractmethod
    def get(
        self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
    ) -> dict: ...

    @abc.abstractmethod
    def post(
        self, url: str, payload: dict, *, headers: t.Optional[t.Dict[str, str]] = None
    ) -> dict: ...

    @abc.abstractmethod
    def delete(self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None) -> None:
        """
        Sends a DELETE request to the specified URL.

        Args:
            url: The URL to send the DELETE request to.
            headers: Optional dictionary of HTTP headers to send with the request.

        Returns:
            None
        """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


DEFAULT_CLIENT: t.Optional[t.Type[HttpClient]] = None

try:
    import requests

    class RequestsHttpClient(HttpClient):
        def __init__(self, session: t.Optional[requests.Session] = None) -> None:
            self._session = session

        def __enter__(self):
            if self._session is not None:
                raise ValueError("Session already initialized")

            self._session = requests.Session().__enter__()

            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self._session is None:
                return

            self._session.close()
            self._session = None

        def get(
            self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
        ) -> dict:
            if self._session is None:
                raise ValueError("Session not initialized")

            return self._process_response(self._session.get(url, headers=headers))

        def post(
            self,
            url: str,
            payload: dict,
            *,
            headers: t.Optional[t.Dict[str, str]] = None,
        ) -> dict:
            if self._session is None:
                raise ValueError("Session not initialized")

            return self._process_response(
                self._session.post(url, headers=headers, json=payload)
            )

        def delete(
            self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
        ) -> None:
            if self._session is None:
                raise ValueError("Session not initialized")

            self._session.delete(url, headers=headers).raise_for_status()

        def _process_response(self, response: requests.Response) -> dict:
            response.raise_for_status()
            return response.json()

    DEFAULT_CLIENT = RequestsHttpClient
except ImportError:
    pass

try:
    import httpx

    class HttpxHttpClient(HttpClient):
        def __init__(self, client: t.Optional[httpx.Client] = None) -> None:
            self._client = client

        def __enter__(self):
            if self._client is not None:
                raise ValueError("Client already initialized")

            self._client = httpx.Client().__enter__()

            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self._client is None:
                return

            self._client.close()
            self._client = None

        def get(
            self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
        ) -> dict:
            if self._client is None:
                raise ValueError("Client not initialized")

            return self._client.get(url, headers=headers).raise_for_status().json()

        def post(
            self,
            url: str,
            payload: dict,
            *,
            headers: t.Optional[t.Dict[str, str]] = None,
        ) -> dict:
            if self._client is None:
                raise ValueError("Client not initialized")

            return (
                self._client.post(url, headers=headers, json=payload)
                .raise_for_status()
                .json()
            )

        def delete(
            self, url: str, *, headers: t.Optional[t.Dict[str, str]] = None
        ) -> None:
            if self._client is None:
                raise ValueError("Client not initialized")

            self._client.delete(url, headers=headers).raise_for_status()

    DEFAULT_CLIENT = HttpxHttpClient
except ImportError:
    pass


def get_client() -> HttpClient:
    if DEFAULT_CLIENT is None:
        raise ImportError("Please install requests or httpx")

    return DEFAULT_CLIENT()
````

## File: tests/test_domain.py
````python
import pytest

from android_sms_gateway.enums import WebhookEvent
from android_sms_gateway.domain import MessageState, RecipientState, Webhook


# Test for successful instantiation from a dictionary
def test_message_state_from_dict():
    payload = {
        "id": "123",
        "state": "Pending",
        "recipients": [
            {"phoneNumber": "123", "state": "Pending"},
            {"phoneNumber": "456", "state": "Pending"},
        ],
        "isHashed": True,
        "isEncrypted": False,
    }

    message_state = MessageState.from_dict(payload)
    assert message_state.id == payload["id"]
    assert message_state.state.name == payload["state"]
    assert all(
        isinstance(recipient, RecipientState) for recipient in message_state.recipients
    )
    assert len(message_state.recipients) == len(payload["recipients"])
    assert message_state.is_hashed == payload["isHashed"]
    assert message_state.is_encrypted == payload["isEncrypted"]


# Test for backward compatibility
def test_message_state_from_dict_backwards_compatibility():
    payload = {
        "id": "123",
        "state": "Pending",
        "recipients": [
            {"phoneNumber": "123", "state": "Pending"},
            {"phoneNumber": "456", "state": "Pending"},
        ],
    }

    message_state = MessageState.from_dict(payload)
    assert message_state.id == payload["id"]
    assert message_state.state.name == payload["state"]
    assert all(
        isinstance(recipient, RecipientState) for recipient in message_state.recipients
    )
    assert len(message_state.recipients) == len(payload["recipients"])
    assert message_state.is_hashed is False
    assert message_state.is_encrypted is False


# Test for handling missing fields
def test_message_state_from_dict_missing_fields():
    incomplete_payload = {
        "id": "123",
        # 'state' is missing
        "recipients": [
            {"phoneNumber": "123", "state": "Pending"}
        ],  # Assume one recipient is enough to test
        "isHashed": True,
        "isEncrypted": False,
    }

    with pytest.raises(KeyError):
        MessageState.from_dict(incomplete_payload)


# Test for handling incorrect types
def test_message_state_from_dict_incorrect_types():
    incorrect_payload = {
        "id": 123,  # Should be a string
        "state": 42,  # Should be a string that can be converted to a ProcessState
        "recipients": "Alice, Bob",  # Should be a list of dictionaries
        "isHashed": "yes",  # Should be a boolean
        "isEncrypted": "no",  # Should be a boolean
    }

    with pytest.raises(
        Exception
    ):  # Replace Exception with the specific exception you expect
        MessageState.from_dict(incorrect_payload)


def test_webhook_from_dict():
    """
    Tests that a Webhook instance can be successfully instantiated from a dictionary
    representation of a webhook.
    """
    payload = {
        "id": "webhook_123",
        "url": "https://example.com/webhook",
        "event": "sms:received",
    }

    webhook = Webhook.from_dict(payload)

    assert webhook.id == payload["id"]
    assert webhook.url == payload["url"]
    assert webhook.event == WebhookEvent(payload["event"])


def test_webhook_asdict():
    """
    Tests that a Webhook instance can be successfully converted to a dictionary
    representation and that the fields match the expected values.

    This test ensures that the asdict method of the Webhook class returns a dictionary
    with the correct keys and values.
    """
    webhook = Webhook(
        id="webhook_123",
        url="https://example.com/webhook",
        event=WebhookEvent.SMS_RECEIVED,
    )

    expected_dict = {
        "id": "webhook_123",
        "url": "https://example.com/webhook",
        "event": "sms:received",
    }

    assert webhook.asdict() == expected_dict

    webhook = Webhook(
        id=None,
        url="https://example.com/webhook",
        event=WebhookEvent.SMS_RECEIVED,
    )

    expected_dict = {
        "id": None,
        "url": "https://example.com/webhook",
        "event": "sms:received",
    }

    assert webhook.asdict() == expected_dict
````

## File: Makefile
````
.PHONY: install test lint build publish clean

# Variables
PACKAGE_NAME=android_sms_gateway
VERSION=$(shell grep '__version__' $(PACKAGE_NAME)/__init__.py | cut -d '"' -f 2)

# Install pipenv and project dependencies
install:
	pipenv install --dev --categories encryption

# Run tests with pytest or unittest
test:
	pipenv run python -m pytest tests

# Lint the project with flake8
lint:
	pipenv run flake8 $(PACKAGE_NAME) tests

# Build the project
build:
	pipenv run python -m build

# Publish the library to PyPI
publish:
	pipenv run twine upload dist/*

# Clean up the project directory
clean:
	pipenv --rm
	rm -rf dist build $(PACKAGE_NAME).egg-info
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
````

## File: Pipfile
````
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]

[dev-packages]
setuptools = "*"
pytest = "*"
black = "*"
flake8 = "*"
wheel = "*"
twine = "*"
build = "*"
importlib-metadata = "*"

[requires]
python_version = "3"

[requests]
requests = "~=2.31"

[httpx]
httpx = "~=0.26"

[aiohttp]
aiohttp = "~=3.9"

[encryption]
pycryptodome = "~=3.20"
````

## File: android_sms_gateway/client.py
````python
import abc
import base64
import dataclasses
import logging
import sys
import typing as t

from . import ahttp, domain, http
from .constants import DEFAULT_URL, VERSION
from .encryption import BaseEncryptor

logger = logging.getLogger(__name__)


class BaseClient(abc.ABC):
    def __init__(
        self,
        login: str,
        password: str,
        *,
        base_url: str = DEFAULT_URL,
        encryptor: t.Optional[BaseEncryptor] = None,
    ) -> None:
        credentials = base64.b64encode(f"{login}:{password}".encode("utf-8")).decode(
            "utf-8"
        )
        self.headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "User-Agent": f"android-sms-gateway/{VERSION} (client; python {sys.version_info.major}.{sys.version_info.minor})",
        }
        self.base_url = base_url.rstrip("/")
        self.encryptor = encryptor

    def _encrypt(self, message: domain.Message) -> domain.Message:
        if self.encryptor is None:
            return message

        if message.is_encrypted:
            raise ValueError("Message is already encrypted")

        message = dataclasses.replace(
            message,
            is_encrypted=True,
            message=self.encryptor.encrypt(message.message),
            phone_numbers=[
                self.encryptor.encrypt(phone) for phone in message.phone_numbers
            ],
        )

        return message

    def _decrypt(self, state: domain.MessageState) -> domain.MessageState:
        if state.is_encrypted and self.encryptor is None:
            raise ValueError("Message is encrypted but encryptor is not set")

        if self.encryptor is None:
            return state

        return dataclasses.replace(
            state,
            recipients=[
                dataclasses.replace(
                    recipient,
                    phone_number=self.encryptor.decrypt(recipient.phone_number),
                )
                for recipient in state.recipients
            ],
            is_encrypted=False,
        )


class APIClient(BaseClient):
    def __init__(
        self,
        login: str,
        password: str,
        *,
        base_url: str = DEFAULT_URL,
        encryptor: t.Optional[BaseEncryptor] = None,
        http: t.Optional[http.HttpClient] = None,
    ) -> None:
        super().__init__(login, password, base_url=base_url, encryptor=encryptor)
        self.http = http
        self.default_http = None

    def __enter__(self):
        if self.http is not None:
            return self

        self.http = self.default_http = http.get_client().__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.default_http is None:
            return

        self.default_http.__exit__(exc_type, exc_val, exc_tb)
        self.http = self.default_http = None

    def send(self, message: domain.Message) -> domain.MessageState:
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        message = self._encrypt(message)
        return self._decrypt(
            domain.MessageState.from_dict(
                self.http.post(
                    f"{self.base_url}/message",
                    payload=message.asdict(),
                    headers=self.headers,
                )
            )
        )

    def get_state(self, _id: str) -> domain.MessageState:
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        return self._decrypt(
            domain.MessageState.from_dict(
                self.http.get(f"{self.base_url}/message/{_id}", headers=self.headers)
            )
        )

    def get_webhooks(self) -> t.List[domain.Webhook]:
        """
        Retrieves a list of all webhooks registered for the account.

        Returns:
            A list of Webhook instances.
        """
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        return [
            domain.Webhook.from_dict(webhook)
            for webhook in self.http.get(
                f"{self.base_url}/webhooks", headers=self.headers
            )
        ]

    def create_webhook(self, webhook: domain.Webhook) -> domain.Webhook:
        """
        Creates a new webhook.

        Args:
            webhook: The webhook to create.

        Returns:
            The created webhook.
        """
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        return domain.Webhook.from_dict(
            self.http.post(
                f"{self.base_url}/webhooks",
                payload=webhook.asdict(),
                headers=self.headers,
            )
        )

    def delete_webhook(self, _id: str) -> None:
        """
        Deletes a webhook.

        Args:
            _id: The ID of the webhook to delete.

        Returns:
            None
        """
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        self.http.delete(f"{self.base_url}/webhooks/{_id}", headers=self.headers)


class AsyncAPIClient(BaseClient):
    def __init__(
        self,
        login: str,
        password: str,
        *,
        base_url: str = DEFAULT_URL,
        encryptor: t.Optional[BaseEncryptor] = None,
        http_client: t.Optional[ahttp.AsyncHttpClient] = None,
    ) -> None:
        super().__init__(login, password, base_url=base_url, encryptor=encryptor)
        self.http = http_client
        self.default_http = None

    async def __aenter__(self):
        if self.http is not None:
            return self

        self.http = self.default_http = await ahttp.get_client().__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.default_http is None:
            return

        await self.default_http.__aexit__(exc_type, exc_val, exc_tb)
        self.http = self.default_http = None

    async def send(self, message: domain.Message) -> domain.MessageState:
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        message = self._encrypt(message)
        return self._decrypt(
            domain.MessageState.from_dict(
                await self.http.post(
                    f"{self.base_url}/message",
                    payload=message.asdict(),
                    headers=self.headers,
                )
            )
        )

    async def get_state(self, _id: str) -> domain.MessageState:
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        return self._decrypt(
            domain.MessageState.from_dict(
                await self.http.get(
                    f"{self.base_url}/message/{_id}", headers=self.headers
                )
            )
        )

    async def get_webhooks(self) -> t.List[domain.Webhook]:
        """
        Retrieves a list of all webhooks registered for the account.

        Returns:
            A list of Webhook instances.
        """
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        return [
            domain.Webhook.from_dict(webhook)
            for webhook in await self.http.get(
                f"{self.base_url}/webhooks", headers=self.headers
            )
        ]

    async def create_webhook(self, webhook: domain.Webhook) -> domain.Webhook:
        """
        Creates a new webhook.

        Args:
            webhook: The webhook to create.

        Returns:
            The created webhook.
        """
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        return domain.Webhook.from_dict(
            await self.http.post(
                f"{self.base_url}/webhooks",
                payload=webhook.asdict(),
                headers=self.headers,
            )
        )

    async def delete_webhook(self, _id: str) -> None:
        """
        Deletes a webhook.

        Args:
            _id: The ID of the webhook to delete.

        Returns:
            None
        """
        if self.http is None:
            raise ValueError("HTTP client not initialized")

        await self.http.delete(f"{self.base_url}/webhooks/{_id}", headers=self.headers)
````

## File: android_sms_gateway/domain.py
````python
import dataclasses
import typing as t

from .enums import ProcessState, WebhookEvent


def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


@dataclasses.dataclass(frozen=True)
class Message:
    message: str
    phone_numbers: t.List[str]
    with_delivery_report: bool = True
    is_encrypted: bool = False

    id: t.Optional[str] = None
    ttl: t.Optional[int] = None
    sim_number: t.Optional[int] = None

    def asdict(self) -> t.Dict[str, t.Any]:
        return {
            snake_to_camel(field.name): getattr(self, field.name)
            for field in dataclasses.fields(self)
            if getattr(self, field.name) is not None
        }


@dataclasses.dataclass(frozen=True)
class RecipientState:
    phone_number: str
    state: ProcessState
    error: t.Optional[str]

    @classmethod
    def from_dict(cls, payload: t.Dict[str, t.Any]) -> "RecipientState":
        return cls(
            phone_number=payload["phoneNumber"],
            state=ProcessState(payload["state"]),
            error=payload.get("error"),
        )


@dataclasses.dataclass(frozen=True)
class MessageState:
    id: str
    state: ProcessState
    recipients: t.List[RecipientState]
    is_hashed: bool
    is_encrypted: bool

    @classmethod
    def from_dict(cls, payload: t.Dict[str, t.Any]) -> "MessageState":
        return cls(
            id=payload["id"],
            state=ProcessState(payload["state"]),
            recipients=[
                RecipientState.from_dict(recipient)
                for recipient in payload["recipients"]
            ],
            is_hashed=payload.get("isHashed", False),
            is_encrypted=payload.get("isEncrypted", False),
        )


@dataclasses.dataclass(frozen=True)
class Webhook:
    """A webhook configuration."""

    id: t.Optional[str]
    """The unique identifier of the webhook."""
    url: str
    """The URL the webhook will be sent to."""
    event: WebhookEvent
    """The type of event the webhook is triggered for."""

    @classmethod
    def from_dict(cls, payload: t.Dict[str, t.Any]) -> "Webhook":
        """Creates a Webhook instance from a dictionary.

        Args:
            payload: A dictionary containing the webhook's data.

        Returns:
            A Webhook instance.
        """
        return cls(
            id=payload.get("id"),
            url=payload["url"],
            event=WebhookEvent(payload["event"]),
        )

    def asdict(self) -> t.Dict[str, t.Any]:
        """Returns a dictionary representation of the webhook.

        Returns:
            A dictionary containing the webhook's data.
        """
        return {
            "id": self.id,
            "url": self.url,
            "event": self.event.value,
        }
````

## File: .github/workflows/testing.yml
````yaml
name: Python CI

on:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pipenv

      - name: Install pipenv
        run: |
          python -m pip install --upgrade pipenv

      - name: Install dependencies
        run: |
          pipenv sync --dev
          pipenv sync --categories encryption

      - name: Lint with flake8
        run: pipenv run flake8 android_sms_gateway tests

      - name: Test with pytest
        run: pipenv run pytest tests
````

## File: pyproject.toml
````toml
[build-system]
requires = ["setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "android-sms-gateway"
description = "A client library for sending and managing SMS messages via the SMS Gateway for Android API"
requires-python = ">=3.9"
authors = [{ name = "Aleksandr Soloshenko", email = "admin@sms-gate.app" }]
maintainers = [{ name = "Aleksandr Soloshenko", email = "support@sms-gate.app" }]
readme = "README.md"
license = { text = "Apache-2.0" }
keywords = ["android", "sms", "gateway"]
dynamic = ["version"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Communications :: Telephony",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]

[tool.setuptools.dynamic]
version = { attr = "android_sms_gateway.__version__" }

[project.urls]
Homepage = "https://sms-gate.app"
Repository = "https://github.com/android-sms-gateway/client-py"

[project.optional-dependencies]
dev = ["setuptools", "pytest", "black", "flake8", "wheel"]
requests = ["requests"]
httpx = ["httpx"]
aiohttp = ["aiohttp"]
encryption = ["pycryptodome"]
````

## File: README.md
````markdown
Segue a tradução para o português brasileiro do conteúdo do README do projeto "SMS Gateway for Android™ Python API Client"[1]:

# 📱 Cliente Python para SMS Gateway for Android™

Um cliente Python moderno para integração transparente com a API do [SMS Gateway for Android](https://sms-gate.app). Envie mensagens SMS programaticamente por meio de seus dispositivos Android com esta biblioteca poderosa e fácil de usar.

## 📖 Índice
- [📱 Cliente Python para SMS Gateway for Android™](#-cliente-python-para-sms-gateway-for-android)
  - [📖 Índice](#-índice)
  - [✨ Funcionalidades](#-funcionalidades)
  - [⚙️ Requisitos](#️-requisitos)
  - [📦 Instalação](#-instalação)
  - [🚀 Primeiros Passos](#-primeiros-passos)
    - [Uso Básico](#uso-básico)
  - [🤖 Guia do Cliente](#-guia-do-cliente)
    - [Configuração do Cliente](#configuração-do-cliente)
    - [Métodos Principais](#métodos-principais)
    - [Definições de Tipos](#definições-de-tipos)
    - [Configuração de Criptografia](#configuração-de-criptografia)
  - [🌐 Clientes HTTP](#-clientes-http)
  - [🔒 Notas de Segurança](#-notas-de-segurança)
  - [📚 Referência da API](#-referência-da-api)
  - [👥 Contribuindo](#-contribuindo)
    - [Ambiente de Desenvolvimento](#ambiente-de-desenvolvimento)
  - [📄 Licença](#-licença)

## ✨ Funcionalidades
- **Suporte a Cliente Duplo**: Escolha entre interfaces síncronas (`APIClient`) e assíncronas (`AsyncAPIClient`)
- **Criptografia de Ponta a Ponta**: Criptografia opcional de mensagens usando AES-CBC-256
- **Múltiplos Backends HTTP**: Suporte a `requests`, `aiohttp` e `httpx`
- **Gestão de Webhooks**: Crie, consulte e exclua webhooks
- **URL Base Personalizável**: Aponte para diferentes endpoints da API
- **Type Hinting**: Totalmente tipado para melhor experiência de desenvolvimento

## ⚙️ Requisitos
- Python 3.9+
- Escolha um cliente HTTP:
  - 🚀 [requests](https://pypi.org/project/requests/) (síncrono)
  - ⚡ [aiohttp](https://pypi.org/project/aiohttp/) (assíncrono)
  - 🌈 [httpx](https://pypi.org/project/httpx/) (síncrono + assíncrono)

**Opcional**:
- 🔒 [pycryptodome](https://pypi.org/project/pycryptodome/) - Para suporte à criptografia ponta a ponta

## 📦 Instalação

Instale o pacote base:
```bash
pip install android_sms_gateway
```

Instale com seu cliente HTTP preferido:
```bash
# Escolha um:
pip install android_sms_gateway[requests]
pip install android_sms_gateway[aiohttp]
pip install android_sms_gateway[httpx]
```

Para mensagens criptografadas:
```bash
pip install android_sms_gateway[encryption]
```

## 🚀 Primeiros Passos

### Uso Básico
```python
import asyncio
import os

from android_sms_gateway import client, domain, Encryptor

login = os.getenv("ANDROID_SMS_GATEWAY_LOGIN")
password = os.getenv("ANDROID_SMS_GATEWAY_PASSWORD")
# para criptografia ponta a ponta, veja https://docs.sms-gate.app/privacy/encryption/
# encryptor = Encryptor('frase-secreta')

message = domain.Message(
    "Seu texto de mensagem aqui.",
    ["+5511999999999"],
)

def sync_client():
    with client.APIClient(
        login, 
        password,
        # encryptor=encryptor,
    ) as c:
        state = c.send(message)
        print(state)

        state = c.get_state(state.id)
        print(state)


async def async_client():
    async with client.AsyncAPIClient(
        login, 
        password,
        # encryptor=encryptor,
    ) as c:
        state = await c.send(message)
        print(state)

        state = await c.get_state(state.id)
        print(state)

print("Cliente síncrono")
sync_client()

print("\nCliente assíncrono")
asyncio.run(async_client())
```

## 🤖 Guia do Cliente

Existem duas classes de cliente: `APIClient` e `AsyncAPIClient`.  
A `APIClient` é síncrona e a `AsyncAPIClient` é assíncrona. Ambas implementam a mesma interface e podem ser usadas como context managers.

### Configuração do Cliente

Ambos os clientes suportam os seguintes parâmetros de inicialização:

| Argumento    | Descrição                | Padrão                                    |
| ------------ | ----------------------- | ----------------------------------------- |
| `login`      | Usuário                 | **Obrigatório**                           |
| `password`   | Senha                   | **Obrigatório**                           |
| `base_url`   | URL base da API         | `"https://api.sms-gate.app/3rdparty/v1"`  |
| `encryptor`  | Instância de Encryptor  | `None`                                    |
| `http`       | Cliente HTTP customizado | Detectado automaticamente                 |

### Métodos Principais

| Método                                           | Descrição                | Retorno                   |
| ------------------------------------------------ | ------------------------ | ------------------------- |
| `send(self, message: domain.Message)`            | Envia uma mensagem       | `domain.MessageState`     |
| `get_state(self, _id: str)`                      | Consulta o estado        | `domain.MessageState`     |
| `create_webhook(self, webhook: domain.Webhook)`  | Cria um novo webhook     | `domain.Webhook`          |
| `get_webhooks(self)`                             | Lista todos os webhooks  | `List[domain.Webhook]`    |
| `delete_webhook(self, _id: str)`                 | Exclui um webhook        | `None`                    |

### Definições de Tipos

```python
class Message:
    message: str
    phone_numbers: t.List[str]
    with_delivery_report: bool = True
    is_encrypted: bool = False

    id: t.Optional[str] = None
    ttl: t.Optional[int] = None
    sim_number: t.Optional[int] = None


class MessageState:
    id: str
    state: ProcessState
    recipients: t.List[RecipientState]
    is_hashed: bool
    is_encrypted: bool

class Webhook:
    id: t.Optional[str]
    url: str
    event: WebhookEvent
```

Para mais detalhes, veja [`domain.py`](./android_sms_gateway/domain.py).

### Configuração de Criptografia
```python
from android_sms_gateway import client, Encryptor

# Inicialize com sua frase secreta
encryptor = Encryptor("minha-frase-secreta")

# Use na inicialização do cliente
client.APIClient(login, password, encryptor=encryptor)
```

## 🌐 Clientes HTTP
A biblioteca detecta automaticamente os clientes HTTP instalados. Prioridade:

| Cliente   | Síncrono | Assíncrono |
| --------- | -------- | ---------- |
| aiohttp   | ❌       | 1️⃣         |
| requests  | 1️⃣       | ❌         |
| httpx     | 2️⃣       | 2️⃣         |

Para usar um cliente específico:
```python
# Forçar uso do cliente síncrono httpx
client.APIClient(..., http=http.HttpxHttpClient())
```

Você também pode implementar seu próprio cliente HTTP que siga o protocolo `http.HttpClient` ou `ahttp.HttpClient`.

## 🔒 Notas de Segurança

⚠️ **Práticas Importantes de Segurança**
- Sempre armazene credenciais em variáveis de ambiente
- Nunca exponha credenciais em código do lado do cliente
- Use HTTPS para todas as comunicações em produção

## 📚 Referência da API
Para documentação completa da API, incluindo todos os métodos disponíveis, esquemas de requisição/resposta e códigos de erro, acesse:  
[📘 Documentação Oficial da API](https://docs.sms-gate.app/integration/api/)

## 👥 Contribuindo
Contribuições são bem-vindas! Veja como ajudar:

1. Faça um fork do repositório
2. Crie sua branch de funcionalidade (`git checkout -b feature/NovaFuncionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona NovaFuncionalidade'`)
4. Faça push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Ambiente de Desenvolvimento
```bash
git clone https://github.com/android-sms-gateway/client-py.git
cd client-py
pipenv install --dev --categories encryption,requests
pipenv shell
```

## 📄 Licença
Distribuído sob a Licença Apache 2.0. Veja [LICENSE](LICENSE) para mais informações.

**Nota**: Android é uma marca registrada da Google LLC. Este projeto não é afiliado nem endossado pela Google[1].

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/44487462/84be9ca8-aef9-40b2-a817-0e5d29ec814a/paste-2.txt
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/44487462/5d57bb9e-c735-4030-bf52-cb19e4556c77/paste.txt
````
