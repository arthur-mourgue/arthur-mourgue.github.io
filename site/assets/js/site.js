// Tactile background: the page-wide cross grid lights up in blue around the
// cursor (see body::before in style.css). Tracking runs everywhere, including
// over the media; the paper backing keeps the crosses from showing through.
(function () {
  if (!matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  var root = document.documentElement;

  document.addEventListener("mousemove", function (e) {
    // pageX/pageY (document-relative), not clientX/clientY (viewport-relative):
    // body::before is position: absolute and scrolls with the page.
    root.style.setProperty("--mx", e.pageX + "px");
    root.style.setProperty("--my", e.pageY + "px");
  });
})();

// Click ripple: every click sends a wave through the cross grid — the existing
// crosses turn blue as the circle grows past them. The layer is a full-page div
// (see .ripple in style.css); we only hand it the click point in page coordinates
// and drop it when the animation ends. Any pointer type, skipped under
// prefers-reduced-motion.
(function () {
  var reduced = matchMedia("(prefers-reduced-motion: reduce)");

  document.addEventListener("click", function (e) {
    if (reduced.matches) return;

    var ripple = document.createElement("div");
    ripple.className = "ripple";
    // pageX/pageY (document-relative): the layer is position: absolute in body
    // and scrolls with the page, so the circle must use page coordinates too.
    ripple.style.setProperty("--rx", e.pageX + "px");
    ripple.style.setProperty("--ry", e.pageY + "px");

    ripple.addEventListener("animationend", function () {
      ripple.remove();
    });
    document.body.appendChild(ripple);
  });
})();

// Scroll reveal: sections, cards and list rows fade up once as they enter the
// viewport. The .js class is set in the document head, so the initial hidden
// state only applies when JavaScript is available. Skipped under
// prefers-reduced-motion.
(function () {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!("IntersectionObserver" in window)) return;

  var targets = document.querySelectorAll(".reveal");
  if (!targets.length) return;

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

  targets.forEach(function (el) { observer.observe(el); });
})();

// Ambient touches: every few seconds a soft blue patch lights up the cross
// grid at a random point in the viewport, then fades. Skipped under
// prefers-reduced-motion.
(function () {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  function touch() {
    var el = document.createElement("div");
    el.className = "touch";
    el.style.setProperty("--tx", (window.scrollX + Math.random() * window.innerWidth) + "px");
    el.style.setProperty("--ty", (window.scrollY + Math.random() * window.innerHeight) + "px");
    el.addEventListener("animationend", function () { el.remove(); });
    document.body.appendChild(el);
    setTimeout(touch, 5000 + Math.random() * 7000);
  }

  setTimeout(touch, 2500 + Math.random() * 3000);
})();
