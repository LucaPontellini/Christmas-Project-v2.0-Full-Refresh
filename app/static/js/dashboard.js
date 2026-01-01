document.addEventListener('DOMContentLoaded', () => {

    /* GESTIONE BILANCIO (+ / -) */
    // Abilita i pulsanti solo con numero valido > 0
    document.querySelectorAll('.add-balance-form').forEach(form => {
        const input = form.querySelector('input[name="amount"]');
        const btnAdd = form.querySelector('.btn-add');
        const btnSub = form.querySelector('.btn-sub');

        if (!input || !btnAdd || !btnSub) return;

        input.addEventListener('input', () => {
            const val = parseInt(input.value, 10);
            const isInvalid = isNaN(val) || val <= 0;
            btnAdd.disabled = isInvalid;
            btnSub.disabled = isInvalid;
        });
    });

    /* NAVIGAZIONE SIDEBAR */
    // Cambio sezione + evidenziazione + scroll fluido
    document.querySelectorAll('.menu-link').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();

            const targetId = link.dataset.target;
            const target = document.getElementById(targetId);
            
            if (!target) return;

            // Evidenziazione link attivo
            document.querySelectorAll('.menu-link')
                .forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Scroll fluido con effetto glow temporaneo
            target.classList.add('highlight-glow');
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });

            setTimeout(() => {
                target.classList.remove('highlight-glow');
            }, 1500);
        });
    });

    /* MODALE HARD DELETE (con fix metodo 405) */
    const modal = document.getElementById('hard-delete-modal');
    const modalUsername = document.getElementById('modal-username');
    const cancelBtn = document.getElementById('cancel-delete');
    const hardDeleteForm = document.getElementById('hard-delete-form');

    // Apertura modale: inietta username e URL dinamico
    document.querySelectorAll('.hard-delete-btn').forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault(); // Previene submission accidentale se il btn è dentro un form

            const username = btn.dataset.username;
            const actionUrl = btn.dataset.url; // URL generato dal backend (Flask)

            if (modalUsername) modalUsername.textContent = username;
            if (hardDeleteForm && actionUrl) {
                hardDeleteForm.setAttribute('action', actionUrl);
            }

            if (modal) modal.style.display = 'flex';
        });
    });

    // Chiusura modale
    const closeModal = () => {
        if (modal) modal.style.display = 'none';
        if (hardDeleteForm) hardDeleteForm.setAttribute('action', ''); // Pulizia sicurezza
    };

    cancelBtn?.addEventListener('click', closeModal);

    // Chiusura cliccando sullo sfondo
    window.addEventListener('click', e => {
        if (e.target === modal) closeModal();
    });

    /* SERVER STATUS (effetto heartbeat) */
    setInterval(() => {
        const dot = document.querySelector('.status-dot-online');
        if (!dot) return;

        dot.style.opacity = '0.5';
        setTimeout(() => dot.style.opacity = '1', 500);
    }, 30000);

    /* AUTO-HIDE FLASH MESSAGES */
    // Nasconde gradualmente i messaggi flash dopo 5 secondi
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 600); // Rimuove dal DOM dopo fade-out
        }, 5000);
    });

});