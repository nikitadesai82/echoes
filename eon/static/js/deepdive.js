// ============================================
// INITIALIZATION FUNCTIONS
// ============================================

function initNavigationButtons() {
  const buttons = document.querySelectorAll('img[data-active]');
  const currentPath = window.location.pathname.replace(/\/$/, '');
  const homePaths = ['', '/', '/home'];

  buttons.forEach((btn) => {
    const defaultSrc = btn.dataset.default;
    const activeSrc = btn.dataset.active;
    const isHomeIcon = btn.id === 'Home_2';

    if (isHomeIcon && homePaths.includes(currentPath)) {
      btn.src = activeSrc;
      btn.classList.add('active');
      return;
    }

    btn.addEventListener('mouseenter', () => {
      btn.src = activeSrc;
    });

    btn.addEventListener('mouseleave', () => {
      btn.src = defaultSrc;
    });

    btn.addEventListener('mousedown', () => {
      btn.src = activeSrc;
    });

    btn.addEventListener('mouseup', () => {
      btn.src = defaultSrc;
    });

    btn.addEventListener('touchstart', () => {
      btn.src = activeSrc;
    });

    btn.addEventListener('touchend', () => {
      btn.src = defaultSrc;
    });
  });
}

function initDropdownMenu() {
  const menuBtn = document.getElementById('menuBtn');
  const menuIcon = menuBtn?.querySelector('img');
  const mask = document.querySelector('.dropdown-mask');
  const dropdown = document.querySelector('.dropdown-content');

  if (!menuBtn || !menuIcon || !mask || !dropdown) return;

  const defaultSrc = menuIcon.dataset.default;
  const activeSrc = menuIcon.dataset.active;

  gsap.set(dropdown, {
    yPercent: -100,
    opacity: 0,
  });

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

function initAudioPlayer() {
    const audio = document.getElementById('audioPlayer');
    const playBtn = document.getElementById('playPauseBtn');
    const maskRect = document.getElementById('maskRect');
    const svg = document.getElementById('audioWave');

    if (!audio || !playBtn || !maskRect || !svg) return;

    let rafId = null;

    function updateMaskSmooth() {
        if (!audio.duration) return;

        const progress = audio.currentTime / audio.duration;
        const width = svg.getBoundingClientRect().width;

        maskRect.setAttribute('width', width * progress);
        rafId = requestAnimationFrame(updateMaskSmooth);
    }

    playBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play();
            playBtn.src = playBtn.dataset.pauseIcon;
            playBtn.alt = "Pause";
            rafId = requestAnimationFrame(updateMaskSmooth);
        } else {
            audio.pause();
            playBtn.src = playBtn.dataset.playIcon;
            playBtn.alt = "Play";
            cancelAnimationFrame(rafId);
        }
    });

    audio.addEventListener('ended', () => {
        cancelAnimationFrame(rafId);
        maskRect.setAttribute('width', 0);
        playBtn.src = playBtn.dataset.playIcon;
        playBtn.alt = "Play";
    });

    audio.addEventListener('loadedmetadata', () => {
        maskRect.setAttribute('width', 0);
    });
}


function initScrollAnimations() {
  gsap.registerPlugin(ScrollTrigger);

  // Bounce up animation
  gsap.utils.toArray('.bounce-up').forEach((el) => {
    gsap.fromTo(
      el,
      {
        y: 40,
        scale: 0.7,
        opacity: 0,
      },
      {
        y: 0,
        scale: 1,
        opacity: 1,
        duration: 0.6,
        ease: 'back.out(2.5)',
        scrollTrigger: {
          trigger: el,
          start: 'top 80%',
          toggleActions: 'play none none none',
      		once: true
        },
      },
    );
  });

  // Button fill left animation
  gsap.utils
    .toArray('.btn-fill-left:not(.hiranandani-text-box .btn-fill-left)')
    .forEach((btn) => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: btn,
          start: 'top 80%',
          toggleActions: 'play none none none',
      		once: true
        },
      });

      tl.fromTo(
        btn,
        { '--reveal': 0 },
        {
          '--reveal': 1.08,
          duration: 0.6,
          ease: 'power2.out',
        },
      ).to(
        btn,
        {
          '--reveal': 1,
          duration: 0.25,
          ease: 'back.out(1.4)',
        },
        '-=0.2',
      );
    });
}

function initHiranandaniAnimation() {
  const hTL = gsap.timeline({
    defaults: { ease: 'power3.out' },
    scrollTrigger: {
      trigger: '.hiranandani-box',
      start: 'top 75%',
      toggleActions: 'play none none none',
      		once: true
    },
  });

  hTL
    .fromTo(
      '.hiranandani-img-box',
      { opacity: 0, y: 40, scale: 0.95 },
      { opacity: 1, y: 0, scale: 1, duration: 0.5 },
    )
    .fromTo(
      '.hiranandani-text-2 .inner2',
      { yPercent: 100, opacity: 0 },
      { yPercent: 0, opacity: 1, duration: 0.5 },
      '<',
    )
    .fromTo(
      '.hiranandani-text-1, .hiranandani-text-3, .hiranandani-text-4',
      { opacity: 0, y: 30 },
      {
        opacity: 1,
        y: 0,
        duration: 0.45,
        stagger: 0.12,
      },
      '-=0.15',
    )
    .fromTo(
      '.hiranandani-text-box .btn-fill-left',
      { opacity: 0, '--reveal': 0 },
      {
        opacity: 1,
        '--reveal': 1.08,
        duration: 0.5,
        ease: 'power2.out',
      },
    )
    .to(
      '.hiranandani-text-box .btn-fill-left',
      {
        '--reveal': 1,
        duration: 0.25,
        ease: 'back.out(1.4)',
      },
      '-=0.2',
    );
}

function initAdditionalScrollAnimations() {
  // Fade sections
  gsap.utils
    .toArray(
      '.fade-section:not(.hiranandani-text-1):not(.hiranandani-text-3):not(.hiranandani-text-4)',
    )
    .forEach((el) => {
      gsap.fromTo(
        el,
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none',
      		once: true
          },
        },
      );
    });

  // Reveal animations
  gsap.utils.toArray('.reveal').forEach((el) => {
    gsap.from(el, {
      opacity: 0,
      scale: 0.95,
      transformOrigin: '50% 50%',
      duration: 1.4,
      ease: 'expo.out',
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        end: 'top 30%',
        toggleActions: 'play none none none',
      		once: true
      },
    });
  });

  // Nature trail image blocks
  gsap.utils.toArray('.naturetrail-imgblock').forEach((block) => {
    gsap.fromTo(
      block,
      { opacity: 0, scale: 0.95 },
      {
        opacity: 1,
        scale: 1,
        duration: 1.1,
        ease: 'expo.out',
        scrollTrigger: {
          trigger: block,
          start: 'top 75%',
          toggleActions: 'play none none none',
      		once: true
        },
      },
    );
  });

  // Inner2 text blocks
  gsap.utils
    .toArray('.inner2:not(.hiranandani-text-2 .inner2)')
    .forEach((el) => {
      gsap.fromTo(
        el,
        { yPercent: 100, opacity: 0 },
        {
          yPercent: 0,
          opacity: 1,
          duration: 0.6,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: el.closest('.naturetrail-textblock'),
            start: 'top 80%',
            toggleActions: 'play none none none',
      		once: true
          },
        },
      );
    });

  // Right 6 element
  gsap.fromTo(
    '.right_6',
    {
      opacity: 0,
      transformOrigin: '50% 50%',
    },
    {
      opacity: 1,
      y: 20,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: '.right_6',
        start: 'top 75%',
        end: 'top 25%',
        scrub: 1,
      },
    },
  );
}

function initBackButton() {
  const backBtn = document.getElementById('backBtn');
  if (!backBtn) return;

  backBtn.addEventListener('click', function (e) {
    e.preventDefault();

    const referrer = document.referrer;

    if (referrer && referrer.includes(window.location.origin)) {
      window.location.href = referrer;
    } else {
      window.location.href = "{% url 'home' %}";
    }
  });
}

function initFooterAnimations() {
  gsap.utils.toArray('.fade-section2').forEach((el) => {
    gsap.from(el, {
      opacity: 0,
      y: 50,
      duration: 0.6,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: el,
        start: 'top 95%',
        toggleActions: 'play none none none',
      		once: true
      },
    });
  });

  gsap.fromTo(
    '.footer-img',
    {
      opacity: 0,
      y: 40,
    },
    {
      opacity: 1,
      y: 0,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: '.footer-img',
        start: 'top 85%',
        end: 'bottom 90%',
        scrub: 1,
      },
    },
  );
}

function initScrollToTop() {
  const scrollBtn = document.getElementById('scrollUpBtn');
  if (!scrollBtn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > window.innerHeight * 0.3) {
      scrollBtn.classList.add('active');
    } else {
      scrollBtn.classList.remove('active');
    }
  });

  scrollBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  });
}

function initGlobalClickSound() {
  const sound = document.getElementById('globalClickSound');
  if (!sound) return;

  let unlocked = false;

  function unlock() {
    if (unlocked) return;
    sound.volume = 0.25;
    sound
      .play()
      .then(() => {
        sound.pause();
        sound.currentTime = 0;
        unlocked = true;
      })
      .catch(() => {});
    document.removeEventListener('pointerdown', unlock, true);
  }

  document.addEventListener('pointerdown', unlock, true);

  document.addEventListener(
    'pointerdown',
    (e) => {
      if (!unlocked) return;

      if (
        e.target.closest(
          '.top-nav a, .menu-item,#Back_2,#Home_2,.menu-item,.bg-dots,.bg-nav-btn,.play-button,.left_4,.right_3,.MD-message-link,.naturetrail-link,.urbanlegend-link,.birdwatch-link,#scrollUpBtn',
        )
      ) {
        sound.currentTime = 0;
        sound.play().catch(() => {});
      }
    },
    true,
  );
}
function initAfterFirstPaint(fn) {
  requestAnimationFrame(() => {
    requestAnimationFrame(fn);
  });
}

// ============================================
// MAIN INITIALIZATION
// ============================================
function init() {
  initNavigationButtons();
  initDropdownMenu();
  initAudioPlayer();
  initHiranandaniAnimation();
  initBackButton();
  initFooterAnimations();
  initScrollToTop();
  initGlobalClickSound();

  // ⬇️ GSAP ONLY ONCE
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      initScrollAnimations();
      initAdditionalScrollAnimations();
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init, { once: true });
} else {
  init();
}


// Single DOMContentLoaded listener with readyState check
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init, { once: true });
} else {
  init();
}

// ============================================
// NON-DOM DEPENDENT EVENT LISTENERS
// ============================================

// Page show (back/forward cache)
window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    const dropdown = document.querySelector('.dropdown-content');
    const mask = document.querySelector('.dropdown-mask');
    const menuBtn = document.getElementById('menuBtn');
    const menuIcon = menuBtn?.querySelector('img');

    if (!dropdown || !mask || !menuBtn || !menuIcon) return;

    gsap.set(dropdown, {
      yPercent: -100,
      opacity: 0,
    });

    mask.style.pointerEvents = 'none';
    menuBtn.classList.remove('is-open');
    menuIcon.src = menuIcon.dataset.default;
  }
});

let scrollSpeed = 3;
let wheelEnabled = false;

// Enable wheel ONLY after load + one frame
window.addEventListener('load', () => {
  requestAnimationFrame(() => {
    wheelEnabled = true;
    document.documentElement.dataset.loading = 'false';
  });
});

window.addEventListener(
  'wheel',
  (e) => {
    if (!wheelEnabled) return;

    e.preventDefault();

    window.scrollTo({
      top: window.scrollY + e.deltaY * scrollSpeed,
      behavior: 'smooth',
    });
  },
  { passive: false },
);

