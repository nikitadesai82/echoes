/* =========================================================
   GLOBAL STATE SWITCHER (HOME <-> DEEPDIVE)
========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  const home = document.getElementById('homeView');
  const deep = document.getElementById('deepdiveView');

  window.switchToDeepdive = () => {
    home?.classList.remove('active');
    deep?.classList.add('active');
    document.body.dataset.state = 'deepdive';
  };

  window.switchToHome = () => {
    deep?.classList.remove('active');
    home?.classList.add('active');
    document.body.dataset.state = 'home';
    playHomeIntro(); // replay home intro safely
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

  setTimeout(() => {
    switchToDeepdive();
  }, 700); // synced with your GSAP timing
}

/* =========================================================
   NAV ICON HOVER / ACTIVE STATES
========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('img[data-active]');

  buttons.forEach((btn) => {
    const defaultSrc = btn.dataset.default;
    const activeSrc = btn.dataset.active;
    const isHomeIcon = btn.id === 'Home_2';

    if (isHomeIcon) {
      btn.src = activeSrc;
      btn.classList.add('active');
      return;
    }

    btn.addEventListener('mouseenter', () => (btn.src = activeSrc));
    btn.addEventListener('mouseleave', () => (btn.src = defaultSrc));
    btn.addEventListener('mousedown', () => (btn.src = activeSrc));
    btn.addEventListener('mouseup', () => (btn.src = defaultSrc));
    btn.addEventListener('touchstart', () => (btn.src = activeSrc));
    btn.addEventListener('touchend', () => (btn.src = defaultSrc));
  });
});

/* =========================================================
   MENU DROPDOWN (GSAP)
========================================================= */

document.addEventListener('DOMContentLoaded', () => {
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
});

/* =========================================================
   HOME INTRO GSAP TIMELINE (UNCHANGED LOGIC)
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

document.addEventListener('DOMContentLoaded', playHomeIntro);

/* =========================================================
   AUDIO UNLOCK + GLOBAL CLICK SOUND
========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  const sound = document.getElementById('globalClickSound');
  if (!sound) return;

  let unlocked = false;

  function unlock() {
    if (unlocked) return;
    sound.volume = 0.25;
    sound.play()
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
          '.top-nav a, .menu-item, #Back_2, #Home_2, .deepdive-link, .birdspagelink_1'
        )
      ) {
        sound.currentTime = 0;
        sound.play().catch(() => {});
      }
    },
    true
  );
});

/* =========================================================
   DEEPDIVE BACK BUTTON
========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  const backBtn = document.getElementById('backBtn');
  backBtn?.addEventListener('click', (e) => {
    e.preventDefault();
    switchToHome();
  });
});
