/**
 * smc_engine.js — Moteur de détection SMC/ICT automatique
 * Kengni Finance — v2.0
 * Placer dans : /static/js/smc_engine.js
 */
'use strict';

const SMCEngine = (() => {

  /* ═══════════════════════════════════════════════════════════════
     1. SWING POINTS — Détection ZigZag (pivots hauts/bas)
  ═══════════════════════════════════════════════════════════════ */
  function detectSwings(candles, leftBars = 5, rightBars = 5) {
    const swings = [];
    const lb = Math.max(2, Math.min(leftBars,  Math.floor(candles.length / 10)));
    const rb = Math.max(2, Math.min(rightBars, Math.floor(candles.length / 10)));

    for (let i = lb; i < candles.length - rb; i++) {
      let isHigh = true, isLow = true;
      for (let j = 1; j <= lb; j++) {
        if (candles[i-j].high >= candles[i].high) isHigh = false;
        if (candles[i-j].low  <= candles[i].low)  isLow  = false;
        if (!isHigh && !isLow) break;
      }
      for (let j = 1; j <= rb; j++) {
        if (candles[i+j].high > candles[i].high) isHigh = false;
        if (candles[i+j].low  < candles[i].low)  isLow  = false;
        if (!isHigh && !isLow) break;
      }
      if (isHigh) swings.push({ type:'high', price:candles[i].high, time:candles[i].time, index:i });
      if (isLow)  swings.push({ type:'low',  price:candles[i].low,  time:candles[i].time, index:i });
    }
    return swings.sort((a,b) => a.time - b.time);
  }

  /* ═══════════════════════════════════════════════════════════════
     2. MARKET STRUCTURE — HH / HL / LH / LL
  ═══════════════════════════════════════════════════════════════ */
  function detectMarketStructure(swings) {
    const result = [];
    const highs = swings.filter(s => s.type === 'high');
    const lows  = swings.filter(s => s.type === 'low');
    let lastH = null;
    for (const h of highs) {
      if (lastH) {
        const label = h.price > lastH.price ? 'HH' : 'LH';
        result.push({ ...h, label, color: label === 'HH' ? '#10b981' : '#f59e0b', isBullish: label === 'HH' });
      }
      lastH = h;
    }
    let lastL = null;
    for (const l of lows) {
      if (lastL) {
        const label = l.price > lastL.price ? 'HL' : 'LL';
        result.push({ ...l, label, color: label === 'HL' ? '#00d4aa' : '#ef4444', isBullish: label === 'HL' });
      }
      lastL = l;
    }
    return result.sort((a,b) => a.time - b.time);
  }

  /* ═══════════════════════════════════════════════════════════════
     3. BOS / CHoCH — Break of Structure / Change of Character
  ═══════════════════════════════════════════════════════════════ */
  function detectBOSCHoCH(candles, swings) {
    const events = [];
    const highs = swings.filter(s => s.type === 'high').sort((a,b) => a.time - b.time);
    const lows  = swings.filter(s => s.type === 'low').sort((a,b) => a.time - b.time);
    let trend = null;

    for (let i = 1; i < highs.length; i++) {
      const level = highs[i-1].price, t0 = highs[i-1].time, t1 = highs[i].time;
      for (const c of candles) {
        if (c.time <= t0 || c.time > t1) continue;
        if (c.close > level) {
          const isCHoCH = trend === 'bear';
          events.push({ type:isCHoCH?'CHoCH':'BOS', direction:'bullish', price:level, time:c.time, color:isCHoCH?'#a5b4fc':'#10b981' });
          trend = 'bull'; break;
        }
      }
    }
    for (let i = 1; i < lows.length; i++) {
      const level = lows[i-1].price, t0 = lows[i-1].time, t1 = lows[i].time;
      for (const c of candles) {
        if (c.time <= t0 || c.time > t1) continue;
        if (c.close < level) {
          const isCHoCH = trend === 'bull';
          events.push({ type:isCHoCH?'CHoCH':'BOS', direction:'bearish', price:level, time:c.time, color:isCHoCH?'#fcd34d':'#ef4444' });
          trend = 'bear'; break;
        }
      }
    }
    return events.sort((a,b) => a.time - b.time);
  }

  /* ═══════════════════════════════════════════════════════════════
     4. FAIR VALUE GAPS — FVG / Imbalances
  ═══════════════════════════════════════════════════════════════ */
  function detectFVG(candles, minPct = 0.0002) {
    const fvgs = [];
    for (let i = 2; i < candles.length; i++) {
      const p2 = candles[i-2], p1 = candles[i-1], c = candles[i];
      // Bullish FVG : gap entre p2.high et c.low
      if (c.low > p2.high) {
        const sz = c.low - p2.high;
        if (sz / p1.close >= minPct) {
          const fvg = { type:'bullish', top:c.low, bottom:p2.high, mid:(c.low+p2.high)/2, size:sz, time:p1.time, index:i, filled:false, fillTime:null, partialFill:false };
          for (let j = i+1; j < candles.length; j++) {
            if (candles[j].low <= fvg.mid) { fvg.filled = true; fvg.fillTime = candles[j].time; break; }
            if (candles[j].low <= fvg.top) fvg.partialFill = true;
          }
          fvgs.push(fvg);
        }
      }
      // Bearish FVG : gap entre p2.low et c.high
      if (c.high < p2.low) {
        const sz = p2.low - c.high;
        if (sz / p1.close >= minPct) {
          const fvg = { type:'bearish', top:p2.low, bottom:c.high, mid:(p2.low+c.high)/2, size:sz, time:p1.time, index:i, filled:false, fillTime:null, partialFill:false };
          for (let j = i+1; j < candles.length; j++) {
            if (candles[j].high >= fvg.mid) { fvg.filled = true; fvg.fillTime = candles[j].time; break; }
            if (candles[j].high >= fvg.bottom) fvg.partialFill = true;
          }
          fvgs.push(fvg);
        }
      }
    }
    return [...fvgs.filter(f=>!f.filled).slice(-25), ...fvgs.filter(f=>f.filled).slice(-8)].sort((a,b)=>a.time-b.time);
  }

  /* ═══════════════════════════════════════════════════════════════
     5. ORDER BLOCKS — Dernière bougie impulsive avant renversement
  ═══════════════════════════════════════════════════════════════ */
  function detectOrderBlocks(candles, swings) {
    const obs = [], seenIdx = new Set();
    for (let i = 2; i < candles.length - 4; i++) {
      const c = candles[i];
      // Bullish OB : dernière bougie baissière avant impulsion haussière
      if (c.close < c.open && !seenIdx.has(i)) {
        const impulse = candles.slice(i+1, Math.min(i+6, candles.length));
        const impulseHigh = Math.max(...impulse.map(x => x.high));
        const prevHigh = swings.filter(s => s.type==='high' && s.index < i).slice(-1)[0];
        if (prevHigh && impulseHigh > prevHigh.price) {
          const ob = _buildOB('bullish', c, i, candles);
          if (ob) { obs.push(ob); seenIdx.add(i); }
        }
      }
      // Bearish OB : dernière bougie haussière avant impulsion baissière
      if (c.close > c.open && !seenIdx.has(i)) {
        const impulse = candles.slice(i+1, Math.min(i+6, candles.length));
        const impulseLow = Math.min(...impulse.map(x => x.low));
        const prevLow = swings.filter(s => s.type==='low' && s.index < i).slice(-1)[0];
        if (prevLow && impulseLow < prevLow.price) {
          const ob = _buildOB('bearish', c, i, candles);
          if (ob) { obs.push(ob); seenIdx.add(i); }
        }
      }
    }
    return [...obs.filter(o=>o.status!=='mitigated').slice(-12), ...obs.filter(o=>o.status==='mitigated').slice(-4)].sort((a,b)=>a.time-b.time);
  }

  function _buildOB(type, c, idx, candles) {
    const ob = { type, high:c.high, low:c.low, open:c.open, close:c.close, time:c.time, index:idx, status:'fresh' };
    for (let j = idx+1; j < candles.length; j++) {
      const n = candles[j];
      if (type === 'bullish') {
        if (n.low <= ob.high && n.low >= ob.low) ob.status = 'tested';
        if (n.low < ob.low) { ob.status = 'mitigated'; break; }
      } else {
        if (n.high >= ob.low && n.high <= ob.high) ob.status = 'tested';
        if (n.high > ob.high) { ob.status = 'mitigated'; break; }
      }
    }
    return ob;
  }

  /* ═══════════════════════════════════════════════════════════════
     6. LIQUIDITY — Equal Highs (BSL) / Equal Lows (SSL)
  ═══════════════════════════════════════════════════════════════ */
  function detectLiquidity(candles, swings, tolerance = 0.0003) {
    const liq = [], seen = new Set();
    const highs = swings.filter(s => s.type === 'high');
    const lows  = swings.filter(s => s.type === 'low');

    for (let i = 0; i < highs.length - 1; i++) {
      for (let j = i+1; j < highs.length; j++) {
        const key = `bsl-${i}-${j}`;
        if (seen.has(key)) continue;
        if (Math.abs(highs[i].price - highs[j].price) / highs[i].price < tolerance) {
          const price = (highs[i].price + highs[j].price) / 2;
          let swept = false, sweepTime = null;
          for (const c of candles.filter(c => c.time > highs[j].time))
            if (c.high > price + price * 0.0001) { swept = true; sweepTime = c.time; break; }
          liq.push({ type:'BSL', price, t1:highs[i].time, t2:highs[j].time, swept, sweepTime });
          seen.add(key); break;
        }
      }
    }
    for (let i = 0; i < lows.length - 1; i++) {
      for (let j = i+1; j < lows.length; j++) {
        const key = `ssl-${i}-${j}`;
        if (seen.has(key)) continue;
        if (Math.abs(lows[i].price - lows[j].price) / lows[i].price < tolerance) {
          const price = (lows[i].price + lows[j].price) / 2;
          let swept = false, sweepTime = null;
          for (const c of candles.filter(c => c.time > lows[j].time))
            if (c.low < price - price * 0.0001) { swept = true; sweepTime = c.time; break; }
          liq.push({ type:'SSL', price, t1:lows[i].time, t2:lows[j].time, swept, sweepTime });
          seen.add(key); break;
        }
      }
    }
    return liq.slice(-20);
  }

  /* ═══════════════════════════════════════════════════════════════
     7. EMA — Exponential Moving Average
  ═══════════════════════════════════════════════════════════════ */
  function calcEMA(candles, period) {
    if (candles.length < period) return [];
    const k = 2 / (period + 1);
    let ema = candles.slice(0, period).reduce((s,c) => s + c.close, 0) / period;
    const result = [];
    for (let i = period; i < candles.length; i++) {
      ema = candles[i].close * k + ema * (1 - k);
      result.push({ time:candles[i].time, value:+ema.toFixed(8) });
    }
    return result;
  }

  /* ═══════════════════════════════════════════════════════════════
     8. PREMIUM / DISCOUNT — Zone 50% EQ
  ═══════════════════════════════════════════════════════════════ */
  function calcPremiumDiscount(candles, lookback = 100) {
    const slice = candles.slice(-lookback);
    if (!slice.length) return null;
    const high = Math.max(...slice.map(c => c.high));
    const low  = Math.min(...slice.map(c => c.low));
    const eq50 = (high + low) / 2;
    const current = candles[candles.length - 1].close;
    const pct = ((current - low) / (high - low)) * 100;
    return {
      high, low, eq50, current, pct,
      zone: pct > 60 ? 'PREMIUM' : pct < 40 ? 'DISCOUNT' : 'EQUILIBRIUM',
      bias: pct > 60 ? 'Short favorisé' : pct < 40 ? 'Long favorisé' : 'Neutre'
    };
  }

  /* ═══════════════════════════════════════════════════════════════
     MASTER RUN — Lance toutes les détections
  ═══════════════════════════════════════════════════════════════ */
  function runAll(candles) {
    if (!candles || candles.length < 20) return null;
    const lb = candles.length > 200 ? 5 : 3;
    const swings = detectSwings(candles, lb, lb);
    return {
      swings,
      ms:  detectMarketStructure(swings),
      bos: detectBOSCHoCH(candles, swings),
      fvg: detectFVG(candles),
      ob:  detectOrderBlocks(candles, swings),
      liq: detectLiquidity(candles, swings),
      pd:  calcPremiumDiscount(candles),
      ema: { ema20:calcEMA(candles,20), ema50:calcEMA(candles,50), ema200:calcEMA(candles,200) }
    };
  }

  /* ═══════════════════════════════════════════════════════════════
     DATA SOURCES — Binance, Backend Flask, Auto
  ═══════════════════════════════════════════════════════════════ */
  const TF_BINANCE = { '1m':'1m','5m':'5m','15m':'15m','1h':'1h','4h':'4h','1d':'1d' };

  async function fetchBinance(symbol, tf, limit = 500) {
    const url = `https://api.binance.com/api/v3/klines?symbol=${symbol.toUpperCase()}&interval=${TF_BINANCE[tf]||'1h'}&limit=${limit}`;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`Binance HTTP ${resp.status}`);
    const raw = await resp.json();
    if (!Array.isArray(raw)) throw new Error('Réponse Binance invalide');
    return raw.map(k => ({ time:Math.floor(k[0]/1000), open:+k[1], high:+k[2], low:+k[3], close:+k[4], volume:+k[5] }));
  }

  async function fetchBackend(symbol, tf, limit = 500) {
    const resp = await fetch(`/api/ohlc?symbol=${encodeURIComponent(symbol)}&tf=${tf}&limit=${limit}`);
    if (!resp.ok) throw new Error(`Backend HTTP ${resp.status}`);
    const data = await resp.json();
    if (data.error) throw new Error(data.error);
    return data.candles;
  }

  async function fetchAuto(symbol, tf, limit = 500) {
    const sym = symbol.toUpperCase();
    const isCrypto = /USDT$|BUSD$|BTC$|ETH$|BNB$/.test(sym);
    if (isCrypto) { try { return await fetchBinance(sym, tf, limit); } catch(e) {} }
    try { return await fetchBackend(sym, tf, limit); } catch(e) {}
    return null;
  }

  /* ═══════════════════════════════════════════════════════════════
     PUBLIC API
  ═══════════════════════════════════════════════════════════════ */
  return {
    detectSwings, detectMarketStructure, detectBOSCHoCH,
    detectFVG, detectOrderBlocks, detectLiquidity,
    calcEMA, calcPremiumDiscount, runAll,
    fetchBinance, fetchBackend, fetchAuto
  };
})();

if (typeof module !== 'undefined') module.exports = SMCEngine;