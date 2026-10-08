/* Local-only presentation helpers; no analytics, remote calls, or stored state. */
(() => {
  const chart = document.getElementById('education-income-map');
  if (!chart) return;
  const fallback = document.getElementById('chart-fallback');
  const statusObserver = new MutationObserver(() => {
    if (chart.dataset.error && fallback) fallback.hidden = false;
    if (chart.dataset.ready === 'true' || chart.dataset.error) statusObserver.disconnect();
  });
  statusObserver.observe(chart, { attributes: true, attributeFilter: ['data-ready', 'data-error'] });
  if (chart.dataset.error && fallback) fallback.hidden = false;

  const tooltip = document.createElement('div');
  tooltip.className = 'chart-tooltip';
  tooltip.hidden = true;
  tooltip.setAttribute('role', 'tooltip');
  tooltip.setAttribute('aria-hidden', 'true');
  document.body.appendChild(tooltip);
  let active = null;
  let timer = null;
  let pointer = { x: 0, y: 0 };
  function position() {
    const rect = tooltip.getBoundingClientRect();
    tooltip.style.left = Math.max(12, Math.min(pointer.x + 12, innerWidth - rect.width - 12)) + 'px';
    tooltip.style.top = Math.max(12, Math.min(pointer.y + 18, innerHeight - rect.height - 12)) + 'px';
  }
  function hide() {
    clearTimeout(timer);
    timer = null;
    tooltip.hidden = true;
    active = null;
  }
  chart.addEventListener('pointermove', event => {
    if (event.pointerType === 'touch') return;
    pointer = { x: event.clientX, y: event.clientY };
    const target = event.target.closest('[data-tooltip]');
    if (!target) { hide(); return; }
    if (target !== active) {
      hide();
      active = target;
      timer = setTimeout(() => {
        tooltip.textContent = target.getAttribute('data-tooltip');
        tooltip.hidden = false;
        position();
      }, 450);
    } else if (!tooltip.hidden) position();
  });
  chart.addEventListener('pointerleave', hide);
  chart.addEventListener('pointerdown', hide);
  chart.addEventListener('change', hide);
  document.addEventListener('keydown', event => { if (event.key === 'Escape') hide(); });
  window.addEventListener('scroll', hide, { passive: true });
  window.addEventListener('resize', hide, { passive: true });
})();
