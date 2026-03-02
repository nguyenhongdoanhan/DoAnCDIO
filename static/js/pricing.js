function choosePlan(plan) {

    fetch("/update-plan/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "plan=" + plan
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("Đã cập nhật gói: " + data.plan);
            location.reload();
        }
    });
}


/* Lấy CSRF token từ cookie */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}