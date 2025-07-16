function abrirModal() {
  document.getElementById("modalNovaSala").style.display = "block";
}
function fecharModal() {
  document.getElementById("modalNovaSala").style.display = "none";
}

function abrirModalReserva(salaId, salaNome) {
    try {
        // Verifica se o modal existe
        const modal = document.getElementById('modalReserva');
        if (!modal) {
            console.error('Elemento modal não encontrado');
            return;
        }

        document.getElementById('salaId').value = salaId;
        document.getElementById('nomeSala').textContent = salaNome;


        const today = new Date().toISOString().split('T')[0];
        const dateInput = document.querySelector('input[name="data_reserva"]');
        if (dateInput) {
            dateInput.min = today;
            dateInput.value = today; 
        }

        modal.style.display = 'block';
        
    } catch (error) {
        console.error('Erro ao abrir modal:', error);
        alert('Ocorreu um erro ao abrir o formulário de reserva');
    }
}

function fecharModal() {
    document.getElementById('modalReserva').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('modalReserva');
    if (event.target == modal) {
        fecharModal();
    }
}


document.getElementById('formReserva').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/reservar', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Reserva realizada com sucesso!');
            fecharModal();
            // Atualizar a página ou a interface conforme necessário
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocorreu um erro ao processar a reserva');
    });
});