function showToast(message, type = "success") {
    let toast = document.getElementById("toast");
    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast";
        document.body.appendChild(toast);
    }

    toast.innerText = message;
    toast.style.borderLeftColor = type === "error" ? "#f44336" : "#ffb700";
    toast.style.background = type === "error"
        ? "rgba(244, 67, 54, 0.15)"
        : "#1a1a1a";

    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 4000);
}