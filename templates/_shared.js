/* VizCraft shared runtime: injected into every template by generate.py. */

// Theme list is discovered from templates/_themes.css at generate time.
const VIZCRAFT_THEMES = /*__VIZCRAFT_THEME_LIST__*/[];

const REDUCED_MOTION = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function escapeHtml(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/* GSAP is loaded from a CDN. If it is unreachable (offline, blocked, file
   viewers) install a tiny stand-in that jumps straight to the final state, so
   the visualization still renders and works, just without entry animations. */
(function installGsapFallback() {
  if (typeof window.gsap !== 'undefined') return;
  const SKIP = { duration: 1, ease: 1, delay: 1, stagger: 1, onUpdate: 1, onComplete: 1, transformOrigin: 1 };
  function targets(t) {
    if (typeof t === 'string') return Array.from(document.querySelectorAll(t));
    if (t && !t.nodeType && typeof t.length === 'number') return Array.from(t);
    return [t];
  }
  function apply(t, vars) {
    if (!t) return;
    if (t.nodeType) {
      if (vars.attr) Object.keys(vars.attr).forEach(k => t.setAttribute(k, vars.attr[k]));
      if (vars.opacity !== undefined) t.style.opacity = vars.opacity;
      if (vars.strokeDashoffset !== undefined) t.style.strokeDashoffset = vars.strokeDashoffset;
      if (vars.y !== undefined || vars.scale !== undefined) {
        t.style.transform = 'translateY(' + (vars.y || 0) + 'px) scale(' + (vars.scale === undefined ? 1 : vars.scale) + ')';
      }
    } else {
      Object.keys(vars).forEach(k => { if (!SKIP[k]) t[k] = vars[k]; });
    }
    if (typeof vars.onUpdate === 'function') vars.onUpdate();
  }
  const chain = {
    to(t, vars) { targets(t).forEach(e => apply(e, vars)); return chain; },
    from() { return chain; },
    call(fn) { fn(); return chain; },
    fromTo(t, from, to) { targets(t).forEach(e => apply(e, to)); return chain; },
  };
  window.gsap = { to: chain.to, from: chain.from, fromTo: chain.fromTo, timeline: () => chain };
})();

/* Build the theme <select> from the discovered theme list. */
function populateThemeSelect(selectEl, current) {
  const themes = VIZCRAFT_THEMES.length ? VIZCRAFT_THEMES : [{ id: 'dark_neon', label: 'Dark Neon' }];
  selectEl.innerHTML = themes.map(t =>
    '<option value="' + escapeHtml(t.id) + '">' + escapeHtml(t.label) + '</option>').join('');
  selectEl.value = themes.some(t => t.id === current) ? current : themes[0].id;
}

/* Theme precedence: ?theme=<id> in the URL > project.theme > dark_neon. */
function resolveTheme(projectTheme) {
  let wanted = projectTheme;
  try {
    const q = new URLSearchParams(window.location.search).get('theme');
    if (q) wanted = q;
  } catch (e) { /* ignore */ }
  const known = VIZCRAFT_THEMES.map(t => t.id);
  return (wanted && (known.length === 0 || known.indexOf(wanted) !== -1)) ? wanted : 'dark_neon';
}
