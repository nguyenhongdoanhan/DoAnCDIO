async function load(id, file, callback) {
  try {
    const res = await fetch(file);
    if (!res.ok) throw new Error(`Cannot load ${file}`);

    const html = await res.text();
    document.getElementById(id).innerHTML = html;

    if (callback) callback();
  } catch (err) {
    console.error(err);
  }
}

/* =========================
   LOAD COMPONENTS
========================= */
load("sidebar", "/static/components/sidebar.html", setActiveSidebar);
load("header", "/static/components/header.html", initUserDropdown);


/* =========================
   SIDEBAR ACTIVE STATE
========================= */
function setActiveSidebar() {

  const currentPath = window.location.pathname;

  document.querySelectorAll(".sidebar a").forEach(link => {
    link.classList.remove("active");

    const linkPath = link.getAttribute("href");

    if (currentPath === linkPath) {
      link.classList.add("active");
    }
  });
}


/* =========================
   USER DROPDOWN
========================= */
function initUserDropdown() {
  const trigger = document.getElementById("userTrigger");
  const dropdown = document.getElementById("userDropdown");

  if (!trigger || !dropdown) return;

  trigger.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("active");
  });

  dropdown.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  document.addEventListener("click", () => {
    dropdown.classList.remove("active");
  });
}