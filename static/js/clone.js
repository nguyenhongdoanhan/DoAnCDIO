function goFast() {
    window.location.href = "/dashboard/";
}

function goPremium() {
    window.location.href = "/pricing/";
}

/* Animation khi load trang */
document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".clone-card");

    cards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(() => {
            card.style.transition = "all 0.5s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, index * 200);
    });
});