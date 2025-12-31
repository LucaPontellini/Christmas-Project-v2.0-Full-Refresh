document.addEventListener("DOMContentLoaded", () => {

    const bonusButtons = document.querySelectorAll(".claim-bonus");
    if (!bonusButtons.length) return;

    bonusButtons.forEach(btn => {
        btn.addEventListener("click", async () => {

            // 🔒 sicurezza extra (server già protegge)
            if (!document.querySelector(".user-avatar.logged-in")) {
                if (window.showToast) {
                    showToast("Please log in to claim the bonus", "error");
                }
                return;
            }

            if (btn.disabled) return;

            const method = btn.dataset.type;
            if (!method) return;

            btn.disabled = true;
            const originalText = btn.innerText;
            btn.innerText = "Activating...";

            try {
                const res = await fetch("/bonus/claim", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ method })
                });

                const data = await res.json();

                if (!res.ok) {
                    throw new Error(data.error || "Unable to activate bonus");
                }

                // 💰 aggiorna saldo se presente
                const balanceEl = document.getElementById("user-balance");
                if (balanceEl && typeof data.new_balance === "number") {
                    balanceEl.innerText = "€" + data.new_balance.toFixed(2);
                }

                // 🎉 feedback
                if (window.showToast) {
                    showToast("Bonus activated successfully 🎁", "success");
                }

                // UI success
                btn.innerText = "Activated ✓";
                btn.classList.add("claimed");

                // disabilita gli altri bonus
                document.querySelectorAll(".claim-bonus").forEach(other => {
                    if (other !== btn) {
                        other.disabled = true;
                        other.innerText = "Not available";
                        other.closest(".bonus-option")?.classList.add("disabled");
                    }
                });

            } catch (err) {
                console.error(err);
                if (window.showToast) {
                    showToast(err.message || "Connection error", "error");
                }
                btn.disabled = false;
                btn.innerText = originalText;
            }
        });
    });

});