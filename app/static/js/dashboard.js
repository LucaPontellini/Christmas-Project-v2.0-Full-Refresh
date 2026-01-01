// --- 1. GESTIONE BILANCIO ---
document.querySelectorAll('.add-balance-form').forEach(form => {
    const input = form.querySelector('input[name="amount"]');
    const btnAdd = form.querySelector('.btn-add');
    const btnSub = form.querySelector('.btn-sub');
    
    input.addEventListener('input', () => {
        const val = parseInt(input.value, 10);
        const invalid = isNaN(val) || val <= 0;
        btnAdd.disabled = invalid; 
        btnSub.disabled = invalid;
    });
});

// --- 2. NAVIGAZIONE SIDEBAR ---
document.querySelectorAll('.menu-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelectorAll('.menu-link').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
        
        const target = document.getElementById(this.dataset.target);
        if (target) {
            target.classList.add('highlight-glow');
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => target.classList.remove('highlight-glow'), 1500);
        }
    });
});

// --- 3. LOGICA MODALE HARD DELETE ---
const modal = document.getElementById('hard-delete-modal');
const modalUser = document.getElementById('modal-username');
let deleteForm = null;

document.querySelectorAll('.hard-delete-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        modalUser.textContent = this.dataset.username;
        deleteForm = this.closest('form'); 
        modal.style.display = 'flex';
    });
});

document.getElementById('cancel-delete').onclick = () => {
    modal.style.display = 'none';
    deleteForm = null;
};

document.getElementById('confirm-delete').onclick = () => { 
    if(deleteForm) {
        deleteForm.submit(); 
    }
};

window.onclick = (event) => {
    if (event.target == modal) {
        modal.style.display = 'none';
        deleteForm = null;
    }
};