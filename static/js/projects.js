// ===============================
// PROJECT SEARCH (FIXED VERSION)
// ===============================

document.addEventListener("input", function (e) {

    if (e.target.id === "projectSearch") {

        const keyword = e.target.value.toLowerCase().trim();
        const projectItems = document.querySelectorAll(".project-item");

        projectItems.forEach(function (item) {

            const text = item.textContent.toLowerCase();

            if (text.includes(keyword)) {
                item.style.display = "";        // Trả về display mặc định
            } else {
                item.style.display = "none";    // Ẩn nếu không khớp
            }

        });
    }

});


// ===============================
// CREATE PROJECT BUTTON
// ===============================

document.addEventListener("click", function (e) {

    if (e.target.classList.contains("btn-create")) {
        window.location.href = "/dashboard/";
    }

});
// ===============================
// PROJECT SEARCH
// ===============================

document.addEventListener("input", function (e) {

    if (e.target.id === "projectSearch") {

        const keyword = e.target.value.toLowerCase().trim();
        const projectItems = document.querySelectorAll(".project-item");

        projectItems.forEach(function (item) {
            const text = item.textContent.toLowerCase();

            if (text.includes(keyword)) {
                item.style.display = "";
            } else {
                item.style.display = "none";
            }
        });
    }

});


// ===============================
// CREATE PROJECT BUTTON
// ===============================

document.addEventListener("click", function (e) {

    if (e.target.classList.contains("btn-create")) {
        window.location.href = "/dashboard/";
    }

});


// =======================================
// CLICK CARD "TỪ FILE VĂN BẢN"
// =======================================

document.addEventListener("click", function (e) {

    const card = e.target.closest(".action-card");

    if (!card) return;

    if (card.innerText.toLowerCase().includes("file văn bản")) {
        uploadTextFile();
    }

});


// =======================================
// UPLOAD DOCX / PDF
// =======================================

function uploadTextFile() {

    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".docx,.pdf";

    input.onchange = function () {

        const file = input.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        fetch("/api/upload-text/", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {

            console.log("Upload response:", data); // debug

            if (data.success) {

                //  LƯU TEXT
                localStorage.setItem("uploaded_text", data.text);

                console.log("Saved to localStorage:", data.text);

                window.location.href = "/dashboard/";
            } else {
                alert(data.error || "Lỗi upload file");
            }

        })
        .catch(error => {
            console.error("Upload error:", error);
            alert("Lỗi upload file");
        });

    };

    input.click();
}
// =======================================
// CLICK CARD "TẢI LÊN ÂM THANH"
// =======================================

document.addEventListener("click", function (e) {

    const card = e.target.closest(".action-card");
    if (!card) return;

    if (card.innerText.toLowerCase().includes("tải lên âm thanh")) {

        const audioInput = document.getElementById("audioInput");
        if (audioInput) {
            audioInput.click();
        }

    }

});


// ===============================
// PROJECT SEARCH
// ===============================

document.addEventListener("input", function (e) {

    if (e.target.id === "projectSearch") {

        const keyword = e.target.value.toLowerCase().trim();
        const projectItems = document.querySelectorAll(".project-item");

        projectItems.forEach(function (item) {

            const text = item.textContent.toLowerCase();

            if (text.includes(keyword)) {
                item.style.display = "";
            } else {
                item.style.display = "none";
            }

        });
    }

});


// ===============================
// CREATE PROJECT BUTTON
// ===============================

document.addEventListener("click", function (e) {

    if (e.target.classList.contains("btn-create")) {
        window.location.href = "/dashboard/";
    }

});


// =======================================
// CLICK ACTION CARDS
// =======================================

document.addEventListener("click", function (e) {

    const card = e.target.closest(".action-card");
    if (!card) return;

    const text = card.innerText.toLowerCase();

    // 📁 FILE VĂN BẢN
    if (text.includes("file văn bản")) {
        uploadTextFile();
    }

    // 🎧 TẢI LÊN ÂM THANH
    if (text.includes("tải lên âm thanh")) {
        uploadAudioFile();
    }

});


// =======================================
// UPLOAD DOCX / PDF
// =======================================

function uploadTextFile() {

    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".docx,.pdf";

    input.onchange = function () {

        const file = input.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        fetch("/api/upload-text/", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {

            if (data.success) {

                localStorage.setItem("uploaded_text", data.text);
                window.location.href = "/dashboard/";

            } else {
                alert(data.error || "Lỗi upload file");
            }

        })
        .catch(error => {
            console.error(error);
            alert("Lỗi upload file");
        });

    };

    input.click();
}


// =======================================
// UPLOAD AUDIO (.mp3 / .wav)
// =======================================

function uploadAudioFile() {

    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".mp3,.wav";

    input.onchange = function () {

        const file = input.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("audio", file);

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                const cookies = document.cookie.split(";");
                for (let cookie of cookies) {
                    cookie = cookie.trim();
                    if (cookie.startsWith(name + "=")) {
                        cookieValue = decodeURIComponent(
                            cookie.substring(name.length + 1)
                        );
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie("csrftoken");

        fetch("/api/upload-audio/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": csrftoken
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {

            console.log("API trả về:", data);

            if (data.error) {
                alert(data.error);
                return;
            }

            // 🔥 Chỉ cần có key text là coi như thành công
            if (data.text !== undefined) {

                localStorage.setItem("uploaded_text", data.text || "");
                window.location.href = "/dashboard/";

            } else {
                alert("Server không trả về text");
            }

        })
        .catch(err => {
            console.error(err);
            alert("Lỗi upload audio");
        });

    };

    input.click();
}