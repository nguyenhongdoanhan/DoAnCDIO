document.addEventListener("DOMContentLoaded", function () {

    // Load theme khi vào bất kỳ trang nào
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
    }

});