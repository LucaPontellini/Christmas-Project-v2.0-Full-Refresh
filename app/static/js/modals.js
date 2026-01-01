document.addEventListener('DOMContentLoaded', () => {
    
    // 1. MAPPATURA DEI MODAL
    // Memorizziamo i riferimenti agli elementi DOM per performance e pulizia
    const modals = {
        login: document.getElementById('loginModal'),
        register: document.getElementById('registerModal'),
        forgot: document.getElementById('forgotModal'),
        recoveryComplete: document.getElementById('recoveryCompleteModal'),
        deleteAccount: document.getElementById('deleteAccountModal')
    };

    // 2. FUNZIONI DI CONTROLLO (WINDOW = DISPONIBILI NEGLI ONCLICK HTML)
    
    // Chiude tutti i modal attivi
    window.closeAll = function() {
        Object.values(modals).forEach(modal => {
            if (modal) modal.classList.remove('show');
        });
    };

    // Apre un modal specifico con logica di transizione e focus
    window.openModal = function(type) {
        closeAll();
        
        // Timeout per permettere una transizione fluida tra un modal e l'altro
        setTimeout(() => {
            const modal = modals[type];
            if (!modal) return;

            modal.classList.add('show');

            // --- Logiche Specifiche per Modal ---
            
            // Focus automatico sul campo PIN (se presente)
            const pinInput = modal.querySelector('input[name="pin"]');
            if (pinInput) pinInput.focus();

            // Sincronizzazione automatica Username tra Forgot e Recovery
            if (type === 'recoveryComplete') {
                const usernameInput = modal.querySelector('input[name="username"]');
                const forgotUsername = document.querySelector('#forgotModal input[name="username"]')?.value;
                
                if (usernameInput && forgotUsername && !usernameInput.value) {
                    usernameInput.value = forgotUsername;
                }
            }
        }, 80);
    };

    // 3. EVENT LISTENERS GENERALI
    
    // Chiusura cliccando fuori dal contenuto (sull'overlay scuro)
    window.onclick = (e) => {
        if (e.target.classList.contains('modal')) {
            closeAll();
        }
    };

    // 4. LOGICA AUTO-APERTURA (DA FLASH MESSAGES)
    // window.FLASH_TARGET_MODAL viene definita nello script inline dentro modals.html
    if (window.FLASH_TARGET_MODAL) {
        openModal(window.FLASH_TARGET_MODAL);
    }

    // 5. VALIDAZIONE PASSWORD LIVE (MODAL RECOVERY)
    const newPass = document.getElementById('new_password');
    const confirmPass = document.getElementById('confirm_password');

    if (newPass && confirmPass) {
        const updateRules = () => {
            const p = newPass.value;
            const c = confirmPass.value;

            // Mapping dei requisiti grafici
            const requirements = {
                'req-length': p.length >= 6,
                'req-upper': /[A-Z]/.test(p),
                'req-num': /\d/.test(p),
                'req-match': p === c && p !== ""
            };

            // Aggiornamento classi CSS
            Object.keys(requirements).forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.toggle('valid', requirements[id]);
            });
        };

        newPass.addEventListener('input', updateRules);
        confirmPass.addEventListener('input', updateRules);
    }
});