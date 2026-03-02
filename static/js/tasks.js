// KHẢO SÁT GIẢ LẬP
function completeSurvey() {

    const answer = prompt("Bạn đánh giá dịch vụ từ 1 đến 5 sao?");

    if (answer && answer >= 1 && answer <= 5) {
        alert("Cảm ơn bạn đã đánh giá " + answer + " ⭐");

        document.getElementById("surveyCheckbox").checked = true;
        document.getElementById("surveyTask").classList.add("done");
    } else {
        alert("Vui lòng nhập số từ 1 đến 5");
    }
}


// MỜI BẠN BÈ GIẢ LẬP
function inviteFriend() {

    const email = prompt("Nhập email bạn bè để gửi lời mời:");

    if (email && email.includes("@")) {

        alert("Đã gửi lời mời tới: " + email);

        document.getElementById("inviteCheckbox").checked = true;
        document.getElementById("inviteTask").classList.add("done");

    } else {
        alert("Email không hợp lệ!");
    }
}


// NHẬN THƯỞNG
function claimReward() {

    const surveyDone = document.getElementById("surveyCheckbox").checked;
    const inviteDone = document.getElementById("inviteCheckbox").checked;

    if (surveyDone && inviteDone) {
        alert("🎉 Bạn đã nhận thưởng thành công!");
    } else {
        alert("Bạn chưa hoàn thành đủ nhiệm vụ!");
    }
}