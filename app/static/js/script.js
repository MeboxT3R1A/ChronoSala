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

// static/js/script.js

// Substitua a função atual por esta versão mais robusta
function toggleSidebar() {
    console.log("Botão clicado"); // Para debug
    const sidebar = document.getElementById("sidebar");
    if (!sidebar) {
        console.error("Elemento sidebar não encontrado");
        return;
    }
    
    const body = document.body;
    sidebar.classList.toggle("active");
    body.classList.toggle("sidebar-open");
    
    // Adicione um overlay quando o sidebar estiver aberto
    if (sidebar.classList.contains("active")) {
        createOverlay();
    } else {
        removeOverlay();
    }
}

function createOverlay() {
    let overlay = document.getElementById("sidebar-overlay");
    if (!overlay) {
        overlay = document.createElement("div");
        overlay.id = "sidebar-overlay";
        overlay.style.position = "fixed";
        overlay.style.top = "0";
        overlay.style.left = "0";
        overlay.style.width = "100vw";
        overlay.style.height = "100vh";
        overlay.style.zIndex = "999";
        overlay.onclick = function() {
            toggleSidebar();
        };
        document.body.appendChild(overlay);
    }
}

function removeOverlay() {
    const overlay = document.getElementById("sidebar-overlay");
    if (overlay) {
        overlay.remove();
    }
}

// Fechar o sidebar quando clicar fora (opcional)
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.querySelector('.sidebar-toggle');
    
    if (!sidebar.contains(event.target) && event.target !== toggleBtn) {
        sidebar.classList.remove('active');
        document.body.classList.remove('sidebar-open');
        toggleBtn.classList.add('closed');
    }
});

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