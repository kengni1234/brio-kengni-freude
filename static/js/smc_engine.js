/**
 * ============================================================
 *  SMC ENGINE — Smart Money Concepts Auto-Detection
 *  Kengni Finance — /static/js/smc_engine.js
 *  Version 2.0 — Full ICT/SMC analysis engine
 * ============================================================
 */

'use strict';

const SMCEngine = (() => {

  /* ── Binance timeframe map ─────────────────────────────────── */
  const TF_MAP = {
    '1m':'1m',  '3m':'3m',  '5m':'5m',  '15m':'15m', '30m':'30m',
    '1h':'1h',  '2h':'2h',  '4h':'4h',  '6h':'6h',   '12h':'12h',
    '1d':'1d',  '1D':'1d',  '1w':'1w',  '1W':'1w',
    '2h':'2h',  '4h':'4h',
  };

  /* ── Forex/Stock OHLCV via public proxy ────────────────────── */
  const FOREX_SYMBOLS = /^(EUR|USD|GBP|JPY|CHF|CAD|AUD|NZD|XAU|XAG|OIL|SP500|NAS)/i;

  /* ============================================================
     FETCH FUNCTIONS
  ============================================================ */

  /**
   * Fetch candles from Binance Futures or Spot API
   */
  async function fetchBinance(sym, tf) {
    const interval = TF_MAP[tf] || tf || '1h';
    const symbol = sym.toUpperCase().trim();

    // Try futures first (more volume/liquidity)
    const urls = [
      `https://fapi.binance.com/fapi/v1/klines?symbol=${symbol}&interval=${interval}&limit=300`,
      `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=300`,
    ];

    let lastError;
    for (const url of urls) {
      try {
        const res = await fetch(url, { signal: AbortSignal.timeout(8000) });
        if (!res.ok) { lastError = new Error(`HTTP ${res.status}`); continue; }
        const data = await res.json();
        if (!Array.isArray(data) || data.length < 5) {
          lastError = new Error('Données insuffisantes'); continue;
        }
        return data.map(k => ({
          time:  Math.floor(Number(k[0]) / 1000),
          open:  parseFloat(k[1]),
          high:  parseFloat(k[2]),
          low:   parseFloat(k[3]),
          close: parseFloat(k[4]),
          vol:   parseFloat(k[5]),
        }));
      } catch (e) { lastError = e; }
    }
    throw lastError || new Error(`Binance: ${sym} introuvable`);
  }

  /**
   * Fetch candles from Flask backend (for forex/stocks)
   */
  async function fetchBackend(sym, tf) {
    const res = await fetch(
      `/api/candles?symbol=${encodeURIComponent(sym)}&tf=${encodeURIComponent(tf)}&limit=300`,
      { signal: AbortSignal.timeout(10000) }
    );
    if (!res.ok) throw new Error(`Backend ${res.status}`);
    const data = await res.json();
    const candles = data.candles || data;
    if (!Array.isArray(candles) || candles.length < 5) throw new Error('Backend: données vides');
    return candles.map(c => ({
      time:  c.time || c.timestamp,
      open:  parseFloat(c.open),
      high:  parseFloat(c.high),
      low:   parseFloat(c.low),
      close: parseFloat(c.close),
      vol:   parseFloat(c.vol || c.volume || 0),
    }));
  }

  /**
   * Auto-detect best data source for a given symbol
   */
  async function fetchAuto(sym, tf) {
    const s = sym.toUpperCase().trim();

    // Forex/metals — try backend first, then skip Binance
    if (FOREX_SYMBOLS.test(s)) {
      try { return await fetchBackend(s, tf); } catch (e) {}
    }

    // Crypto — try Binance directly
    const cryptoEndings = ['USDT','BUSD','BTC','ETH','BNB','SOL','XRP','ADA','DOGE','USDC'];
    const hasCryptoEnding = cryptoEndings.some(e => s.endsWith(e));

    if (hasCryptoEnding) {
      return fetchBinance(s, tf);
    }

    // Unknown — try USDT pair, then backend
    try { return await fetchBinance(s + 'USDT', tf); } catch (e) {}
    try { return await fetchBackend(s, tf); } catch (e) {}
    throw new Error(`Impossible de récupérer les données pour ${s}`);
  }

  /* ============================================================
     MATHEMATICAL HELPERS
  ============================================================ */

  function calcEMA(closes, period) {
    if (!closes || closes.length < period) return new Array(closes?.length || 0).fill(null);
    const k = 2 / (period + 1);
    const result = new Array(period - 1).fill(null);
    let ema = closes.slice(0, period).reduce((a, b) => a + b, 0) / period;
    result.push(ema);
    for (let i = period; i < closes.length; i++) {
      ema = closes[i] * k + ema * (1 - k);
      result.push(ema);
    }
    return result;
  }

  function calcATR(candles, period = 14) {
    const trs = candles.map((c, i) => {
      if (i === 0) return c.high - c.low;
      const prev = candles[i - 1];
      return Math.max(c.high - c.low, Math.abs(c.high - prev.close), Math.abs(c.low - prev.close));
    });
    const result = new Array(period).fill(null);
    let atr = trs.slice(0, period).reduce((a, b) => a + b, 0) / period;
    result.push(atr);
    for (let i = period + 1; i < trs.length; i++) {
      atr = (atr * (period - 1) + trs[i]) / period;
      result.push(atr);
    }
    return result;
  }

  /* ============================================================
     SWING DETECTION
  ============================================================ */

  function detectSwings(candles, lookback = 5) {
    const n = Math.max(3, Math.min(lookback, Math.floor(candles.length / 15)));
    const swings = [];

    for (let i = n; i < candles.length - n; i++) {
      const c = candles[i];
      let isHigh = true, isLow = true;

      for (let j = i - n; j <= i + n; j++) {
        if (j === i) continue;
        if (candles[j].high > c.high) isHigh = false;
        if (candles[j].low  < c.low)  isLow  = false;
      }
      if (isHigh) swings.push({ time: c.time, price: c.high, type: 'high', index: i, candle: c });
      if (isLow)  swings.push({ time: c.time, price: c.low,  type: 'low',  index: i, candle: c });
    }

    return swings.sort((a, b) => a.time - b.time);
  }

  /* ============================================================
     HH / HL / LH / LL (Market Structure Points)
  ============================================================ */

  function detectHHHL(swings) {
    const highs = swings.filter(s => s.type === 'high');
    const lows  = swings.filter(s => s.type === 'low');
    const points = [];

    for (let i = 1; i < highs.length; i++) {
      const label = highs[i].price > highs[i-1].price ? 'HH' : 'LH';
      points.push({
        time:  highs[i].time,
        price: highs[i].price,
        label,
        isBullish: label === 'HH',
        color: label === 'HH' ? '#6ee7b7' : '#fca5a5',
      });
    }
    for (let i = 1; i < lows.length; i++) {
      const label = lows[i].price > lows[i-1].price ? 'HL' : 'LL';
      points.push({
        time:  lows[i].time,
        price: lows[i].price,
        label,
        isBullish: label === 'HL',
        color: label === 'HL' ? '#6ee7b7' : '#fca5a5',
      });
    }
    return points.sort((a, b) => a.time - b.time);
  }

  /* ============================================================
     BOS / CHoCH DETECTION
  ============================================================ */

  function detectBOS(candles, swings) {
    const highs = swings.filter(s => s.type === 'high');
    const lows  = swings.filter(s => s.type === 'low');
    const events = [];

    // Bullish BOS — close breaks above previous swing high
    for (let i = 1; i < highs.length; i++) {
      const level = highs[i - 1].price;
      const breakCandles = candles.filter(c => c.time > highs[i-1].time && c.time <= highs[i].time);
      if (breakCandles.some(c => c.close > level)) {
        events.push({
          time: highs[i].time, price: level,
          type: 'BOS', direction: 'bullish',
          color: '#6ee7b7', label: 'BOS↑',
        });
      }
    }

    // Bearish BOS — close breaks below previous swing low
    for (let i = 1; i < lows.length; i++) {
      const level = lows[i - 1].price;
      const breakCandles = candles.filter(c => c.time > lows[i-1].time && c.time <= lows[i].time);
      if (breakCandles.some(c => c.close < level)) {
        events.push({
          time: lows[i].time, price: level,
          type: 'BOS', direction: 'bearish',
          color: '#fca5a5', label: 'BOS↓',
        });
      }
    }

    // Identify CHoCH — BOS that breaks the previous trend direction
    const sorted = events.sort((a, b) => a.time - b.time);
    for (let i = 1; i < sorted.length; i++) {
      if (sorted[i].direction !== sorted[i-1].direction) {
        sorted[i].type  = 'CHoCH';
        sorted[i].color = sorted[i].direction === 'bullish' ? '#a5b4fc' : '#fcd34d';
        sorted[i].label = sorted[i].direction === 'bullish' ? 'CHoCH↑' : 'CHoCH↓';
      }
    }

    return sorted.slice(-25);
  }

  /* ============================================================
     FAIR VALUE GAPS (Imbalances)
  ============================================================ */

  function detectFVG(candles) {
    const fvgs = [];
    const minSize = candles.reduce((acc, c) => acc + (c.high - c.low), 0) / candles.length * 0.3;

    for (let i = 2; i < candles.length; i++) {
      const [c1, c2, c3] = [candles[i-2], candles[i-1], candles[i]];

      // Bullish FVG: c1.high < c3.low — gap UP between candle 1 and candle 3
      if (c3.low > c1.high && (c3.low - c1.high) >= minSize) {
        fvgs.push({
          time:   c2.time,
          type:   'bullish',
          top:    c3.low,
          bottom: c1.high,
          size:   c3.low - c1.high,
          filled: false,
          fillPct: 0,
        });
      }

      // Bearish FVG: c1.low > c3.high — gap DOWN between candle 1 and candle 3
      if (c3.high < c1.low && (c1.low - c3.high) >= minSize) {
        fvgs.push({
          time:   c2.time,
          type:   'bearish',
          top:    c1.low,
          bottom: c3.high,
          size:   c1.low - c3.high,
          filled: false,
          fillPct: 0,
        });
      }
    }

    // Check fill status for each FVG
    fvgs.forEach(f => {
      const laterCandles = candles.filter(c => c.time > f.time);
      for (const c of laterCandles) {
        if (f.type === 'bullish') {
          const penetration = (f.top - Math.max(c.low, f.bottom)) / (f.top - f.bottom);
          f.fillPct = Math.max(f.fillPct, Math.max(0, Math.min(1, penetration)));
        } else {
          const penetration = (Math.min(c.high, f.top) - f.bottom) / (f.top - f.bottom);
          f.fillPct = Math.max(f.fillPct, Math.max(0, Math.min(1, penetration)));
        }
      }
      f.filled = f.fillPct >= 0.5;
    });

    // Return the most recent 25, prioritizing unfilled ones
    return fvgs
      .sort((a, b) => (a.filled === b.filled ? b.time - a.time : (a.filled ? 1 : -1)))
      .slice(0, 25);
  }

  /* ============================================================
     ORDER BLOCKS
  ============================================================ */

  function detectOrderBlocks(candles, swings) {
    const obs = [];
    const highs = swings.filter(s => s.type === 'high').slice(-12);
    const lows  = swings.filter(s => s.type === 'low').slice(-12);

    // Bullish OB — last bearish candle before an upward swing low→high impulse
    for (const sw of lows.slice(-6)) {
      const idx = sw.index;
      for (let i = idx - 1; i >= Math.max(0, idx - 15); i--) {
        const c = candles[i];
        if (c.close < c.open) { // bearish candle
          const laterCandles = candles.slice(idx);
          const status = _obStatus(c, laterCandles, 'bullish');
          obs.push({ time: c.time, type: 'bullish', high: c.high, low: c.low, status });
          break;
        }
      }
    }

    // Bearish OB — last bullish candle before a downward swing high→low impulse
    for (const sw of highs.slice(-6)) {
      const idx = sw.index;
      for (let i = idx - 1; i >= Math.max(0, idx - 15); i--) {
        const c = candles[i];
        if (c.close > c.open) { // bullish candle
          const laterCandles = candles.slice(idx);
          const status = _obStatus(c, laterCandles, 'bearish');
          obs.push({ time: c.time, type: 'bearish', high: c.high, low: c.low, status });
          break;
        }
      }
    }

    // Deduplicate by time
    const seen = new Set();
    return obs.filter(o => { const k = `${o.time}-${o.type}`; return seen.has(k) ? false : seen.add(k); }).slice(-14);
  }

  function _obStatus(ob, laterCandles, type) {
    let touched = false;
    for (const c of laterCandles) {
      if (type === 'bullish') {
        if (c.low <= ob.high && c.low >= ob.low) touched = true;
        if (c.close < ob.low) return 'mitigated';
      } else {
        if (c.high >= ob.low && c.high <= ob.high) touched = true;
        if (c.close > ob.high) return 'mitigated';
      }
    }
    return touched ? 'tested' : 'fresh';
  }

  /* ============================================================
     LIQUIDITY LEVELS (BSL / SSL)
  ============================================================ */

  function detectLiquidity(candles, swings) {
    const liqs = [];
    const highs = swings.filter(s => s.type === 'high').slice(-10);
    const lows  = swings.filter(s => s.type === 'low').slice(-10);

    highs.forEach(sw => {
      const later = candles.filter(c => c.time > sw.time);
      const swept = later.some(c => c.high > sw.price && c.close < sw.price);
      liqs.push({ t1: sw.time, price: sw.price, type: 'BSL', swept });
    });

    lows.forEach(sw => {
      const later = candles.filter(c => c.time > sw.time);
      const swept = later.some(c => c.low < sw.price && c.close > sw.price);
      liqs.push({ t1: sw.time, price: sw.price, type: 'SSL', swept });
    });

    // Sort by price descending, show intact levels + a few swept
    return liqs
      .sort((a, b) => b.price - a.price)
      .slice(0, 15);
  }

  /* ============================================================
     PREMIUM / DISCOUNT ZONES
  ============================================================ */

  function detectPD(candles) {
    const lookback = Math.min(100, candles.length);
    const slice = candles.slice(-lookback);
    const rangeHigh = Math.max(...slice.map(c => c.high));
    const rangeLow  = Math.min(...slice.map(c => c.low));
    const range = rangeHigh - rangeLow;
    if (range === 0) return null;

    const eq50  = (rangeHigh + rangeLow) / 2;
    const close = candles[candles.length - 1].close;
    const pct   = ((close - rangeLow) / range) * 100;

    let zone, bias;
    if (pct > 62.5)      { zone = 'PREMIUM';     bias = 'Short favorisé'; }
    else if (pct < 37.5) { zone = 'DISCOUNT';    bias = 'Long favorisé';  }
    else                 { zone = 'EQUILIBRIUM';  bias = 'Neutre';         }

    return { rangeHigh, rangeLow, eq50, pct, zone, bias };
  }

  /* ============================================================
     KILL ZONES (ICT — times in UTC)
  ============================================================ */

  function getKillZones() {
    const now  = new Date();
    const utcH = now.getUTCHours();
    const utcM = now.getUTCMinutes();
    const utcTotal = utcH * 60 + utcM;

    const zones = [
      { name: 'Asian KZ',     start: 0*60,    end: 3*60,   color: 'rgba(99,102,241,.18)',  label: 'Asian 00:00–03:00' },
      { name: 'London Open',  start: 7*60,    end: 10*60,  color: 'rgba(0,212,170,.15)',   label: 'London 07:00–10:00' },
      { name: 'NY Open',      start: 12*60+30,end: 15*60,  color: 'rgba(245,158,11,.15)',  label: 'NY 12:30–15:00' },
      { name: 'NY Close',     start: 19*60,   end: 20*60,  color: 'rgba(239,68,68,.12)',   label: 'NY Close 19:00–20:00' },
    ];

    return zones.map(z => ({
      ...z,
      active: utcTotal >= z.start && utcTotal < z.end,
      pctStart: z.start / 1440,
      pctEnd:   z.end   / 1440,
    }));
  }

  /* ============================================================
     SESSIONS (Forex market hours UTC)
  ============================================================ */

  function getSessions() {
    const now  = new Date();
    const utcH = now.getUTCHours();

    return [
      { name: 'Asie',     start: 0,  end: 9,  active: utcH >= 0  && utcH < 9,  color: '#6366f1' },
      { name: 'Londres',  start: 7,  end: 16, active: utcH >= 7  && utcH < 16, color: '#00d4aa' },
      { name: 'New York', start: 12, end: 21, active: utcH >= 12 && utcH < 21, color: '#f59e0b' },
    ];
  }

  /* ============================================================
     MAIN: runAll — Run every analysis on the candle set
  ============================================================ */

  function runAll(candles) {
    if (!candles || candles.length < 20) return null;

    try {
      // Sort by time (safety)
      candles = [...candles].sort((a, b) => a.time - b.time);

      const lookback = Math.max(3, Math.min(5, Math.floor(candles.length / 25)));
      const swings   = detectSwings(candles, lookback);
      const closes   = candles.map(c => c.close);
      const times    = candles.map(c => c.time);

      // EMAs
      const mkSeries = (arr) => arr
        .map((v, i) => v !== null ? { time: times[i], value: parseFloat(v.toFixed(8)) } : null)
        .filter(Boolean);

      const ema20  = calcEMA(closes, 20);
      const ema50  = calcEMA(closes, 50);
      const ema200 = calcEMA(closes, 200);

      // All analyses
      const ms     = detectHHHL(swings);
      const bos    = detectBOS(candles, swings);
      const fvg    = detectFVG(candles);
      const ob     = detectOrderBlocks(candles, swings);
      const liq    = detectLiquidity(candles, swings);
      const pd     = detectPD(candles);
      const kz     = getKillZones();
      const sess   = getSessions();

      return {
        candles,
        swings,
        ms,
        bos,
        fvg,
        ob,
        liq,
        pd,
        kz,
        sessions: sess,
        ema: {
          ema20:  mkSeries(ema20),
          ema50:  mkSeries(ema50),
          ema200: mkSeries(ema200),
        },
      };
    } catch (e) {
      console.error('[SMCEngine.runAll]', e);
      return null;
    }
  }

  /* ============================================================
     AUTO-POPULATE LOCALSTORAGE
     Call this after loading chart data to feed the ICT overlay
  ============================================================ */

  function syncToICTPanel(smc) {
    if (!smc) return;

    try {
      // FVG → ict_fvg
      if (smc.fvg && smc.fvg.length) {
        const mapped = smc.fvg.map((f, i) => ({
          id:     Date.now() + i,
          sym:    'AUTO',
          top:    parseFloat(f.top.toFixed(8)),
          bot:    parseFloat(f.bottom.toFixed(8)),
          dir:    f.type === 'bullish' ? 'bull' : 'bear',
          size:   parseFloat(f.size.toFixed(8)),
          filled: f.filled,
        }));
        localStorage.setItem('ict_fvg', JSON.stringify(mapped));
        window.fvgList = mapped;
        const el = document.getElementById('fvgList');
        if (el) renderFVGList && renderFVGList();
      }

      // OB → ict_ob
      if (smc.ob && smc.ob.length) {
        const mapped = smc.ob.map((o, i) => ({
          id:     Date.now() + i + 1000,
          sym:    'AUTO',
          tf:     'AUTO',
          dir:    o.type === 'bullish' ? 'bull' : 'bear',
          high:   parseFloat(o.high.toFixed(8)),
          low:    parseFloat(o.low.toFixed(8)),
          status: o.status,
        }));
        localStorage.setItem('ict_ob', JSON.stringify(mapped));
        window.obList = mapped;
        if (typeof renderOBList === 'function') renderOBList();
      }

      // Liquidity → ict_liq
      if (smc.liq && smc.liq.length) {
        const mapped = smc.liq.map((l, i) => ({
          id:     Date.now() + i + 2000,
          level:  parseFloat(l.price.toFixed(8)),
          type:   l.type === 'BSL' ? 'bsl' : 'ssl',
          status: l.swept ? 'swept' : 'intact',
        }));
        localStorage.setItem('ict_liq', JSON.stringify(mapped));
        window.liqData = mapped;
        if (typeof renderLiqList === 'function') renderLiqList();
      }

      // Market Structure → ict_ms
      if (smc.bos && smc.bos.length) {
        const mapped = smc.bos.slice(-10).map((b, i) => ({
          id:    Date.now() + i + 3000,
          type:  b.type === 'CHoCH'
                 ? (b.direction === 'bullish' ? 'choch-bull' : 'choch-bear')
                 : (b.direction === 'bullish' ? 'bos-bull'   : 'bos-bear'),
          level: parseFloat(b.price.toFixed(8)),
          tf:    'AUTO',
          time:  new Date(b.time * 1000).toLocaleTimeString('fr'),
        }));
        localStorage.setItem('ict_ms', JSON.stringify(mapped));
        window.msData = mapped;
        if (typeof renderMSList === 'function') renderMSList();
      }

      // Structure Points HH/HL/LH/LL → structPoints
      if (smc.ms && smc.ms.length) {
        const mapped = smc.ms.slice(-12).map((p, i) => ({
          id:     Date.now() + i + 4000,
          type:   p.label,
          price:  parseFloat(p.price.toFixed(8)),
          tf:     'AUTO',
          time:   new Date(p.time * 1000).toLocaleTimeString('fr'),
          color:  p.color,
        }));
        window.structPoints = mapped;
        if (typeof renderStructPointsList === 'function') renderStructPointsList();
      }

      // Re-render the ICT overlay and panel
      if (typeof renderICTOverlay === 'function') renderICTOverlay();
      if (typeof updateICTPanel   === 'function') updateICTPanel();

    } catch (e) {
      console.warn('[SMCEngine.syncToICTPanel]', e);
    }
  }

  /* ============================================================
     SCORING — Confluence Score (0–10)
  ============================================================ */

  function confluenceScore(smc) {
    if (!smc) return { score: 0, details: [] };
    let score = 0;
    const details = [];
    const last = smc.candles ? smc.candles[smc.candles.length - 1] : null;

    if (!last) return { score, details };

    const price = last.close;

    // 1. BOS bullish
    const lastBOS = (smc.bos || []).slice(-3);
    const hasBullBOS = lastBOS.some(b => b.direction === 'bullish' && b.type === 'BOS');
    const hasBullCHoCH = lastBOS.some(b => b.direction === 'bullish' && b.type === 'CHoCH');
    if (hasBullBOS)   { score += 1; details.push({ label: 'BOS Bullish', pts: 1, bull: true }); }
    if (hasBullCHoCH) { score += 2; details.push({ label: 'CHoCH Bullish', pts: 2, bull: true }); }

    // 2. FVG near price
    const nearFVG = (smc.fvg || []).filter(f => !f.filled && price >= f.bottom && price <= f.top);
    if (nearFVG.length) { score += 2; details.push({ label: 'Dans un FVG', pts: 2, bull: nearFVG[0].type === 'bullish' }); }

    // 3. Order Block near price
    const nearOB = (smc.ob || []).filter(o => o.status !== 'mitigated' && price >= o.low && price <= o.high);
    if (nearOB.length) { score += 2; details.push({ label: 'Sur un OB', pts: 2, bull: nearOB[0].type === 'bullish' }); }

    // 4. Liquidity above/below
    const intactBSL = (smc.liq || []).filter(l => l.type === 'BSL' && !l.swept && l.price > price);
    const intactSSL = (smc.liq || []).filter(l => l.type === 'SSL' && !l.swept && l.price < price);
    if (intactBSL.length) { score += 1; details.push({ label: 'BSL disponible', pts: 1, bull: true }); }
    if (intactSSL.length) { score += 1; details.push({ label: 'SSL disponible', pts: 1, bull: false }); }

    // 5. Premium / Discount zone
    if (smc.pd) {
      if (smc.pd.zone === 'DISCOUNT') { score += 1; details.push({ label: 'Zone Discount', pts: 1, bull: true }); }
      if (smc.pd.zone === 'PREMIUM')  { score += 1; details.push({ label: 'Zone Premium',  pts: 1, bull: false }); }
    }

    return { score: Math.min(10, score), max: 10, details };
  }

  /* ============================================================
     BIAS DETECTION
  ============================================================ */

  function getBias(smc) {
    if (!smc || !smc.bos || !smc.bos.length) return { bias: 'NEUTRE', color: '#9ca3af', confidence: 0 };

    const recent = smc.bos.slice(-5);
    let bull = 0, bear = 0;

    recent.forEach(b => {
      const w = b.type === 'CHoCH' ? 2 : 1;
      if (b.direction === 'bullish') bull += w;
      else bear += w;
    });

    const total = bull + bear || 1;
    if (bull > bear) return { bias: 'HAUSSIER', color: '#6ee7b7', confidence: Math.round(bull/total*100) };
    if (bear > bull) return { bias: 'BAISSIER', color: '#fca5a5', confidence: Math.round(bear/total*100) };
    return { bias: 'NEUTRE', color: '#fcd34d', confidence: 50 };
  }

  /* ============================================================
     PUBLIC API
  ============================================================ */

  return {
    fetchBinance,
    fetchBackend,
    fetchAuto,
    runAll,
    syncToICTPanel,
    confluenceScore,
    getBias,
    detectSwings,
    detectFVG,
    detectOrderBlocks,
    detectLiquidity,
    detectBOS,
    detectHHHL,
    detectPD,
    getKillZones,
    getSessions,
    calcEMA,
    calcATR,
  };

})();