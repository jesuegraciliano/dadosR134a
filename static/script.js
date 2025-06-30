document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('calc-form');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorDiv.classList.add('hidden');
        resultDiv.classList.add('hidden');

        const tempValue = document.getElementById('temp-input').value;

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ temperature: tempValue })
            });

            const data = await response.json();

            if (!response.ok) {
                // Mensagem de erro vinda do backend
                errorDiv.textContent = data.error || 'Erro desconhecido.';
                errorDiv.classList.remove('hidden');
                return;
            }

            // Preenchendo resultados
            document.getElementById('pressure').textContent = data.pressure.toFixed(2);
            document.getElementById('hl').textContent       = data.hl.toFixed(2);
            document.getElementById('hv').textContent       = data.hv.toFixed(2);
            document.getElementById('latent').textContent   = data.latent_heat.toFixed(2);

            resultDiv.classList.remove('hidden');
        } catch (err) {
            errorDiv.textContent = `Falha de comunicação: ${err.message}`;
            errorDiv.classList.remove('hidden');
        }
    });
});
