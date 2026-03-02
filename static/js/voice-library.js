document.addEventListener("DOMContentLoaded", function () {
console.log("VOICE LIBRARY JS LOADED");
  const buttons = document.querySelectorAll(".preview-btn");

  let audioPlayer = new Audio();   // tạo audio mới hoàn toàn
  let currentButton = null;

  buttons.forEach(btn => {
    btn.addEventListener("click", function () {

      const audioUrl = this.dataset.audio;

      // Nếu đang phát cùng file thì dừng
      if (currentButton === this && !audioPlayer.paused) {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        this.innerText = "Nghe thử";
        currentButton = null;
        return;
      }

      // Reset tất cả nút
      buttons.forEach(b => b.innerText = "Nghe thử");

      // Dừng audio cũ
      audioPlayer.pause();
      audioPlayer.currentTime = 0;

      // Tạo audio mới
      audioPlayer = new Audio(audioUrl);
      currentButton = this;

      audioPlayer.play();
      this.innerText = "Đang phát...";

      // Khi phát xong
      audioPlayer.onended = function () {
        if (currentButton) {
          currentButton.innerText = "Nghe thử";
          currentButton = null;
        }
      };

    });
  });

});