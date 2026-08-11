/**
 * Hero — Dissect on Scroll
 * Drives a single --hd-progress CSS custom property (0 → 1) per instance based
 * on scroll position through the section's tall track. All interpolation
 * happens in CSS (transform/opacity only); this file just measures and writes
 * one variable per animation frame, and only while the section is on screen.
 */
(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  var mobileQuery = window.matchMedia('(max-width: 749px)');

  document.querySelectorAll('[data-hero-dissect]').forEach(function (section) {
    var track = section.querySelector('.hero-dissect__track');
    if (!track) return;

    var ticking = false;
    var active = false;

    function setMobileFactor() {
      section.style.setProperty('--hd-mobile-factor', mobileQuery.matches ? '0.55' : '1');
    }

    function update() {
      ticking = false;
      var rect = track.getBoundingClientRect();
      var viewportH = window.innerHeight;
      var total = rect.height - viewportH;
      var progress = total > 0 ? (0 - rect.top) / total : 0;
      progress = Math.max(0, Math.min(1, progress));
      section.style.setProperty('--hd-progress', progress.toFixed(4));
    }

    function requestUpdate() {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(update);
      }
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          active = entry.isIntersecting;
          if (active) {
            window.addEventListener('scroll', requestUpdate, { passive: true });
            window.addEventListener('resize', requestUpdate);
            requestUpdate();
          } else {
            window.removeEventListener('scroll', requestUpdate);
            window.removeEventListener('resize', requestUpdate);
          }
        });
      },
      { threshold: 0 }
    );

    setMobileFactor();
    mobileQuery.addEventListener('change', function () {
      setMobileFactor();
      requestUpdate();
    });

    observer.observe(track);
  });
})();
