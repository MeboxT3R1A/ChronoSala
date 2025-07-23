document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.form-entregar').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            const dataReserva = this.dataset.dataReserva;  // Ex: '2025-07-22'
            const hoje = new Date().toISOString().split('T')[0];

            if (dataReserva !== hoje) {
                event.preventDefault();
                alert("Você só pode entregar a chave no dia da reserva!\nData da reserva: " + dataReserva);
            } else {
                const confirmar = confirm("Você tem certeza que quer entregar a chave?");
                if (!confirmar) {
                    event.preventDefault();
                }
            }
        });
    });
});
