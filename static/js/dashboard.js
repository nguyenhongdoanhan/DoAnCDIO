let selectedVoice = "female";

/* ================= VOICE SELECT ================= */
function selectVoice(voice, element) {
    selectedVoice = voice;

    document.querySelectorAll(".voice")
        .forEach(v => v.classList.remove("active"));

    element.classList.add("active");
}

/* ================= COUNTER ================= */
function updateCounter() {

    const text = document.getElementById("textInput").value;

    const maxLength = document.getElementById("textInput").getAttribute("maxlength");

    document.getElementById("charCounter").innerText =
        text.length + " / " + maxLength + " ký tự";
}

/* ================= PASTE ================= */
function pasteText() {
    navigator.clipboard.readText().then(text => {
        document.getElementById("textInput").value = text;
        updateCounter();
    });
}

/* ================= CLEAR ================= */
function clearText() {
    document.getElementById("textInput").value = "";
    updateCounter();
}

/* ================= GET CSRF ================= */
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

/* ================= CONVERT ================= */
async function convertTextToSpeech() {

    const text = document.getElementById("textInput").value.trim();
    const rate = document.getElementById("rateInput").value;
    const pitch = document.getElementById("pitchInput").value;

    if (!text) {
        alert("Vui lòng nhập nội dung");
        return;
    }

    const csrftoken = getCookie("csrftoken");

    try {

        const response = await fetch("/api/tts/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                text: text,
                voice: selectedVoice,
                rate: rate,
                pitch: pitch
            })
        });

        if (!response.ok) {
            const err = await response.json();
            alert("Lỗi: " + (err.detail || JSON.stringify(err)));
            return;
        }

        const result = await response.json();

        if (result.audio_url) {
            const audioPlayer = document.getElementById("audioPlayer");
            audioPlayer.src = result.audio_url;
            audioPlayer.style.display = "block";
            audioPlayer.play();
        } else {
            alert("Không nhận được audio từ server");
        }

    } catch (error) {
        console.error(error);
        alert("Lỗi kết nối server");
    }
}
/* ================= LOAD TEXT FROM UPLOAD ================= */
document.addEventListener("DOMContentLoaded", function () {

    const savedText = localStorage.getItem("uploaded_text");

    if (!savedText) return;

    const textarea = document.getElementById("textInput");

    if (textarea) {
        textarea.value = savedText;
        updateCounter(); // 🔥 cập nhật số ký tự
    }

    // Xóa sau khi dùng
    localStorage.removeItem("uploaded_text");

});