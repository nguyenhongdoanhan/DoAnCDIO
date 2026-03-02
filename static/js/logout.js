function logoutUser() {
  // ❌ Xóa JWT
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");

  // 👉 Gọi logout Django
  window.location.href = "/logout/";
}
