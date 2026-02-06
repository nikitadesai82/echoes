/* =========================================================
   GLOBAL STATE SWITCHER (HOME <-> DEEPDIVE)
========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  const homeView = document.getElementById('homeView');
  const deepdiveView = document.getElementById('deepdiveView');
  const portalVideo = document.getElementById('portalVideo');


  function cleanupGSAP() {
    if (window.ScrollTrigger) {
      ScrollTrigger.getAll().forEach(t => t.kill());
    }
    gsap.globalTimeline.clear();
  }

  window.switchToDeepdive = () => {
    // 🧹 kill animations from home
    cleanupGSAP();

    // 🔒 ensure video is ready
    if (portalVideo && portalVideo.readyState < 3) {
      document.documentElement.dataset.videoLoading = 'true';

      portalVideo.addEventListener(
        'canplaythrough',
        () => {
          document.documentElement.dataset.videoLoading = 'false';
          switchToDeepdive();
        },
        { once: true }
      );
      return;
    }

    homeView?.classList.remove('active');
    deepdiveView?.classList.add('active');
    document.body.dataset.state = 'deepdive';
  };

  window.switchToHome = () => {
    // 🧹 kill deepdive animations
    cleanupGSAP();

    deepdiveView?.classList.remove('active');
    homeView?.classList.add('active');
    document.body.dataset.state = 'home';

    playHomeIntro?.();
  };
});


/* =========================================================
   HOME → DEEPDIVE PORTAL TRIGGER
========================================================= */

function goToDeepdive() {
  const portal = document.querySelector('.circle-portal');
  const animBox = document.querySelector('.animation-box');

  portal?.classList.add('expand');
  animBox?.classList.add('expand-box');

  // Let animation finish, then request state switch
  window.setTimeout(() => {
    if (typeof window.switchToDeepdive === 'function') {
      window.switchToDeepdive();
    }
  }, 700);
}


/* =========================================================
   NAV ICON STATES
========================================================= */

function initNavigationButtons() {
  const buttons = document.querySelectorAll('img[data-active]');

  buttons.forEach((btn) => {
    const defaultSrc = btn.dataset.default;
    const activeSrc = btn.dataset.active;
    const isHomeIcon = btn.id === 'Home_2';

    if (isHomeIcon && document.body.dataset.state === 'home') {
  btn.src = activeSrc;
  btn.classList.add('active');
}

    btn.addEventListener('mouseenter', () => (btn.src = activeSrc));
    btn.addEventListener('mouseleave', () => (btn.src = defaultSrc));
    btn.addEventListener('mousedown', () => (btn.src = activeSrc));
    btn.addEventListener('mouseup', () => (btn.src = defaultSrc));
    btn.addEventListener('touchstart', () => (btn.src = activeSrc));
    btn.addEventListener('touchend', () => (btn.src = defaultSrc));
  });
}

/* =========================================================
   MENU DROPDOWN
========================================================= */

function initDropdownMenu() {
  const menuBtn = document.getElementById('menuBtn');
  const menuIcon = menuBtn?.querySelector('img');
  const mask = document.querySelector('.dropdown-mask');
  const dropdown = document.querySelector('.dropdown-content');

  if (!menuBtn || !menuIcon || !mask || !dropdown) return;

  const defaultSrc = menuIcon.dataset.default;
  const activeSrc = menuIcon.dataset.active;

  gsap.set(dropdown, { yPercent: -100, opacity: 0 });

  const tl = gsap.timeline({
    paused: true,
    onStart: () => {
      mask.style.pointerEvents = 'auto';
      menuIcon.src = activeSrc;
    },
    onReverseComplete: () => {
      mask.style.pointerEvents = 'none';
      menuIcon.src = defaultSrc;
    },
  });

  tl.to(dropdown, {
    yPercent: 0,
    opacity: 1,
    duration: 0.4,
    ease: 'power3.out',
  });

  let isOpen = false;

  menuBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    isOpen ? tl.reverse() : tl.play();
    isOpen = !isOpen;
    menuBtn.classList.toggle('is-open', isOpen);
  });

  document.addEventListener('click', () => {
    if (!isOpen) return;
    tl.reverse();
    isOpen = false;
    menuBtn.classList.remove('is-open');
  });

  mask.addEventListener('click', (e) => e.stopPropagation());
}

/* =========================================================
   HOME INTRO GSAP (UNCHANGED)
========================================================= */

function playHomeIntro() {
  gsap.killTweensOf('*');

  const master = gsap.timeline({ defaults: { ease: 'power3.out' } });

  master.fromTo(
    '.circle-portal',
    { yPercent: 100, opacity: 0 },
    { yPercent: 0, opacity: 1, duration: 0.6 }
  );

  master.fromTo(
    '.btn-fill-circle',
    { '--circle': 0 },
    { '--circle': 1.2, duration: 0.7, stagger: 0.12, ease: 'power2.out' },
    '-=0.2'
  );

  master.fromTo(
    '.left-bird',
    { xPercent: -100, opacity: 0 },
    { xPercent: 0, opacity: 1, duration: 0.6 },
    '-=0.3'
  );

  master.fromTo(
    '.right-bird',
    { xPercent: 100, opacity: 0 },
    { xPercent: 0, opacity: 1, duration: 0.6 },
    '<'
  );

  master.fromTo('.right-text', { opacity: 0 }, { opacity: 1, duration: 0.6 }, '-=0.2');
  master.fromTo('.left-text', { opacity: 0 }, { opacity: 1, duration: 0.6 }, '<');
}

/* =========================================================
   DEEPDIVE AUDIO PLAYER
========================================================= */

function initAudioPlayer() {
  const audio = document.getElementById('audioPlayer');
  const playBtn = document.getElementById('playPauseBtn');
  const maskRect = document.getElementById('maskRect');
  const svg = document.getElementById('audioWave');

  if (!audio || !playBtn || !maskRect || !svg) return;

  let rafId = null;

  function updateMask() {
    if (!audio.duration) return;
    const progress = audio.currentTime / audio.duration;
    maskRect.setAttribute('width', svg.clientWidth * progress);
    rafId = requestAnimationFrame(updateMask);
  }

  playBtn.addEventListener('click', () => {
    if (audio.paused) {
      audio.play();
      rafId = requestAnimationFrame(updateMask);
    } else {
      audio.pause();
      cancelAnimationFrame(rafId);
    }
  });

  audio.addEventListener('ended', () => {
    cancelAnimationFrame(rafId);
    maskRect.setAttribute('width', 0);
  });
}

/* =========================================================
   BACK BUTTON (STATE BASED)
========================================================= */

function initBackButton() {
  const backBtn = document.getElementById('backBtn');
  backBtn?.addEventListener('click', (e) => {
    e.preventDefault();
    switchToHome();
  });
}

/* =========================================================
   GLOBAL CLICK SOUND
========================================================= */

function initGlobalClickSound() {
  const sound = document.getElementById('globalClickSound');
  if (!sound) return;

  let unlocked = false;

  function unlock() {
    if (unlocked) return;
    sound.volume = 0.25;
    sound.play().then(() => {
      sound.pause();
      sound.currentTime = 0;
      unlocked = true;
    }).catch(() => {});
    document.removeEventListener('pointerdown', unlock, true);
  }

  document.addEventListener('pointerdown', unlock, true);

  document.addEventListener('pointerdown', (e) => {
    if (!unlocked) return;
    if (e.target.closest('.top-nav a, .menu-item, .deepdive-link, .birdspagelink_1')) {
      sound.currentTime = 0;
      sound.play().catch(() => {});
    }
  }, true);
}

/* =========================================================
   INIT
========================================================= */

function init() {
  // 🔒 VIDEO READY GATE — ADD THIS FIRST
  const portalVideo = document.querySelector('.portal-video');

  if (portalVideo) {
    document.documentElement.dataset.videoLoading = 'true';

    if (portalVideo.readyState >= 3) {
      // already enough data (fast reload / kiosk)
      document.documentElement.dataset.videoLoading = 'false';
    } else {
      portalVideo.addEventListener(
        'canplaythrough',
        () => {
          document.documentElement.dataset.videoLoading = 'false';
        },
        { once: true }
      );
    }
  }

  // ⬇️ EXISTING INIT LOGIC (unchanged)
  initNavigationButtons();
  initDropdownMenu();
  initAudioPlayer();
  initHiranandaniAnimation();
  initBackButton();
  initFooterAnimations();
  initScrollToTop();
  initGlobalClickSound();

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      initScrollAnimations();
      initAdditionalScrollAnimations();
    });
  });
}
