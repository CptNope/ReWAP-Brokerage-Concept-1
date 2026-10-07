/* REWAP Concept 1 website — progressive enhancement. Pages render fully without it. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* storage unavailable */ } },
  };

  /* Sheets (menu, filters): native <dialog> with focus return */
  $$('[data-open]').forEach((btn) => {
    const dlg = document.getElementById(btn.dataset.open);
    if (!dlg || typeof dlg.showModal !== 'function') return;
    btn.addEventListener('click', () => { dlg.showModal(); btn.setAttribute('aria-expanded', 'true'); });
    dlg.addEventListener('close', () => { btn.setAttribute('aria-expanded', 'false'); btn.focus(); });
    dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
  });
  $$('[data-close]').forEach((b) => b.addEventListener('click', () => b.closest('dialog').close()));

  /* Saved listings (this browser only) */
  const saved = new Set(store.get('rewap-saved', []));
  const paintSaved = () => {
    $$('[data-save]').forEach((b) => {
      const on = saved.has(b.dataset.save);
      b.setAttribute('aria-pressed', String(on));
      b.setAttribute('aria-label', `${on ? 'Remove' : 'Save'} ${b.dataset.label}${on ? ' from saved' : ''}`);
    });
    $$('.saved-count').forEach((el) => { el.textContent = saved.size ? `(${saved.size})` : ''; });
  };
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-save]');
    if (!b) return;
    e.preventDefault(); e.stopImmediatePropagation();
    saved.has(b.dataset.save) ? saved.delete(b.dataset.save) : saved.add(b.dataset.save);
    store.set('rewap-saved', [...saved]); paintSaved();
  }, true);
  paintSaved();

  /* Share */
  $$('[data-share]').forEach((b) => b.addEventListener('click', async () => {
    const url = location.href;
    try {
      if (navigator.share) await navigator.share({ title: document.title, url });
      else { await navigator.clipboard.writeText(url); b.querySelector('span').textContent = 'Link copied'; }
    } catch { /* dismissed */ }
  }));

  /* Search */
  const page = $('[data-search-page]');
  if (!page) return;
  const rows = $$('.result', page);
  const pins = $$('.pin', page);
  const count = $('[data-count]', page);
  const empty = $('.empty', page);
  const form = $('#search-form');
  const split = $('.split', page);
  const card = $('.map-card', page);
  const params = new URLSearchParams(location.search);
  if (params.get('q') && form.q) form.q.value = params.get('q');
  if (params.get('region') && form.region) form.region.value = params.get('region');
  if (params.get('status') && form.status) form.status.value = params.get('status');

  const fmt = (n) => `$${n.toLocaleString('en-US')}`;
  const apply = () => {
    const f = new FormData(form);
    const q = (f.get('q') || '').toString().trim().toLowerCase();
    const min = +f.get('min') || 0, max = +f.get('max') || Infinity, beds = +f.get('beds') || 0;
    const type = f.get('type') || '', region = f.get('region') || '', status = f.get('status') || '';
    let n = 0;
    rows.forEach((r) => {
      const d = r.dataset;
      const ok = (!q || d.search.includes(q)) && +d.price >= min && +d.price <= max && +d.beds >= beds &&
        (!type || d.type === type) && (!region || d.region === region) && (!status || d.status === status);
      r.hidden = !ok;
      if (ok) n++;
    });
    const shown = new Set(rows.filter((r) => !r.hidden).map((r) => r.dataset.id));
    pins.forEach((p) => {
      const ids = p.dataset.ids.split(','), prices = p.dataset.prices.split(',');
      const vis = ids.filter((id) => shown.has(id));
      p.hidden = vis.length === 0;
      p.classList.toggle('cluster', vis.length > 1);
      p.textContent = vis.length > 1 ? `${vis.length} homes` : (prices[ids.indexOf(vis[0])] || '');
      const r = vis.length === 1 && rows.find((x) => x.dataset.id === vis[0]);
      p.setAttribute('aria-label', vis.length > 1 ? `${vis.length} homes near ${p.dataset.near}` : r ? `${fmt(+r.dataset.price)}, ${r.dataset.address}` : '');
    });
    const sort = f.get('sort');
    const list = $('.results', page);
    const visible = rows.slice().sort((a, b) => {
      if (sort === 'price-asc') return a.dataset.price - b.dataset.price;
      if (sort === 'price-desc') return b.dataset.price - a.dataset.price;
      if (sort === 'size') return b.dataset.sqft - a.dataset.sqft;
      return 0;
    });
    visible.forEach((r) => list.append(r));
    count.textContent = `${n} sample ${n === 1 ? 'home' : 'homes'}`;
    empty.hidden = n > 0;
    const u = new URL(location);
    ['q', 'region', 'status', 'type', 'beds', 'min', 'max', 'sort'].forEach((k) => { const v = f.get(k); v ? u.searchParams.set(k, v) : u.searchParams.delete(k); });
    history.replaceState(null, '', u);
  };
  form.addEventListener('input', apply);
  form.addEventListener('submit', (e) => { e.preventDefault(); apply(); const d = $('#filters'); if (d?.open) d.close(); });
  $$('[data-reset]', page).forEach((b) => b.addEventListener('click', () => { form.reset(); apply(); }));
  apply();

  const visibleIds = (p) => p.dataset.ids.split(',').filter((id) => { const r = rows.find((x) => x.dataset.id === id); return r && !r.hidden; });
  const activate = (id) => {
    rows.forEach((r) => r.classList.toggle('is-active', r.dataset.id === id));
    pins.forEach((p) => p.classList.toggle('is-active', p.dataset.ids.split(',').includes(id)));
  };
  const showCard = (p) => {
    const ids = visibleIds(p);
    const items = ids.map((id) => rows.find((x) => x.dataset.id === id));
    card.innerHTML = items.length === 1
      ? `<span class="property-price" style="font-size:1.375rem">${fmt(+items[0].dataset.price)}</span><a class="property-address" href="${items[0].dataset.href}">${items[0].dataset.address}</a><span class="property-facts">${items[0].dataset.facts}</span>`
      : `<p class="small"><b style="color:var(--c-night)">${items.length} homes</b> near ${p.dataset.near}</p><ul>${items.map((r) => `<li><a href="${r.dataset.href}"><b>${fmt(+r.dataset.price)}</b><span>${r.dataset.address}</span></a></li>`).join('')}</ul>`;
    card.classList.add('show');
    pins.forEach((x) => x.classList.toggle('is-active', x === p));
    rows.forEach((r) => r.classList.toggle('is-active', ids.includes(r.dataset.id)));
    const first = items[0];
    if (first && matchMedia('(min-width: 64rem)').matches) first.scrollIntoView({ block: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  };
  pins.forEach((p) => p.addEventListener('click', () => showCard(p)));
  rows.forEach((r) => {
    r.addEventListener('mouseenter', () => activate(r.dataset.id));
    r.addEventListener('focusin', () => activate(r.dataset.id));
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && card.classList.contains('show')) card.classList.remove('show'); });

  const toggle = $('.view-toggle', page);
  toggle?.addEventListener('click', () => {
    const toMap = split.dataset.view !== 'map';
    split.dataset.view = toMap ? 'map' : 'list';
    toggle.querySelector('span').textContent = toMap ? 'List' : 'Map';
    toggle.setAttribute('aria-label', toMap ? 'Show results as a list' : 'Show results on the map');
    window.scrollTo(0, 0);
  });

  const tools = $('.search-tools');
  const setH = () => document.documentElement.style.setProperty('--tools-h', `${tools.offsetHeight}px`);
  setH(); addEventListener('resize', setH);
})();
