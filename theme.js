// Переключатель тёмной/светлой темы — тумблер в шапке. Запоминает выбор.
(function () {
  var saved = localStorage.getItem("theme");
  // По умолчанию — тёмная. Если выбора ещё не было — уважаем системную.
  if (!saved && window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: light)").matches) {
    saved = "light";
  }
  if (saved === "light") {
    document.documentElement.setAttribute("data-theme", "light");
  }

  function isLight() {
    return document.documentElement.getAttribute("data-theme") === "light";
  }

  function makeSwitch() {
    var sw = document.createElement("button");
    sw.className = "theme-switch";
    sw.type = "button";
    sw.setAttribute("role", "switch");
    sw.setAttribute("aria-label", "Сменить тему");
    sw.innerHTML =
      '<span class="icons"><span>🌙</span><span>☀️</span></span>' +
      '<span class="thumb"></span>';

    function refresh() {
      var light = isLight();
      sw.setAttribute("aria-checked", light ? "true" : "false");
      sw.title = light ? "Включить тёмную тему" : "Включить светлую тему";
    }

    sw.addEventListener("click", function () {
      if (isLight()) {
        document.documentElement.removeAttribute("data-theme");
        localStorage.setItem("theme", "dark");
      } else {
        document.documentElement.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
      }
      refresh();
    });
    refresh();

    // В шапку, если она есть; иначе — плавающим в углу.
    var bar = document.querySelector(".topbar");
    if (bar) {
      bar.appendChild(sw);
    } else {
      sw.classList.add("floating");
      document.body.appendChild(sw);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", makeSwitch);
  } else {
    makeSwitch();
  }
})();
