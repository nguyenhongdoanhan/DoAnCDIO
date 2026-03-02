function login(event) {
  // ⛔ chặn submit mặc định
  event.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!email || !password) {
    alert("Vui lòng nhập email và mật khẩu");
    return;
  }

  fetch("/api/auth/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  credentials: "include", // 🔥 THÊM DÒNG NÀY
  body: JSON.stringify({
    mode: "login",
    email: email,
    password: password
  })
})

    .then(res => res.json())
    .then(data => {
      if (data.access_token) {
        // ✅ Lưu token
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        // ✅ Chuyển sang dashboard
        window.location.href = "/dashboard/";
      } else {
        alert(data.message || "Đăng nhập thất bại");
      }
    })
    .catch(err => {
      console.error(err);
      alert("Lỗi kết nối server");
    });
}
