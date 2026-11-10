/* ============================================================
   MENSCH DENK AN DICH® – „Das Spiel spricht selbst“
   Steuert die Twiggy-Animation. Kein Framework nötig.
   Zeiten (Millisekunden) lassen sich per data-Attribut ändern:
   data-intro, data-slot, data-outro, data-loop="true"
   Seitenverhältnis: data-ratio="1/1" (oder 4/3, 16/9 …)
   ============================================================ */
(function () {
  "use strict";

  function TwiggyShow(root) {
    this.root = root;
    this.items = Array.prototype.slice.call(root.querySelectorAll(".tw-list li"));
    this.dots = root.querySelector(".tw-dots");
    this.bubble = root.querySelector(".tw-bubble");
    this.bubbleText = root.querySelector(".tw-bubble-text");
    this.bubbleNum = root.querySelector(".tw-num");
    this.intro = +root.dataset.intro || 3600;
    this.slot = +root.dataset.slot || 4400;
    this.outroHold = +root.dataset.outro || 8000;
    this.loop = root.dataset.loop === "true";
    this.timers = [];
    this.started = false;
    this.setRatio(root.dataset.ratio);

    this.dots.innerHTML = this.items.map(function () { return "<span></span>"; }).join("");
    this.dotEls = Array.prototype.slice.call(this.dots.children);

    var self = this;
    var replay = root.querySelector(".tw-replay");
    if (replay) replay.addEventListener("click", function () { self.start(); });

    // Ohne Bewegung: alles sofort zeigen, keine Abfolge
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      this.items.forEach(function (li) { li.classList.add("shown"); });
      this.dotEls.forEach(function (d) { d.classList.add("on"); });
      return;
    }
    root.classList.add("js-ready");

    // Start, sobald die Animation sichtbar wird
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting && !self.started) { self.start(); io.disconnect(); }
      }, { threshold: 0.35 });
      io.observe(root);
    } else {
      this.start();
    }
  }

  /* Seitenverhältnis setzen, z. B. "1/1", "4:3", "16/9"; leer = automatisch */
  TwiggyShow.prototype.setRatio = function (r) {
    r = (r || "").replace(":", "/").trim();
    this.ratio = (r && r !== "auto") ? r : "";
    if (this.ratio) this.root.style.setProperty("--tw-ratio", this.ratio);
    else this.root.style.removeProperty("--tw-ratio");
    this.fit();
    if (!this.ro && "ResizeObserver" in window) {
      var self = this, w = 0;
      this.ro = new ResizeObserver(function (e) {
        var nw = Math.round(e[0].contentRect.width);
        if (nw !== w) { w = nw; self.fit(); }
      });
      this.ro.observe(this.root);
    }
  };

  /* Passt der Text bei festem Seitenverhältnis nicht hinein (sehr flache
     Formate auf schmalen Bildschirmen), richtet sich die Höhe nach dem Inhalt. */
  TwiggyShow.prototype.fit = function () {
    var r = this.root, panel = r.querySelector(".tw-panel");
    if (!this.ratio) { r.classList.remove("has-ratio"); return; }
    r.classList.add("has-ratio");
    if (panel.scrollHeight > panel.clientHeight + 2) r.classList.remove("has-ratio");
  };

  TwiggyShow.prototype.at = function (ms, fn) {
    this.timers.push(setTimeout(fn.bind(this), ms));
  };

  TwiggyShow.prototype.reset = function () {
    this.timers.forEach(clearTimeout);
    this.timers = [];
    var r = this.root;
    r.classList.remove("is-running", "is-outro", "is-talking");
    this.items.forEach(function (li) { li.classList.remove("shown"); });
    this.dotEls.forEach(function (d) { d.classList.remove("on"); });
    this.bubble.classList.remove("is-in", "is-out");
  };

  TwiggyShow.prototype.start = function () {
    this.reset();
    this.started = true;
    var n = this.items.length, slot = this.slot;

    this.at(this.intro - 400, function () { this.root.classList.add("is-running"); });

    for (var i = 0; i < n; i++) {
      (function (k) {
        var t0 = this.intro + k * slot;
        // Sprechblase erscheint, Twiggy spricht
        this.at(t0, function () {
          var li = this.items[k];
          this.bubbleText.textContent = li.querySelector(".tw-t").textContent;
          this.bubbleNum.textContent = k + 1;
          this.bubble.classList.remove("is-out");
          void this.bubble.offsetWidth;            // Animation neu starten
          this.bubble.classList.add("is-in");
          this.dotEls[k].classList.add("on");
        });
        this.at(t0 + 350, function () { this.root.classList.add("is-talking"); });
        this.at(t0 + slot * 0.72, function () { this.root.classList.remove("is-talking"); });
        // Blase verschwindet, Satz wandert lesbar in die Liste
        this.at(t0 + slot - 450, function () {
          this.bubble.classList.remove("is-in");
          this.bubble.classList.add("is-out");
          this.items[k].classList.add("shown");
        });
      }).call(this, i);
    }

    var end = this.intro + n * slot;
    this.at(end + 300, function () { this.root.classList.add("is-outro"); });
    if (this.loop) this.at(end + 300 + this.outroHold, function () { this.start(); });
  };

  function init() {
    var nodes = document.querySelectorAll(".mdad-twiggy");
    for (var i = 0; i < nodes.length; i++) nodes[i].twiggy = new TwiggyShow(nodes[i]);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
