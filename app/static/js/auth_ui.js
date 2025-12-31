document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);

    // ================= SINGLE TOAST SYSTEM (FORCED ENGLISH) =================
    // Gestisce i messaggi di errore e successo con stile coerente al tema
    window.showToast = function (message, type = "success") {
        let toast = document.getElementById("toast");

        if (!toast) {
            toast = document.createElement("div");
            toast.id = "toast";
            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.className = "toast show";
        
        // Colori dinamici in base al tipo (Errore = Rosso, Successo = Oro/Nero)
        toast.style.borderLeftColor = type === "error" ? "#f44336" : "#f5c400";
        toast.style.background = type === "error" ? "rgba(244,67,54,0.15)" : "#1a1a1a";

        setTimeout(() => {
            toast.classList.remove("show");
        }, 4000);
    };

    // ================= MODAL SELECTION =================
    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");
    const forgotModal = document.getElementById("forgotModal");
    const resetPinModal = document.getElementById("resetPinModal");
    const deleteModal = document.getElementById("deleteModal");

    const modals = [loginModal, registerModal, forgotModal, resetPinModal, deleteModal].filter(Boolean);

    /**
     * Apre un modal specifico e chiude gli altri.
     * Applica il focus automatico sul primo input disponibile.
     */
    function openModal(modal) {
        closeAllModals();
        if (!modal) return;
        modal.classList.add("show");
        setTimeout(() => {
            modal.querySelector("input")?.focus();
        }, 150);
    }

    function closeAllModals() {
        modals.forEach(m => m.classList.remove("show"));
    }

    // ================= EVENT LISTENERS =================
    
    // Trigger Apertura Modal via attributi data
    document.querySelectorAll("[data-open-login]").forEach(el => 
        el.addEventListener("click", () => openModal(loginModal)));

    document.querySelectorAll("[data-open-register]").forEach(el => 
        el.addEventListener("click", () => openModal(registerModal)));

    document.querySelectorAll("[data-open-forgot]").forEach(el => 
        el.addEventListener("click", () => openModal(forgotModal)));

    document.querySelectorAll("[data-open-delete]").forEach(el => 
        el.addEventListener("click", () => openModal(deleteModal)));

    // Trigger Chiusura
    document.querySelectorAll(".close-modal").forEach(btn => 
        btn.addEventListener("click", closeAllModals));

    // Chiude il modal cliccando sullo sfondo oscurato
    modals.forEach(modal => {
        modal.addEventListener("click", e => {
            if (e.target === modal) closeAllModals();
        });
    });

    // ================= TOGGLE PASSWORD (EYE LOGIC) =================
    // Gestisce il cambio visibilità password e aggiorna l'icona con glow
    document.querySelectorAll(".toggle-password").forEach(toggle => {
        toggle.addEventListener("click", () => {
            const input = toggle.closest(".input-group")?.querySelector("input");
            const icon = toggle.querySelector("img");

            if (!input || !icon) return;

            if (input.type === "password") {
                input.type = "text";
                icon.src = "/static/images/eye_open.png";
            } else {
                input.type = "password";
                icon.src = "/static/images/eye_closed.png";
            }
        });
    });

    // ================= FORM VALIDATION & NO-VALIDATE =================
    // Sostituisce i messaggi di sistema del browser con Toast personalizzati in inglese
    document.querySelectorAll(".modal form").forEach(form => {
        form.setAttribute("novalidate", "true");

        form.addEventListener("submit", e => {
            // Controllo campi obbligatori
            const required = form.querySelectorAll("input[required]");
            for (const input of required) {
                if (!input.value.trim()) {
                    e.preventDefault();
                    showToast("Please fill in all required fields", "error");
                    input.focus();
                    return; 
                }
            }

            // Validazione specifica per il PIN (solo 6 cifre numeriche)
            const pinInput = form.querySelector("input[name='pin']");
            if (pinInput && pinInput.value.trim() !== "" && !/^\d{6}$/.test(pinInput.value)) {
                e.preventDefault();
                showToast("PIN must be exactly 6 digits", "error");
                pinInput.focus();
            }
        });
    });

    // ================= URL PARAM & AUTO-OPEN LOGIC =================
    // Gestisce l'apertura automatica dei modal tramite link email o redirect backend
    const open = params.get("open");
    const usernameParam = params.get("username");

    if (open) {
        if (open === "login") openModal(loginModal);
        else if (open === "register") openModal(registerModal);
        else if (open === "forgot") openModal(forgotModal);
        else if (open === "reset-pin") openModal(resetPinModal);

        // Se l'URL contiene lo username, lo pre-compila nel form di recupero
        if (usernameParam) {
            const targetModal = resetPinModal.classList.contains('show') ? resetPinModal : forgotModal;
            const input = targetModal.querySelector("input[name='username']");
            if (input) input.value = usernameParam;
        }
        
        // Pulisce i parametri dall'URL per evitare riaperture al refresh
        history.replaceState({}, "", window.location.pathname);
    }

    // Logica di fallback se il backend rileva un errore nel PIN
    if (document.getElementById("pinToast")) {
        openModal(resetPinModal);
        if (usernameParam) {
            const input = resetPinModal.querySelector("input[name='username']");
            if (input) input.value = usernameParam;
        }
    }
});