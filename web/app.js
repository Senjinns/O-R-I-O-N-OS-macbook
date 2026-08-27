async function actualiserStatus() {
    try {
        const resp = await fetch('/api/panneau/info');
        const data = await resp.json();
        if (data.budget) {
            const b = data.budget;
            document.getElementById('budget-text').innerText = ;
            document.getElementById('budget-progress').style.width = ;
        }
    } catch (e) {}
}

async function envoyerCommande() {
    const input = document.getElementById('cmd-input');
    const out = document.getElementById('cmd-output');
    const texte = input.value.trim();
    if (!texte) return;
    out.innerText = '⏳ ORION traite votre commande...';
    try {
        const resp = await fetch('/api/commande', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({commande: texte})
        });
        const data = await resp.json();
        out.innerText = data.reponse || 'Aucune réponse.';
        input.value = '';
    } catch (e) {
        out.innerText = 'Erreur : ' + e;
    }
}

document.getElementById('cmd-input').addEventListener('keypress', (e) => { if (e.key === 'Enter') envoyerCommande(); });
setInterval(actualiserStatus, 5000);
actualiserStatus();
