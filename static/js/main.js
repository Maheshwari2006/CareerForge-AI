document.addEventListener("DOMContentLoaded", () => {
    const menu = document.getElementById("mobileMenu");
    const sidebar = document.getElementById("sidebar");
    if (menu && sidebar) {
        menu.addEventListener("click", () => sidebar.classList.toggle("open"));
    }
});

function toggleField(id, button) {
    const field = document.getElementById(id);
    if (!field) return;
    const icon = button.querySelector("i");
    if (field.type === "password") {
        field.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        field.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}
