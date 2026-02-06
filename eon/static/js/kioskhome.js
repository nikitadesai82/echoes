(function () {
  const IDLE_TIME = 600 * 1000; // 1 minute
  let idleTimer;

  function isVideoBoxPlaying() {
    const videoBox = document.getElementById("videoBox");
    if (!videoBox) return false;

    if (getComputedStyle(videoBox).display === "none") {
      return false;
    }

    return Array.from(videoBox.querySelectorAll("video"))
      .some(v => !v.paused && !v.ended);
  }

  function kioskReset() {
    try {
      localStorage.clear();
      sessionStorage.clear();

      if ("caches" in window) {
        caches.keys().then(keys =>
          keys.forEach(key => caches.delete(key))
        );
      }
    } catch (e) {}

    if (window.gsap) {
      gsap.globalTimeline.clear();
      if (window.ScrollTrigger) {
        ScrollTrigger.getAll().forEach(t => t.kill());
      }
    }

    document.querySelectorAll("video, audio").forEach(m => {
      try {
        m.pause();
        m.removeAttribute("src");
        m.load();
      } catch (e) {}
    });

    window.location.href = "/?reset=" + Date.now();
  }

  function resetIdleTimer() {
    clearTimeout(idleTimer);

    idleTimer = setTimeout(() => {
      if (isVideoBoxPlaying()) {
        resetIdleTimer();
        return;
      }

      kioskReset();
    }, IDLE_TIME);
  }

  const events = [
    "pointerdown",
    "mousedown",
    "touchstart",
    "keydown",
    "wheel"
  ];

  events.forEach(evt =>
    document.addEventListener(evt, resetIdleTimer, true)
  );

  resetIdleTimer();
})();
