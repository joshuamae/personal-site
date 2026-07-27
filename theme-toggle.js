const root = document.documentElement;
const themeToggle = document.getElementById("theme-toggle");
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
  themeToggle.setAttribute(
    "aria-label",
    `Switch to ${isDark ? "light" : "dark"} mode`,
  );

  if (persist) {
    saveTheme(theme);
  }
}

const activeTheme =
  root.dataset.theme || getSavedTheme() || (colorScheme.matches ? "dark" : "light");

applyTheme(activeTheme);

themeToggle.addEventListener("click", () => {
  applyTheme(root.dataset.theme === "dark" ? "light" : "dark", true);
});

function handleSystemThemeChange({ matches }) {
  if (!getSavedTheme()) {
    applyTheme(matches ? "dark" : "light");
  }
}

if (typeof colorScheme.addEventListener === "function") {
  colorScheme.addEventListener("change", handleSystemThemeChange);
} else {
  colorScheme.addListener(handleSystemThemeChange);
}
