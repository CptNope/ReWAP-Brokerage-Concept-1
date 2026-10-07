/* REWAP brand book — progressive enhancement only. Every page works without this file. */
(() => {
  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* Reveal: opt in only when motion is welcome and IntersectionObserver exists */
  if (!reduce.matches && 'IntersectionObserver' in window) {
    root.classList.add('js-motion');
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
    // Anything already above the fold reveals immediately
    requestAnimationFrame(() => document.querySelectorAll('.reveal').forEach((el) => {
      if (el.getBoundingClientRect().top < innerHeight) el.classList.add('in');
    }));
  }

  /* Chapter menu: close on Escape and on outside click */
  document.querySelectorAll('.book-nav').forEach((d) => {
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && d.open) { d.open = false; d.querySelector('summary').focus(); } });
    document.addEventListener('click', (e) => { if (d.open && !d.contains(e.target)) d.open = false; });
  });

  /* Toast */
  let toast;
  const say = (msg) => {
    if (!toast) { toast = document.createElement('div'); toast.className = 'toast'; toast.setAttribute('role', 'status'); document.body.append(toast); }
    toast.textContent = msg; toast.classList.add('show');
    clearTimeout(say.t); say.t = setTimeout(() => toast.classList.remove('show'), 1800);
  };

  /* Copy values */
  document.addEventListener('click', async (e) => {
    const b = e.target.closest('[data-copy]');
    if (!b) return;
    try { await navigator.clipboard.writeText(b.dataset.copy); say(`Copied ${b.dataset.copy}`); }
    catch { say('Copy is unavailable in this browser'); }
  });

  /* Logo lab */
  document.querySelectorAll('.lab').forEach((lab) => {
    const stage = lab.querySelector('.lab-stage');
    const img = lab.querySelector('.lab-art > img');
    const status = lab.querySelector('[data-lab-status]');
    const update = () => { if (status) status.textContent = `${lab.dataset.variantLabel} on ${lab.dataset.groundLabel}`; };
    lab.addEventListener('change', (e) => {
      const t = e.target;
      if (t.name === 'variant') {
        img.src = t.value; lab.dataset.variantLabel = t.dataset.label;
        if (t.dataset.ground) {
          const g = lab.querySelector(`input[name="ground"][value="${t.dataset.ground}"]`);
          if (g) { g.checked = true; stage.dataset.ground = g.value; lab.dataset.groundLabel = g.dataset.label; }
        }
      }
      if (t.name === 'ground') { stage.dataset.ground = t.value; lab.dataset.groundLabel = t.dataset.label; }
      if (t.name === 'construct') lab.dataset.construct = t.checked ? 'on' : 'off';
      update();
    });
  });

  /* Motion demos */
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-replay]');
    if (!b) return;
    const el = document.getElementById(b.dataset.replay);
    el.classList.remove('play'); void el.offsetWidth; el.classList.add('play');
  });
  document.querySelectorAll('[data-autoplay]').forEach((el) => {
    if (reduce.matches || !('IntersectionObserver' in window)) { el.classList.add('play'); return; }
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { el.classList.add('play'); io.disconnect(); } }, { threshold: 0.6 });
    io.observe(el);
  });

  /* Toggle buttons (save, chips) */
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[aria-pressed]');
    if (!b || b.disabled) return;
    const on = b.getAttribute('aria-pressed') !== 'true';
    b.setAttribute('aria-pressed', String(on));
    if (b.dataset.on && b.dataset.off) b.setAttribute('aria-label', on ? b.dataset.on : b.dataset.off);
  });

  /* Demo forms never submit */
  document.querySelectorAll('form[data-demo]').forEach((f) => f.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = f.querySelector('[type="submit"]');
    if (btn) { btn.classList.add('is-loading'); setTimeout(() => { btn.classList.remove('is-loading'); say('Demo only — nothing was sent'); }, 900); }
  }));
})();
