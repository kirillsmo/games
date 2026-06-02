// quiz.js — самопроверка после уроков для GitHub Pages (без сервера).
//
// КАК ЭТО УСТРОЕНО (и почему ответ нельзя угадать или подсмотреть):
//  • Ребёнок вводит ответ СВОБОДНЫМ ТЕКСТОМ — нет кнопок-вариантов, перебрать нечего.
//  • В странице лежит НЕ ответ, а его «посоленный» SHA-256-хэш, прогнанный много раз.
//    Из хэша ответ не восстановить, а перебор словами/числами скриптом — дорог.
//  • Правильный ответ нужно НАЙТИ В УРОКЕ — на это и расчёт: подумать → посмотреть → ответить.
//  • Объяснение («почему так») показывается ТОЛЬКО после верного ответа.
//
// Разметка урока:
//   <div class="quiz" data-iter="2000">
//     <h2>🧠 Проверь себя</h2>
//     <div class="quiz-q" data-id="basics2-led" data-hash="ХЭШ1 ХЭШ2">
//       <p class="quiz-prompt">Вопрос…</p>
//       <p class="quiz-hint">Подсказка: где смотреть в уроке.</p>
//       <div class="quiz-explain">Появится после верного ответа.</div>
//     </div>
//   </div>
// data-hash — один или несколько (через пробел) допустимых хэшей ответа.
// Хэши считаются скриптом tools/quizhash.py — он использует ТУ ЖЕ нормализацию и число повторов.

(function () {
  "use strict";

  // ---- SHA-256 (компактная реализация, работает офлайн и на file://) ----
  var K = [
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
  ];

  function sha256bytes(bytes) {
    function rotr(x, n) { return (x >>> n) | (x << (32 - n)); }
    var l = bytes.length;
    var k = (56 - (l + 1) % 64 + 64) % 64;
    var total = l + 1 + k + 8;
    var m = new Uint8Array(total);
    m.set(bytes, 0);
    m[l] = 0x80;
    var bitLen = l * 8;                       // входы короткие — помещаются в 32 бита
    m[total - 4] = (bitLen >>> 24) & 0xff;
    m[total - 3] = (bitLen >>> 16) & 0xff;
    m[total - 2] = (bitLen >>> 8) & 0xff;
    m[total - 1] = bitLen & 0xff;

    var H = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    var w = new Array(64);

    for (var off = 0; off < total; off += 64) {
      for (var i = 0; i < 16; i++) {
        w[i] = (m[off + i*4] << 24) | (m[off + i*4 + 1] << 16) | (m[off + i*4 + 2] << 8) | (m[off + i*4 + 3]);
      }
      for (i = 16; i < 64; i++) {
        var s0 = rotr(w[i-15],7) ^ rotr(w[i-15],18) ^ (w[i-15] >>> 3);
        var s1 = rotr(w[i-2],17) ^ rotr(w[i-2],19) ^ (w[i-2] >>> 10);
        w[i] = (w[i-16] + s0 + w[i-7] + s1) | 0;
      }
      var a=H[0],b=H[1],c=H[2],d=H[3],e=H[4],f=H[5],g=H[6],h=H[7];
      for (i = 0; i < 64; i++) {
        var S1 = rotr(e,6) ^ rotr(e,11) ^ rotr(e,25);
        var ch = (e & f) ^ (~e & g);
        var t1 = (h + S1 + ch + K[i] + w[i]) | 0;
        var S0 = rotr(a,2) ^ rotr(a,13) ^ rotr(a,22);
        var maj = (a & b) ^ (a & c) ^ (b & c);
        var t2 = (S0 + maj) | 0;
        h=g; g=f; f=e; e=(d + t1)|0; d=c; c=b; b=a; a=(t1 + t2)|0;
      }
      H[0]=(H[0]+a)|0; H[1]=(H[1]+b)|0; H[2]=(H[2]+c)|0; H[3]=(H[3]+d)|0;
      H[4]=(H[4]+e)|0; H[5]=(H[5]+f)|0; H[6]=(H[6]+g)|0; H[7]=(H[7]+h)|0;
    }
    var hex = "";
    for (i = 0; i < 8; i++) hex += ("00000000" + (H[i] >>> 0).toString(16)).slice(-8);
    return hex;
  }

  var enc = (typeof TextEncoder !== "undefined") ? new TextEncoder() : null;
  function utf8(str) {
    if (enc) return enc.encode(str);
    str = unescape(encodeURIComponent(str));        // запасной путь
    var arr = new Uint8Array(str.length);
    for (var i = 0; i < str.length; i++) arr[i] = str.charCodeAt(i);
    return arr;
  }
  function sha256hex(str) { return sha256bytes(utf8(str)); }

  // ---- Нормализация ответа (ДОЛЖНА совпадать с tools/quizhash.py) ----
  function normalize(s) {
    s = (s || "").toLowerCase().replace(/ё/g, "е");
    s = s.replace(/,/g, ".");                        // десятичная запятая → точка
    s = s.replace(/[^0-9a-zа-я .\-]/g, " ");         // лишние символы → пробел
    s = s.replace(/\s+/g, " ").trim();
    s = s.replace(/^[.\-]+|[.\-]+$/g, "").trim();    // убрать крайние точки/дефисы
    return s;
  }

  function quizhash(id, answer, iter) {
    var h = sha256hex(id + "|" + normalize(answer));
    for (var i = 1; i < iter; i++) h = sha256hex(h);
    return h;
  }

  // ---- Логика виджета ----
  function setup(q, iter) {
    var id = q.getAttribute("data-id");
    var hashes = (q.getAttribute("data-hash") || "").trim().split(/\s+/);
    var look = q.getAttribute("data-look") || "Загляни в урок выше — там есть ответ.";

    var row = document.createElement("div");
    row.className = "quiz-row";
    var input = document.createElement("input");
    input.className = "quiz-input";
    input.type = "text";
    input.autocomplete = "off";
    input.spellcheck = false;
    input.placeholder = "твой ответ…";
    var btn = document.createElement("button");
    btn.className = "quiz-check";
    btn.type = "button";
    btn.textContent = "Проверить";
    row.appendChild(input);
    row.appendChild(btn);

    var fb = document.createElement("p");
    fb.className = "quiz-feedback";

    var explain = q.querySelector(".quiz-explain");
    var hint = q.querySelector(".quiz-hint");
    if (explain) q.insertBefore(row, explain); else q.appendChild(row);
    q.insertBefore(fb, row.nextSibling);

    var attempts = 0;
    var key = "quiz:" + id;

    function solved() {
      q.classList.add("solved");
      input.value = "";
      input.placeholder = "✓ решено";
      input.disabled = true;
      btn.disabled = true;
      fb.textContent = "✅ Верно!";
      fb.className = "quiz-feedback ok";
      try { localStorage.setItem(key, "1"); } catch (e) {}
    }

    if (localStorage.getItem(key) === "1") { solved(); }

    function check() {
      if (q.classList.contains("solved")) return;
      var val = input.value;
      if (!normalize(val)) { input.focus(); return; }
      var h = quizhash(id, val, iter);
      if (hashes.indexOf(h) !== -1) {
        solved();
      } else {
        attempts++;
        q.classList.remove("shake");
        void q.offsetWidth;                          // перезапустить анимацию
        q.classList.add("shake");
        fb.className = "quiz-feedback no";
        fb.textContent = attempts >= 3
          ? "✗ Пока не то. " + look
          : "✗ Не совсем — подумай ещё и проверь в уроке.";
      }
    }

    btn.addEventListener("click", check);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); check(); }
    });
  }

  function init() {
    var quizzes = document.querySelectorAll(".quiz");
    for (var i = 0; i < quizzes.length; i++) {
      var iter = parseInt(quizzes[i].getAttribute("data-iter"), 10) || 2000;
      var qs = quizzes[i].querySelectorAll(".quiz-q");
      for (var j = 0; j < qs.length; j++) setup(qs[j], iter);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
