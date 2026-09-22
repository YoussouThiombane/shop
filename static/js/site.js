document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-disable-on-submit]").forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.textContent = "Envoi…";
      }
    });
  });

  document.querySelectorAll("[data-copy-url]").forEach((button) => {
    button.addEventListener("click", async () => {
      const original = button.textContent;
      try {
        await navigator.clipboard.writeText(button.dataset.copyUrl);
        button.textContent = "Lien copié";
      } catch (error) {
        const input = button.parentElement.querySelector("input");
        input.select();
        document.execCommand("copy");
        button.textContent = "Lien copié";
      }
      setTimeout(() => { button.textContent = original; }, 1800);
    });
  });

  const sidebar = document.querySelector("#dashboardSidebar");
  const sidebarToggle = document.querySelector("[data-sidebar-toggle]");
  if (sidebar && sidebarToggle) {
    sidebarToggle.addEventListener("click", () => sidebar.classList.toggle("open"));
    document.addEventListener("click", (event) => {
      if (sidebar.classList.contains("open") && !sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) sidebar.classList.remove("open");
    });
  }

  document.querySelectorAll(".thumbnail").forEach((thumbnail) => {
    thumbnail.addEventListener("click", () => {
      document.querySelectorAll(".thumbnail").forEach((item) => item.classList.remove("active"));
      thumbnail.classList.add("active");
    });
  });
});
