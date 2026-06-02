/* ============================================================================
   Игры на Python — site shell (final). Drop-in replacement for theme.js.
   On every page it: (1) injects the left sidebar (whole-site map, active state),
   (2) wraps content into the docs grid, (3) builds a right "На этой странице" TOC
   from <h2>, (4) wires the theme toggle and code "Копировать" buttons.
   No per-page markup changes required.
   ============================================================================ */
(function () {
  "use strict";

  /* ---------- site map ---------- */
  var GAMES = [
    { slug: "snake",    label: "Змейка",      em: "🐍", lessons: ["Окно","Квадрат","Змейка-список","Движение","Стрелки","Еда и рост","Игра окончена"] },
    { slug: "catch",    label: "Ловкий кот",  em: "🐱", lessons: ["Кот-корзинка","Яблоко падает","Ловим!","Жизни","Картинки","Звуки"] },
    { slug: "arkanoid", label: "Арканоид",    em: "🧱", lessons: ["Ракетка","Мяч и стены","Отскок от ракетки","Кирпичи","Жизни и победа"] },
    { slug: "space",    label: "Космос",      em: "🚀", lessons: ["Корабль","Выстрел","Враги","Попадания","Жизни и конец"] }
  ];
  var ROBOTS = [
    { slug: "basics", label: "Основы электроники", em: "⚡", lessons: ["Электричество","Светодиод и резистор","Кнопка","Транзистор","Мотор и H-мост","Мостик к Arduino"] },
    { slug: "mearm", label: "Робот MeArm",  em: "🤖", lessons: ["Покупки и тело","Сервопривод","Основание","Плечо и локоть","Захват","Подключение","Первый скетч","pygame ↔ Arduino","Все суставы","Пульт и запись","Проект"] },
    { slug: "car",   label: "Робомашинка", em: "🚗", lessons: ["Знакомство","Сборка шасси","Мозг и провода","Команды моторам","Bluetooth","Глаза машины","Первый заезд","Кокпит","Радар","Автопилот","Миссия","Камера (бонус)"] }
  ];

  /* ---------- where am I (relative to site root) ---------- */
  function locate() {
    var parts = location.pathname.split("/").filter(Boolean);
    var file = parts.length ? parts[parts.length - 1] : "index.html";
    if (file === "" ) file = "index.html";
    var gi = parts.indexOf("games");
    var ri = parts.indexOf("robot");
    var rootIdx, cur = { type: "home" };
    if (gi !== -1) {
      rootIdx = gi;
      cur = { type: "game", slug: parts[gi + 1], file: parts[gi + 2] || "index.html" };
    } else if (ri !== -1) {
      rootIdx = ri;
      if (parts.length - 1 === ri + 1) cur = { type: "robohub" };
      else cur = { type: "robot", slug: parts[ri + 1], file: parts[ri + 2] || "index.html" };
    } else {
      rootIdx = parts.length - 1; // root file (index.html / start.html / progress.html)
      var t = file === "start.html" ? "start"
            : file === "progress.html" ? "progress" : "home";
      cur = { type: t };
    }
    var depthBelowRoot = (parts.length - 1) - rootIdx;
    var prefix = new Array(depthBelowRoot + 1).join("../");
    return { cur: cur, prefix: prefix };
  }

  function lessonNum(file) {
    var m = /urok(\d+)\.html/.exec(file || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  /* ---------- build sidebar ---------- */
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  // which section's course list to show: only one section at a time, never both
  function sectionOf(cur) {
    if (cur.type === "robot" || cur.type === "robohub") return "robot";
    if (cur.type === "game") return "games";
    return "neutral"; // home / start / progress → no course list, just "Начало"
  }

  function buildSidebar(loc) {
    var cur = loc.cur, P = loc.prefix;
    var section = sectionOf(cur);

    // neutral pages (home / start / progress) have no section list → no sidebar
    if (section === "neutral") return null;

    var aside = el("aside", "sb");

    if (section === "games") {
      var g1 = el("div", "grp");
      g1.appendChild(el("div", "grp-h", "Игры"));
      GAMES.forEach(function (c) {
        var active = cur.type === "game" && cur.slug === c.slug;
        g1.appendChild(linkRow(P + "games/" + c.slug + "/index.html", c.label, { ct: c.lessons.length }, active));
        if (active) g1.appendChild(subList(P + "games/" + c.slug + "/", c.lessons, lessonNum(cur.file)));
      });
      aside.appendChild(g1);
    } else if (section === "robot") {
      var g2 = el("div", "grp");
      g2.appendChild(el("div", "grp-h", "Робототехника"));
      g2.appendChild(linkRow(P + "robot/index.html", "Все роботы", null, cur.type === "robohub"));
      ROBOTS.forEach(function (c) {
        var active = cur.type === "robot" && cur.slug === c.slug;
        g2.appendChild(linkRow(P + "robot/" + c.slug + "/index.html", c.label, { ct: c.lessons.length }, active));
        if (active) g2.appendChild(subList(P + "robot/" + c.slug + "/", c.lessons, lessonNum(cur.file)));
      });
      aside.appendChild(g2);
    }

    return aside;
  }

  function linkRow(href, label, opts, active) {
    var a = el("a", "lnk" + (active ? " active" : ""));
    a.href = href;
    var inner = "";
    if (opts && opts.em) inner += '<span class="em">' + opts.em + "</span>";
    inner += '<span class="tx">' + label + "</span>";
    if (opts && opts.ct) inner += '<span class="ct">' + opts.ct + "</span>";
    a.innerHTML = inner;
    return a;
  }

  function subList(base, lessons, activeNum) {
    var wrap = el("div", "sub");
    lessons.forEach(function (name, i) {
      var n = i + 1;
      var a = el("a", n === activeNum ? "active" : "");
      a.href = base + "urok" + n + ".html";
      a.innerHTML = '<span class="n">' + n + '</span><span class="tx">' + name + "</span>";
      wrap.appendChild(a);
    });
    return wrap;
  }

  /* ---------- strip decorative emoji (keeps arrows/checks) ---------- */
  var EMOJI = /([\u{1F000}-\u{1FAFF}\u{1F1E6}-\u{1F1FF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{2300}-\u{23FF}\u{2190}-\u{21FF}]\uFE0F?|\uFE0F|\u20E3|\u200D)/gu;
  // keep simple navigation arrows even though some live in the ranges above
  var KEEP = { "\u2192": 1, "\u2190": 1, "\u2191": 1, "\u2193": 1, "\u21BA": 1, "\u2713": 1, "\u2714": 1 };
  function stripEmoji(root) {
    if (!root) return;
    var skip = { PRE: 1, CODE: 1, SCRIPT: 1, STYLE: 1, TEXTAREA: 1 };
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode;
        while (p && p !== root) { if (skip[p.tagName]) return NodeFilter.FILTER_REJECT; p = p.parentNode; }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var nodes = [], n;
    while (n = walker.nextNode()) nodes.push(n);
    nodes.forEach(function (t) {
      var orig = t.nodeValue;
      var v = orig.replace(EMOJI, function (m) { return KEEP[m] ? m : ""; });
      if (v !== orig) {
        v = v.replace(/[ \t]{2,}/g, " ").replace(/^[ \t]+/, "");
        t.nodeValue = v;
      }
    });
  }

  /* ---------- TOC from h2 ---------- */
  function slug(s, i) {
    return "sec-" + i + "-" + s.toLowerCase().replace(/[^a-zа-я0-9]+/gi, "-").replace(/(^-|-$)/g, "").slice(0, 24);
  }
  function cleanLabel(s) {
    return s.replace(/^[\s\p{Emoji_Presentation}\p{Extended_Pictographic}\u{1F000}-\u{1FAFF}\u2600-\u27BF\uFE0F]+/u, "").trim() || s.trim();
  }
  function buildToc(col) {
    var hs = col.querySelectorAll("h2");
    if (hs.length < 3) return null;
    var nav = el("nav", "toc2");
    nav.appendChild(el("div", "h", "На этой странице"));
    hs.forEach(function (h, i) {
      if (!h.id) h.id = slug(h.textContent || "h", i);
      var a = el("a", "");
      a.href = "#" + h.id;
      a.textContent = cleanLabel(h.textContent || "");
      nav.appendChild(a);
    });
    return nav;
  }

  /* ---------- theme toggle ---------- */
  function initTheme() {
    // Bright is a light-first brand: default to light; dark is opt-in and remembered.
    if (localStorage.getItem("theme") === "dark") document.documentElement.setAttribute("data-theme", "dark");
  }
  function isDark() { return document.documentElement.getAttribute("data-theme") === "dark"; }
  function makeSwitch(topbar) {
    var sw = el("button", "theme-switch");
    sw.type = "button";
    sw.setAttribute("aria-label", "Сменить тему");
    sw.innerHTML = '<span class="icons"><span>☀️</span><span>🌙</span></span><span class="thumb"></span>';
    sw.addEventListener("click", function () {
      if (isDark()) { document.documentElement.removeAttribute("data-theme"); localStorage.setItem("theme", "light"); }
      else { document.documentElement.setAttribute("data-theme", "dark"); localStorage.setItem("theme", "dark"); }
    });
    if (topbar) topbar.appendChild(sw); else { sw.classList.add("floating"); document.body.appendChild(sw); }
  }

  /* ---------- copy buttons ---------- */
  function addCopyButtons(root) {
    var blocks = root.querySelectorAll("pre");
    for (var i = 0; i < blocks.length; i++) {
      (function (pre) {
        var text = pre.innerText;
        var btn = el("button", "copy-btn", "Копировать");
        btn.type = "button";
        btn.addEventListener("click", function () {
          var done = function () {
            btn.textContent = "Скопировано ✓"; btn.classList.add("copied");
            setTimeout(function () { btn.textContent = "Копировать"; btn.classList.remove("copied"); }, 1400);
          };
          if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, done);
          else done();
        });
        pre.appendChild(btn);
      })(blocks[i]);
    }
  }

  /* ---------- scroll spy ---------- */
  function spy(nav, col) {
    if (!nav) return;
    var links = {}, items = nav.querySelectorAll("a");
    items.forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var obs = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          items.forEach(function (a) { a.classList.remove("on"); });
          if (links[e.target.id]) links[e.target.id].classList.add("on");
        }
      });
    }, { rootMargin: "-8% 0px -78% 0px" });
    col.querySelectorAll("h2[id]").forEach(function (h) { obs.observe(h); });
  }

  /* ---------- assemble ---------- */
  function init() {
    initTheme();
    // Nudge the Cyrillic font subsets to load immediately (Google Fonts loads them
    // lazily; without this the first paint can fall back before Onest arrives).
    if (document.fonts && document.fonts.load) {
      try {
        document.fonts.load("700 1em Onest", "Ёяшщ");
        document.fonts.load("800 1em Onest", "Ёяшщ");
        document.fonts.load("600 1em Manrope", "Ёяшщ");
      } catch (e) {}
    }
    var body = document.body;
    var topbar = document.querySelector(".topbar");
    var loc = locate();

    var app = el("div", "app");
    var main = el("main", "doc");
    var col = el("div", "doc-col");

    Array.prototype.slice.call(body.children).forEach(function (ch) {
      if (ch === topbar) return;
      if (ch.tagName === "SCRIPT") return;
      col.appendChild(ch);
    });
    main.appendChild(col);

    stripEmoji(col);
    stripEmoji(topbar);

    var aside = buildSidebar(loc);
    var toc = buildToc(col);

    if (aside) app.appendChild(aside); else app.classList.add("no-sb");
    app.appendChild(main);
    if (toc) app.appendChild(toc); else app.classList.add("no-toc");
    body.appendChild(app);

    if (topbar) makeSwitch(topbar); else makeSwitch(null);
    addCopyButtons(col);
    spy(toc, col);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
