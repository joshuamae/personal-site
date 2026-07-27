const root = document.documentElement;
const themeToggle = document.getElementById("theme-toggle");
const modeLabel = document.getElementById("mode-label");
const colorScheme = window.matchMedia("(prefers-color-scheme: dark)");

function getSavedTheme() {
  try {
    return localStorage.getItem("theme");
  } catch {
    return null;
  }
}

function saveTheme(theme) {
  try {
    localStorage.setItem("theme", theme);
  } catch {
    // Theme switching still works when storage is unavailable.
  }
}

function applyTheme(theme, persist = false) {
  const isDark = theme === "dark";

  root.dataset.theme = theme;
  themeToggle.setAttribute("aria-pressed", String(isDark));
  modeLabel.textContent = `Switch to ${isDark ? "light" : "dark"} mode`;

  if (persist) {
    saveTheme(theme);
  }
}

applyTheme(root.dataset.theme);

themeToggle.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(nextTheme, true);
});

colorScheme.addEventListener("change", ({ matches }) => {
  if (!getSavedTheme()) {
    applyTheme(matches ? "dark" : "light");
  }
});
