// Tactile background: the page-wide cross grid lights up in blue around the
// cursor (see body::before in style.css). Tracking runs everywhere, including
// over the hand; .hand::before is an opaque paper backing, masked by the
// drawing, that keeps the crosses from showing through its strokes.
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
