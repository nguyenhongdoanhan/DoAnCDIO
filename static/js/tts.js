function convertTextToSpeech() {

    const text = document.getElementById("textInput").value;
    const rateValue = document.getElementById("rateRange").value;
    const pitchValue = document.getElementById("pitchRange").value;

    if (!text.trim()) {
        alert("Vui lòng nhập nội dung");
        return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
        alert("Bạn chưa đăng nhập");
        return;
    }

    fetch("/api/tts/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            text: text,
            rate: rateValue,
            pitch: pitchValue
        })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Unauthorized hoặc token hết hạn");
        }
        return res.json();
    })
    .then(data => {
        if (data.audio_url) {
            const audioPlayer = document.getElementById("audioPlayer");
            audioPlayer.src = data.audio_url;
            audioPlayer.style.display = "block";
            audioPlayer.play();
        }
    })
    .catch(err => {
        console.error(err);
        alert("Lỗi server hoặc token hết hạn");
    });
}
document.addEventListener("DOMContentLoaded", function () {

    const savedText = localStorage.getItem("uploaded_text");

    if (savedText) {
        const textarea = document.getElementById("textInput");

        if (textarea) {
            textarea.value = savedText;
        }

        localStorage.removeItem("uploaded_text");
    }

});