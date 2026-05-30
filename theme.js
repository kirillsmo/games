// Переключатель тёмной/светлой темы. Запоминает выбор в localStorage.
(function () {
  var saved = localStorage.getItem("theme");
  // По умолчанию — тёмная тема (как у игры). Уважаем системную, если не выбрано.
  if (!saved && window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: light)").matches) {
    saved = "light";
  }
  if (saved === "light") {
    document.documentElement.setAttribute("data-theme", "light");
  }

  function makeButton() {
    var btn = document.createElement("button");
    btn.className = "theme-toggle";
    btn.type = "button";
    btn.setAttribute("aria-label", "Сменить тему");
    function refresh() {
      var light = document.documentElement.getAttribute("data-theme") === "light";
      btn.textContent = light ? "🌙" : "☀️";
      btn.title = light ? "Включить тёмную тему" : "Включить светлую тему";
    }
    btn.addEventListener("click", function () {
      var light = document.documentElement.getAttribute("data-theme") === "light";
      if (light) {
        document.documentElement.removeAttribute("data-theme");
        localStorage.setItem("theme", "dark");
      } else {
        document.documentElement.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
      }
      refresh();
    });
    refresh();
    document.body.appendChild(btn);
  }

  if (document.body) {
    makeButton();
  } else {
    document.addEventListener("DOMContentLoaded", makeButton);
  }
})();
