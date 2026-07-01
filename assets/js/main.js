/* =========================================================================
   Samuel's Tree Service — interaction layer
   Robust baseline (no deps) + progressive enhancement (Lenis + GSAP).
   Reveals run through ScrollTrigger when GSAP is present (Lenis-synced),
   and fall back to IntersectionObserver otherwise.
   ========================================================================= */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var root = document.documentElement;
  if (!reduced) root.classList.add("anim");

  /* ---------------- Founding-year-driven values ---------------- */
  var FOUNDED = 2002;
  var yearsInBiz = new Date().getFullYear() - FOUNDED;
  document.querySelectorAll("[data-years]").forEach(function (el) { el.textContent = yearsInBiz; });

  /* ---------------- Open / Closed badge (real hours) ----------------
     Local time. 24h. null = closed. [open, close]. Sat 9–2 per site. */
  var HOURS = { 0: null, 1: [8, 19], 2: [8, 19], 3: [8, 19], 4: [8, 19], 5: [8, 19], 6: [9, 14] };
  function fmt(h) { var ap = h >= 12 ? "PM" : "AM"; var hr = h % 12 || 12; return hr + " " + ap; }
  function renderStatus() {
    var els = document.querySelectorAll("[data-status]");
    if (!els.length) return;
    var now = new Date();
    var today = HOURS[now.getDay()];
    var mins = now.getHours() * 60 + now.getMinutes();
    var open = today && mins >= today[0] * 60 && mins < today[1] * 60;
    els.forEach(function (el) {
      var txt = el.querySelector("[data-status-text]");
      var sub = el.querySelector("[data-status-sub]");
      el.classList.toggle("is-open", !!open);
      el.classList.toggle("is-closed", !open);
      if (txt) txt.textContent = open ? "Open now" : "Closed";
      if (sub) sub.textContent = open ? "· until " + fmt(today[1]) : "· 24/7 emergency line open";
    });
  }
  renderStatus();
  setInterval(renderStatus, 60000);

  /* highlight today's row in any hours table */
  (function () {
    var today = new Date().getDay();
    document.querySelectorAll("[data-hours] tr").forEach(function (tr) {
      if (parseInt(tr.getAttribute("data-day"), 10) === today) tr.classList.add("today");
    });
  })();

  /* ---------------- Sticky header state ---------------- */
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 24); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------------- Mobile nav ---------------- */
  var burger = document.querySelector(".hamburger");
  var drawer = document.querySelector(".mobile-nav");
  function toggleNav(force) {
    var open = typeof force === "boolean" ? force : !drawer.classList.contains("open");
    drawer.classList.toggle("open", open);
    burger.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
  }
  if (burger && drawer) {
    burger.addEventListener("click", function () { toggleNav(); });
    drawer.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { toggleNav(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("open")) toggleNav(false); });
  }

  /* Desktop dropdown: click-toggle in addition to hover */
  document.querySelectorAll(".has-menu").forEach(function (menu) {
    var trigger = menu.querySelector(".nav-link");
    if (!trigger) return;
    trigger.addEventListener("click", function (e) {
      // if this trigger link goes to a real page (not "#"), allow the click through
      // but on touch, toggle open on first tap
      if (window.matchMedia("(hover: none)").matches) {
        if (!menu.classList.contains("open")) { e.preventDefault(); menu.classList.add("open"); }
      }
    });
  });
  document.addEventListener("click", function (e) {
    document.querySelectorAll(".has-menu.open").forEach(function (m) {
      if (!m.contains(e.target)) m.classList.remove("open");
    });
  });

  /* ---------------- Count-up stats (real numbers) ---------------- */
  function countUp(el) {
    if (el.dataset.counted) return;
    el.dataset.counted = "1";
    var target = parseFloat(el.getAttribute("data-count"));
    var dec = (el.getAttribute("data-dec") | 0);
    var dur = 1400, start = performance.now();
    function tick(t) {
      var p = Math.min((t - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = eased * target;
      el.textContent = dec ? val.toFixed(dec) : Math.floor(val).toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = dec ? target.toFixed(dec) : target.toLocaleString();
    }
    requestAnimationFrame(tick);
  }

  /* ---------------- Gallery lightbox ---------------- */
  var gItems = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]"));
  if (gItems.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Photo viewer");
    lb.innerHTML =
      '<button class="lb-close" aria-label="Close">' + icon("x") + "</button>" +
      '<button class="lb-nav lb-prev" aria-label="Previous photo">' + icon("left") + "</button>" +
      '<button class="lb-nav lb-next" aria-label="Next photo">' + icon("right") + "</button>" +
      '<img alt="">' +
      '<div class="lb-cap"></div>';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector("img"), lbCap = lb.querySelector(".lb-cap"), idx = 0;
    function show(i) {
      idx = (i + gItems.length) % gItems.length;
      lbImg.src = gItems[idx].getAttribute("data-lightbox");
      var cap = gItems[idx].getAttribute("data-caption") || "";
      lbImg.alt = cap; lbCap.textContent = cap;
    }
    function open(i) { show(i); lb.classList.add("open"); document.body.style.overflow = "hidden"; }
    function close() { lb.classList.remove("open"); document.body.style.overflow = ""; }
    gItems.forEach(function (it, i) {
      it.addEventListener("click", function () { open(i); });
      it.setAttribute("tabindex", "0"); it.setAttribute("role", "button");
      it.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(i); } });
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
  }

  /* ---------------- Quote form (front-end only) ---------------- */
  document.querySelectorAll("[data-quote-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var success = form.parentNode.querySelector(".form-success");
      form.style.display = "none";
      if (success) success.classList.add("show");
    });
  });

  function icon(name) {
    var p = {
      x: '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
      left: '<polyline points="15 18 9 12 15 6"/>',
      right: '<polyline points="9 18 15 12 9 6"/>'
    }[name];
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + p + "</svg>";
  }

  /* ---------------- Hero choreography ---------------- */
  var hero = document.querySelector(".hero");
  if (hero) requestAnimationFrame(function () { requestAnimationFrame(function () { hero.classList.add("ready"); }); });

  /* =======================================================================
     REVEALS + counters
     ======================================================================= */
  function markIn(el) {
    el.classList.add("is-in");
    if (el.hasAttribute("data-count")) countUp(el);
    el.querySelectorAll && el.querySelectorAll("[data-count]").forEach(countUp);
  }
  var revealEls = Array.prototype.slice.call(document.querySelectorAll(".reveal, .reveal-clip"));
  var standaloneCounters = Array.prototype.slice.call(document.querySelectorAll("[data-count]")).filter(function (el) {
    return !el.closest(".reveal, .reveal-clip");
  });

  if (reduced) {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
    document.querySelectorAll("[data-count]").forEach(function (el) {
      var t = parseFloat(el.getAttribute("data-count")); var d = el.getAttribute("data-dec") | 0;
      el.textContent = d ? t.toFixed(d) : t.toLocaleString();
    });
    return; // no smooth scroll / parallax under reduced motion
  }

  /* ---------------- Smooth scroll (Lenis) ---------------- */
  var lenis = null;
  if (window.Lenis) {
    lenis = new window.Lenis({ duration: 1.05, smoothWheel: true, lerp: 0.095 });
    root.classList.add("lenis");
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href");
        if (id.length > 1) { var t = document.querySelector(id); if (t) { e.preventDefault(); lenis.scrollTo(t, { offset: -90 }); } }
      });
    });
  }

  var hasST = window.gsap && window.ScrollTrigger;
  if (hasST) {
    var gsap = window.gsap;
    gsap.registerPlugin(window.ScrollTrigger);
    var ST = window.ScrollTrigger;

    if (lenis) {
      lenis.on("scroll", ST.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      function raf(time) { requestAnimationFrame(raf); }
    }

    // Reveals via ScrollTrigger.batch — Lenis-synced, reliable.
    ST.batch(revealEls, {
      start: "top 88%",
      once: true,
      onEnter: function (batch) { batch.forEach(markIn); }
    });
    standaloneCounters.forEach(function (el) {
      ST.create({ trigger: el, start: "top 90%", once: true, onEnter: function () { countUp(el); } });
    });

    // Gentle parallax inside the contained hero cards (image has headroom)
    var heroImg = document.querySelector(".hero-card img");
    if (heroImg) gsap.fromTo(heroImg, { yPercent: -6 }, { yPercent: 6, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: 0.5 } });
    var pgImg = document.querySelector(".ph-card img");
    if (pgImg) gsap.fromTo(pgImg, { yPercent: -5 }, { yPercent: 5, ease: "none", scrollTrigger: { trigger: ".page-hero", start: "top top", end: "bottom top", scrub: 0.5 } });

    ST.refresh();
  } else {
    // Drive Lenis without GSAP ticker
    if (lenis) { (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(performance.now()); }
    // Fallback reveals via IntersectionObserver
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) { if (entry.isIntersecting) { markIn(entry.target); io.unobserve(entry.target); } });
      }, { threshold: 0.15, rootMargin: "0px 0px -10% 0px" });
      revealEls.forEach(function (el) { io.observe(el); });
      standaloneCounters.forEach(function (el) { io.observe(el); });
    } else {
      revealEls.forEach(markIn);
      standaloneCounters.forEach(countUp);
    }
  }
})();
