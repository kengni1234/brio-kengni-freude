/**
 * ============================================================
 *  SMC PATCH — Auto-sync ICT Overlay when chart loads
 *  Kengni Finance — À ajouter dans trading_journal.html
 *  Placer juste avant </script> du dernier bloc script
 * ============================================================
 */

/* ── Auto-sync ICT data when main chart loads ──────────────── */
(function() {
  'use strict';

  // Map TradingView TF → Binance interval
  const TV_TO_SMC = {
    '1':'1m', '3':'3m', '5':'5m', '15':'15m', '30':'30m',
    '60':'1h', '120':'2h', '240':'4h', 'D':'1d', 'W':'1w', 'M':'1d',
  };

  let _smcAutoTimer = null;
  let _lastSMCSymbol = '';
  let _lastSMCTF = '';

  /**
   * Show a subtle status badge on the ICT overlay panel
   */
  function showSyncBadge(state, msg) {
    let badge = document.getElementById('smcSyncBadge');
    if (!badge) {
      badge = document.createElement('div');
      badge.id = 'smcSyncBadge';
      badge.style.cssText = `
        position:fixed; bottom:14px; right:14px; z-index:9999;
        background:rgba(10,14,26,.95); border:1px solid rgba(0,212,170,.35);
        border-radius:8px; padding:.4rem .9rem; font-size:.72rem;
        font-family:'Space Mono',monospace; color:#a8b2d1;
        display:flex; align-items:center; gap:.5rem;
        box-shadow:0 4px 15px rgba(0,0,0,.4);
        transition:opacity .3s; pointer-events:none;
      `;
      document.body.appendChild(badge);
    }

    const colors = {
      loading: '#f59e0b',
      ok:      '#00d4aa',
      error:   '#ef4444',
      info:    '#a5b4fc',
    };
    const icons = { loading:'⟳', ok:'✓', error:'✕', info:'ℹ' };
    badge.innerHTML = `
      <span style="color:${colors[state]||'#a8b2d1'};font-size:.9rem">${icons[state]||'·'}</span>
      <span>${msg}</span>
    `;
    badge.style.opacity = '1';

    // Auto-hide after 4 seconds (except loading)
    if (state !== 'loading') {
      setTimeout(() => { badge.style.opacity = '0'; }, 4000);
    }
  }

  /**
   * Run SMC analysis for the current symbol/TF and sync to ICT panel
   */
  async function runAutoSMC(sym, tv_tf) {
    if (typeof SMCEngine === 'undefined') return;

    const tf = TV_TO_SMC[tv_tf] || tv_tf || '1h';

    // Debounce — don't re-run for the same symbol+TF within 30 seconds
    const cacheKey = `${sym}-${tf}`;
    if (cacheKey === _lastSMCSymbol + '-' + _lastSMCTF) return;

    showSyncBadge('loading', `Analyse SMC ${sym} ${tf}…`);

    try {
      const candles = await SMCEngine.fetchAuto(sym, tf);
      if (!candles || candles.length < 20) throw new Error('Données insuffisantes');

      const smc = SMCEngine.runAll(candles);
      if (!smc) throw new Error('Analyse SMC échouée');

      // Sync detected data to localStorage and re-render ICT overlay
      SMCEngine.syncToICTPanel(smc);

      _lastSMCSymbol = sym;
      _lastSMCTF     = tf;

      const bias  = SMCEngine.getBias(smc);
      const score = SMCEngine.confluenceScore(smc);
      const fvgCount = (smc.fvg  || []).filter(f => !f.filled).length;
      const obCount  = (smc.ob   || []).filter(o => o.status !== 'mitigated').length;
      const liqCount = (smc.liq  || []).filter(l => !l.swept).length;

      showSyncBadge('ok',
        `${sym} | Biais: ${bias.bias} | FVG:${fvgCount} OB:${obCount} Liq:${liqCount}`
      );

      // Update ICT panel badge if present
      const biasEl = document.getElementById('ictBiasBadge');
      if (biasEl) {
        biasEl.innerHTML = `
          <span style="color:${bias.color};font-weight:800">${bias.bias}</span>
          <span style="color:var(--text-muted);font-size:.65rem"> · ${bias.confidence}%</span>
        `;
      }

    } catch (err) {
      showSyncBadge('error', `SMC: ${err.message}`);
      console.warn('[SMC Auto-Sync]', err);
    }
  }

  /**
   * Patch the existing loadChart() to trigger SMC auto-sync after loading
   */
  const _origLoadChart = window.loadChart;
  window.loadChart = function() {
    _origLoadChart && _origLoadChart.apply(this, arguments);

    // Debounce: wait 1.5s for the chart to start loading, then run SMC
    clearTimeout(_smcAutoTimer);
    _smcAutoTimer = setTimeout(() => {
      const sym = (document.getElementById('chartSymbol')?.value || 'EURUSD')
        .toUpperCase().trim();
      const tf  = window.currentInterval || '30';
      runAutoSMC(sym, tf);
    }, 1500);
  };

  /**
   * Also patch setTF to trigger sync when timeframe changes
   */
  const _origSetTF = window.setTF;
  window.setTF = function(btn, iv) {
    _origSetTF && _origSetTF.apply(this, arguments);
    // SMC sync triggered by the loadChart() patch above
  };

  /**
   * Add a "🔄 Auto-SMC" button next to the chart toolbar
   * This lets the user manually trigger re-analysis
   */
  document.addEventListener('DOMContentLoaded', () => {

    // Add "Bias" badge to ICT overlay panel
    const panel = document.getElementById('ictOverlayPanel');
    if (panel && !document.getElementById('ictBiasBadge')) {
      const biasRow = document.createElement('div');
      biasRow.className = 'ict-panel-row';
      biasRow.style.cssText = 'margin-top:.3rem;padding-top:.3rem;border-top:1px solid rgba(255,255,255,.07)';
      biasRow.innerHTML = `
        <span class="ict-panel-key">🧭 Biais Auto</span>
        <span class="ict-panel-val" id="ictBiasBadge" style="color:var(--text-muted)">—</span>
      `;
      const rows = document.getElementById('ictPanelRows');
      if (rows) rows.after(biasRow);
    }

    // Add "⚡ SMC Auto" refresh button to chart toolbar
    const toolbar = document.querySelector('.chart-toolbar');
    if (toolbar && !document.getElementById('smcAutoRefreshBtn')) {
      const btn = document.createElement('button');
      btn.id = 'smcAutoRefreshBtn';
      btn.className = 'btn-ghost';
      btn.style.cssText = 'padding:.3rem .75rem;font-size:.72rem;border-color:rgba(0,212,170,.3);color:var(--accent);background:rgba(0,212,170,.07)';
      btn.innerHTML = '⚡ SMC Auto';
      btn.title = 'Relancer l\'analyse SMC automatique';
      btn.onclick = () => {
        _lastSMCSymbol = ''; // Force re-run
        _lastSMCTF = '';
        const sym = (document.getElementById('chartSymbol')?.value || 'EURUSD').toUpperCase().trim();
        const tf  = window.currentInterval || '30';
        runAutoSMC(sym, tf);
      };
      toolbar.appendChild(btn);
    }

    // Run initial analysis when the charts tab is first opened
    const chartsTab = document.querySelector('.jt-tab[onclick*="charts"]');
    if (chartsTab) {
      const _origClick = chartsTab.onclick;
      chartsTab.onclick = function(e) {
        _origClick && _origClick.call(this, e);
        setTimeout(() => {
          const sym = (document.getElementById('chartSymbol')?.value || 'EURUSD').toUpperCase().trim();
          const tf  = window.currentInterval || '30';
          runAutoSMC(sym, tf);
        }, 2000);
      };
    }

    console.log('[SMC Patch] Auto-sync activé ✓');
  });

})();