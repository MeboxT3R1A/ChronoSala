// static/js/coordenador.js

function abrirModal() {
    var myModal = new bootstrap.Modal(document.getElementById('modalNovaSala'));
    myModal.show();
}

// Opcional: Resetar o formulário quando o modal for fechado
document.getElementById('modalNovaSala')?.addEventListener('hidden.bs.modal', function () {
    document.getElementById('formNovaSala')?.reset();
});