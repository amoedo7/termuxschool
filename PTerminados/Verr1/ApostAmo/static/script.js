
document.addEventListener('DOMContentLoaded', function() {
    // Formulario de creación de apuesta
    const createBetForm = document.getElementById('createBetForm');
    if (createBetForm) {
        createBetForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                question: document.getElementById('question').value,
                option_a: document.getElementById('option_a').value,
                option_b: document.getElementById('option_b').value,
                end_time: document.getElementById('end_time').value
            };

            try {
                const response = await fetch('/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                const data = await response.json();
                window.location.href = `/bet/${data.bet_id}`;
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    // Formulario para realizar apuesta
    const placeBetForm = document.getElementById('placeBetForm');
    if (placeBetForm) {
        placeBetForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                side: document.getElementById('bet_side').value,
                amount: document.getElementById('bet_amount').value
            };

            try {
                const betId = window.location.pathname.split('/').pop();
                const response = await fetch(`/bet/${betId}/place`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                const data = await response.json();
                updateBetStatus(data);
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }
});

function updateBetStatus(data) {
    const totalA = document.getElementById('total-a');
    const totalB = document.getElementById('total-b');
    if (totalA) totalA.textContent = data.total_a;
    if (totalB) totalB.textContent = data.total_b;
}
