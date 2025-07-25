document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modalNovaSala');
    const abrirModalBtn = document.getElementById('abrirModalBtn');
    const closeBtn = document.querySelector('.modal-close');
    const cancelBtn = document.querySelector('.btn-cancelar');
    
    function abrirModal() {
        modal.style.display = 'block';
    }
    
    function fecharModal() {
        modal.style.display = 'none';
        // Limpa os campos do formulário ao fechar
        document.getElementById('nomeSala').value = '';
        document.getElementById('statusSala').selectedIndex = 0;
    }
    
    // Event listeners
    abrirModalBtn.addEventListener('click', abrirModal);
    closeBtn.addEventListener('click', fecharModal);
    cancelBtn.addEventListener('click', fecharModal);
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            fecharModal();
        }
    });
    
    // Validação do formulário
    const form = document.querySelector('.modal-form');
    form.addEventListener('submit', function(e) {
        const nome = document.getElementById('nomeSala').value.trim();
        const status = document.getElementById('statusSala').value;
        
        if (!nome || !status) {
            e.preventDefault();
            alert('Por favor, preencha todos os campos obrigatórios!');
        }
    });
});

flatpickr(".datepicker", {
    dateFormat: "d/m/Y",
    locale: "pt",
    allowInput: true,
    static: true
});

// Formata as datas na tabela para o padrão brasileiro
document.addEventListener('DOMContentLoaded', function() {
    const dates = document.querySelectorAll('td:nth-child(6)');
    dates.forEach(function(dateCell) {
        if (dateCell.textContent.trim()) {
            const parts = dateCell.textContent.split('-');
            if (parts.length === 3) {
                dateCell.textContent = `${parts[2]}/${parts[1]}/${parts[0]}`;
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Mostrar/ocultar senha
    const togglePassword = document.querySelector('.btn-toggle-password');
    const password = document.getElementById('senha');
    
    if (togglePassword && password) {
        togglePassword.addEventListener('click', function() {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye-slash');
            this.querySelector('i').classList.toggle('fa-eye');
        });
    }
    
    // Máscara para matrícula (apenas números)
    const matricula = document.getElementById('matricula');
    if (matricula) {
        matricula.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
});