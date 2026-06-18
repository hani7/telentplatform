/**
 * Searchable Dropdown — auto-converts all <select> elements
 * inside a given container into searchable dropdowns.
 *
 * Usage: call  initSearchableDropdowns()  after DOM is ready.
 */
(function () {
  'use strict';

  /* ── CSS (injected once) ── */
  const STYLE = `
    .sd-wrap{position:relative;margin-bottom:.6rem}
    .sd-input{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.22);border-radius:11px;color:#fff;padding:.6rem .9rem;width:100%;font-size:.88rem;box-sizing:border-box;cursor:pointer;transition:border-color .2s,background .2s}
    .sd-input::placeholder{color:rgba(255,255,255,.38)}
    .sd-input:focus{outline:none;border-color:#f1b10f;background:rgba(255,255,255,.13)}
    .sd-arrow{position:absolute;right:12px;top:50%;transform:translateY(-50%);color:rgba(255,255,255,.45);pointer-events:none;font-size:.85rem;transition:transform .2s}
    .sd-wrap.open .sd-arrow{transform:translateY(-50%) rotate(180deg)}
    .sd-list{position:absolute;left:0;right:0;top:100%;margin-top:4px;background:#132a1a;border:1.5px solid rgba(255,255,255,.18);border-radius:12px;max-height:220px;overflow-y:auto;z-index:100;display:none;box-shadow:0 8px 24px rgba(0,0,0,.5)}
    .sd-wrap.open .sd-list{display:block}
    .sd-opt{padding:8px 12px;color:rgba(255,255,255,.8);font-size:.85rem;cursor:pointer;transition:background .15s}
    .sd-opt:hover,.sd-opt.hl{background:rgba(241,177,15,.15);color:#fff}
    .sd-opt.selected{color:#f1b10f;font-weight:600}
    .sd-none{padding:10px 12px;color:rgba(255,255,255,.35);font-size:.82rem;text-align:center}
    .sd-list::-webkit-scrollbar{width:4px}
    .sd-list::-webkit-scrollbar-track{background:transparent}
    .sd-list::-webkit-scrollbar-thumb{background:rgba(255,255,255,.15);border-radius:4px}
  `;

  let styleInjected = false;
  function injectStyle() {
    if (styleInjected) return;
    const s = document.createElement('style');
    s.textContent = STYLE;
    document.head.appendChild(s);
    styleInjected = true;
  }

  /* ── Build one searchable dropdown ── */
  function convert(select) {
    if (select.dataset.sdDone) return;           // skip if already converted
    if (select.options.length <= 3) return;       // skip tiny selects (e.g. Yes/No)
    select.dataset.sdDone = '1';

    // Collect options
    const opts = [];
    for (let i = 0; i < select.options.length; i++) {
      opts.push({ value: select.options[i].value, text: select.options[i].text, idx: i });
    }

    // Hide original select
    select.style.display = 'none';

    // Wrapper
    const wrap = document.createElement('div');
    wrap.className = 'sd-wrap';

    // Text input for searching
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'sd-input';
    input.placeholder = 'Rechercher…';
    input.autocomplete = 'off';

    // Set initial value
    const selOpt = select.options[select.selectedIndex];
    if (selOpt && selOpt.value) input.value = selOpt.text;

    // Arrow
    const arrow = document.createElement('span');
    arrow.className = 'sd-arrow';
    arrow.innerHTML = '▼';

    // Dropdown list
    const list = document.createElement('div');
    list.className = 'sd-list';

    function renderOptions(filter) {
      list.innerHTML = '';
      const q = (filter || '').toLowerCase();
      let count = 0;
      opts.forEach(o => {
        if (q && !o.text.toLowerCase().includes(q)) return;
        const div = document.createElement('div');
        div.className = 'sd-opt';
        if (select.value === o.value) div.classList.add('selected');
        div.textContent = o.text;
        div.addEventListener('mousedown', e => {     // mousedown so it fires before blur
          e.preventDefault();
          select.value = o.value;
          select.dispatchEvent(new Event('change', { bubbles: true }));
          input.value = o.text;
          close();
        });
        list.appendChild(div);
        count++;
      });
      if (count === 0) {
        const none = document.createElement('div');
        none.className = 'sd-none';
        none.textContent = 'Aucun résultat';
        list.appendChild(none);
      }
    }

    function open() { wrap.classList.add('open'); renderOptions(input.value === (selOpt && selOpt.text) ? '' : input.value); }
    function close() { wrap.classList.remove('open'); }

    input.addEventListener('focus', () => { input.select(); open(); });
    input.addEventListener('input', () => { renderOptions(input.value); if (!wrap.classList.contains('open')) open(); });
    input.addEventListener('blur', () => {
      // Restore selected text if nothing was picked
      const cur = select.options[select.selectedIndex];
      if (cur && cur.value) input.value = cur.text;
      else input.value = '';
      close();
    });

    wrap.appendChild(input);
    wrap.appendChild(arrow);
    wrap.appendChild(list);
    select.parentNode.insertBefore(wrap, select.nextSibling);
  }

  /* ── Public init ── */
  window.initSearchableDropdowns = function (root) {
    injectStyle();
    (root || document).querySelectorAll('select').forEach(convert);
  };
})();
