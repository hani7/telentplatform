/**
 * Searchable Dropdown v2
 * - Small selects (≤ 5 options)  → pill/chip buttons
 * - Large selects (> 5 options)  → bottom-sheet popup with search
 *
 * Usage: call  initSearchableDropdowns()  after DOM is ready.
 */
(function () {
  'use strict';

  /* ── Injected CSS ── */
  const STYLE = `
    /* ── Pill chips (small selects) ── */
    .sd-pills { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:.6rem; }
    .sd-pill {
      padding:6px 14px; border-radius:50px; font-size:.82rem; font-weight:600; cursor:pointer;
      background:rgba(255,255,255,.08); border:1.5px solid rgba(255,255,255,.18);
      color:rgba(255,255,255,.72); transition:all .18s ease; user-select:none;
    }
    .sd-pill:hover { background:rgba(255,255,255,.16); color:#fff; }
    .sd-pill.active { background:#f1b10f; border-color:#f1b10f; color:#000; }

    /* ── Trigger input (large selects) ── */
    .sd-wrap { position:relative; margin-bottom:.6rem; }
    .sd-trigger {
      background:rgba(255,255,255,.09); border:1px solid rgba(255,255,255,.22);
      border-radius:11px; color:#fff; padding:.6rem .9rem; width:100%; font-size:.88rem;
      box-sizing:border-box; cursor:pointer; display:flex; align-items:center;
      justify-content:space-between; gap:6px; transition:border-color .2s, background .2s;
    }
    .sd-trigger:hover { border-color:rgba(255,255,255,.45); background:rgba(255,255,255,.13); }
    .sd-trigger .sd-val { flex:1; text-align:left; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:rgba(255,255,255,.9); }
    .sd-trigger .sd-val.placeholder { color:rgba(255,255,255,.38); }
    .sd-trigger .sd-arrow { color:rgba(255,255,255,.45); font-size:.8rem; flex-shrink:0; transition:transform .2s; }

    /* ── Popup overlay ── */
    .sd-overlay {
      position:fixed; inset:0; z-index:9000;
      background:rgba(0,0,0,.6); backdrop-filter:blur(4px);
      display:flex; align-items:flex-end; justify-content:center;
      opacity:0; pointer-events:none; transition:opacity .22s ease;
    }
    .sd-overlay.open { opacity:1; pointer-events:all; }

    /* ── Bottom sheet ── */
    .sd-sheet {
      background:#0f2416; border-radius:20px 20px 0 0;
      border:1.5px solid rgba(255,255,255,.14);
      width:100%; max-width:520px;
      max-height:75vh; display:flex; flex-direction:column;
      transform:translateY(100%); transition:transform .25s cubic-bezier(.4,0,.2,1);
      padding-bottom:env(safe-area-inset-bottom,0);
    }
    .sd-overlay.open .sd-sheet { transform:translateY(0); }

    /* Sheet header */
    .sd-sheet-head {
      padding:1rem 1rem .6rem; display:flex; align-items:center; gap:.6rem;
      border-bottom:1px solid rgba(255,255,255,.1); flex-shrink:0;
    }
    .sd-sheet-title { color:#f1b10f; font-weight:700; font-size:.95rem; flex:1; }
    .sd-close-btn {
      width:30px; height:30px; border-radius:50%; background:rgba(255,255,255,.1);
      border:none; color:rgba(255,255,255,.7); font-size:1rem; cursor:pointer;
      display:flex; align-items:center; justify-content:center; transition:background .2s;
    }
    .sd-close-btn:hover { background:rgba(255,255,255,.22); color:#fff; }

    /* Search input in sheet */
    .sd-search-wrap { padding:.6rem 1rem; flex-shrink:0; }
    .sd-search {
      width:100%; background:rgba(255,255,255,.09);
      border:1.5px solid rgba(255,255,255,.22); border-radius:10px;
      color:#fff; padding:.55rem .9rem; font-size:.88rem; box-sizing:border-box;
    }
    .sd-search::placeholder { color:rgba(255,255,255,.38); }
    .sd-search:focus { outline:none; border-color:#f1b10f; background:rgba(255,255,255,.13); }

    /* Options list */
    .sd-list {
      overflow-y:auto; flex:1; padding:.4rem 0;
    }
    .sd-list::-webkit-scrollbar { width:4px; }
    .sd-list::-webkit-scrollbar-thumb { background:rgba(255,255,255,.15); border-radius:4px; }
    .sd-opt {
      padding:10px 1rem; color:rgba(255,255,255,.82); font-size:.88rem; cursor:pointer;
      transition:background .15s; display:flex; align-items:center; justify-content:space-between;
    }
    .sd-opt:hover { background:rgba(241,177,15,.13); color:#fff; }
    .sd-opt.selected { color:#f1b10f; font-weight:700; }
    .sd-opt.selected::after { content:'✓'; font-size:.9rem; }
    .sd-none { padding:14px 1rem; color:rgba(255,255,255,.35); font-size:.85rem; text-align:center; }
  `;

  let styleInjected = false;
  function injectStyle() {
    if (styleInjected) return;
    const s = document.createElement('style');
    s.textContent = STYLE;
    document.head.appendChild(s);
    styleInjected = true;
  }

  /* ── Shared overlay (one for all popups) ── */
  let overlay, sheet, searchInput, listEl, sheetTitle;
  let currentSelect = null, currentTriggerEl = null;

  function buildOverlay() {
    if (overlay) return;
    overlay = document.createElement('div');
    overlay.className = 'sd-overlay';
    overlay.innerHTML = `
      <div class="sd-sheet">
        <div class="sd-sheet-head">
          <span class="sd-sheet-title">Sélectionner</span>
          <button class="sd-close-btn" type="button">✕</button>
        </div>
        <div class="sd-search-wrap">
          <input class="sd-search" type="text" placeholder="Rechercher…" autocomplete="off">
        </div>
        <div class="sd-list"></div>
      </div>`;
    document.body.appendChild(overlay);
    sheet       = overlay.querySelector('.sd-sheet');
    searchInput = overlay.querySelector('.sd-search');
    listEl      = overlay.querySelector('.sd-list');
    sheetTitle  = overlay.querySelector('.sd-sheet-title');

    overlay.querySelector('.sd-close-btn').addEventListener('click', closeOverlay);
    overlay.addEventListener('click', e => { if (e.target === overlay) closeOverlay(); });
    searchInput.addEventListener('input', () => renderList(searchInput.value));
  }

  function openOverlay(select, triggerEl, label) {
    buildOverlay();
    currentSelect    = select;
    currentTriggerEl = triggerEl;
    sheetTitle.textContent = label || 'Sélectionner';
    searchInput.value = '';
    renderList('');
    overlay.classList.add('open');
    setTimeout(() => searchInput.focus(), 250);
  }

  function closeOverlay() {
    overlay.classList.remove('open');
    currentSelect = null;
  }

  function renderList(filter) {
    if (!currentSelect) return;
    listEl.innerHTML = '';
    const q = filter.toLowerCase();
    let count = 0;
    for (let i = 0; i < currentSelect.options.length; i++) {
      const opt = currentSelect.options[i];
      if (!opt.value) continue;                          // skip blank
      if (q && !opt.text.toLowerCase().includes(q)) continue;
      const div = document.createElement('div');
      div.className = 'sd-opt' + (currentSelect.value === opt.value ? ' selected' : '');
      div.textContent = opt.text;
      div.addEventListener('click', () => {
        currentSelect.value = opt.value;
        currentSelect.dispatchEvent(new Event('change', { bubbles: true }));
        // Update trigger display
        if (currentTriggerEl) {
          const valEl = currentTriggerEl.querySelector('.sd-val');
          if (valEl) { valEl.textContent = opt.text; valEl.classList.remove('placeholder'); }
        }
        closeOverlay();
      });
      listEl.appendChild(div);
      count++;
    }
    if (count === 0) {
      const none = document.createElement('div');
      none.className = 'sd-none';
      none.textContent = 'Aucun résultat';
      listEl.appendChild(none);
    }
  }

  /* ── Convert LARGE select → popup trigger ── */
  function convertLarge(select) {
    if (select.dataset.sdDone) return;
    select.dataset.sdDone = '1';
    select.style.display = 'none';

    const wrap    = document.createElement('div');
    wrap.className = 'sd-wrap';

    const selOpt  = select.options[select.selectedIndex];
    const hasVal  = selOpt && selOpt.value;

    const trigger = document.createElement('div');
    trigger.className = 'sd-trigger';
    trigger.setAttribute('role', 'button');
    trigger.setAttribute('tabindex', '0');
    trigger.innerHTML = `
      <span class="sd-val ${hasVal ? '' : 'placeholder'}">${hasVal ? selOpt.text : 'Sélectionner…'}</span>
      <span class="sd-arrow">▼</span>`;

    const label = select.closest('.col-6, .col-4, .col-12, .fsi, .fc')
                        ?.querySelector('.fl, label')?.textContent?.trim() || '';

    trigger.addEventListener('click', () => openOverlay(select, trigger, label));
    trigger.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') openOverlay(select, trigger, label); });

    // Sync when select changes externally (e.g. JS reset)
    select.addEventListener('change', () => {
      const cur = select.options[select.selectedIndex];
      const valEl = trigger.querySelector('.sd-val');
      if (cur && cur.value) { valEl.textContent = cur.text; valEl.classList.remove('placeholder'); }
      else { valEl.textContent = 'Sélectionner…'; valEl.classList.add('placeholder'); }
    });

    wrap.appendChild(trigger);
    select.parentNode.insertBefore(wrap, select.nextSibling);
  }

  /* ── Convert SMALL select → pill chips ── */
  function convertSmall(select) {
    if (select.dataset.sdDone) return;
    select.dataset.sdDone = '1';
    select.style.display = 'none';

    const pills = document.createElement('div');
    pills.className = 'sd-pills';

    for (let i = 0; i < select.options.length; i++) {
      const opt = select.options[i];
      if (!opt.value) continue;
      const pill = document.createElement('span');
      pill.className = 'sd-pill' + (select.value === opt.value ? ' active' : '');
      pill.textContent = opt.text;
      pill.dataset.val = opt.value;
      pill.addEventListener('click', () => {
        pills.querySelectorAll('.sd-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        select.value = opt.value;
        select.dispatchEvent(new Event('change', { bubbles: true }));
      });
      pills.appendChild(pill);
    }

    // Sync when select changes externally
    select.addEventListener('change', () => {
      pills.querySelectorAll('.sd-pill').forEach(p => {
        p.classList.toggle('active', p.dataset.val === select.value);
      });
    });

    select.parentNode.insertBefore(pills, select.nextSibling);
  }

  /* ── Public init ── */
  window.initSearchableDropdowns = function (root) {
    injectStyle();
    (root || document).querySelectorAll('select').forEach(select => {
      if (select.dataset.sdDone) return;
      if (select.hasAttribute('data-sd-skip')) return;  // keep as native select
      // Count real (non-blank) options
      const realOpts = Array.from(select.options).filter(o => o.value).length;
      if (realOpts <= 5) {
        convertSmall(select);
      } else {
        convertLarge(select);
      }
    });
  };
})();

