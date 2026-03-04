"""
smc_routes.py — Blueprint Flask pour le module SMC Auto-Détection
Kengni Finance v2.0

INSTALLATION :
    1. pip install yfinance
    2. Dans votre app.py :
          from smc_routes import smc_bp
          app.register_blueprint(smc_bp)
"""

from flask import Blueprint, jsonify, request
import yfinance as yf
import traceback

smc_bp = Blueprint('smc', __name__)

# ── Correspondances symbole → format yfinance ──────────────────────────────
SYMBOL_MAP = {
    # Forex
    'EURUSD': 'EURUSD=X', 'GBPUSD': 'GBPUSD=X', 'USDJPY': 'USDJPY=X',
    'USDCHF': 'USDCHF=X', 'AUDUSD': 'AUDUSD=X', 'NZDUSD': 'NZDUSD=X',
    'USDCAD': 'USDCAD=X', 'EURGBP': 'EURGBP=X', 'EURJPY': 'EURJPY=X',
    'GBPJPY': 'GBPJPY=X', 'XAUUSD': 'GC=F',    'XAGUSD': 'SI=F',
    # Indices
    'SPX': '^GSPC', 'US500': '^GSPC', 'NAS100': '^NDX', 'NASDAQ': '^NDX',
    'DOW': '^DJI',  'DJI': '^DJI',   'DAX': '^GDAXI', 'FTSE': '^FTSE',
    'US30': '^DJI', 'NDX': '^NDX',
    # Crypto via yfinance (fallback si Binance indisponible)
    'BTCUSD': 'BTC-USD', 'ETHUSD': 'ETH-USD', 'BNBUSD': 'BNB-USD',
    'SOLUSD': 'SOL-USD', 'ADAUSD': 'ADA-USD', 'XRPUSD': 'XRP-USD',
}

# ── Correspondances timeframe → paramètres yfinance ───────────────────────
TF_MAP = {
    '1m':  ('1m',   '1d'),
    '5m':  ('5m',   '5d'),
    '15m': ('15m',  '15d'),
    '1h':  ('1h',   '60d'),
    '4h':  ('1h',   '60d'),   # on rééchantillonne 1h → 4h côté client
    '1d':  ('1d',   '2y'),
}


def _normalize_symbol(sym: str) -> str:
    sym = sym.upper().strip()
    if sym in SYMBOL_MAP:
        return SYMBOL_MAP[sym]
    if '/' in sym:
        sym = sym.replace('/', '')
    if sym.endswith('USD') and not sym.endswith('-USD') and len(sym) > 6:
        return sym[:-3] + '-USD'
    return sym


def _resample_4h(candles: list) -> list:
    """Rééchantillonne des bougies 1h → 4h."""
    if not candles:
        return []
    groups, current = [], None
    for c in candles:
        slot = (c['time'] // 14400) * 14400
        if current is None or slot != current['_slot']:
            if current:
                groups.append({'time': current['_slot'], 'open': current['open'],
                               'high': current['high'], 'low': current['low'],
                               'close': current['close'], 'volume': current['volume']})
            current = {'_slot': slot, 'open': c['open'], 'high': c['high'],
                       'low': c['low'], 'close': c['close'], 'volume': c['volume']}
        else:
            current['high']   = max(current['high'], c['high'])
            current['low']    = min(current['low'],  c['low'])
            current['close']  = c['close']
            current['volume'] += c['volume']
    if current:
        groups.append({'time': current['_slot'], 'open': current['open'],
                       'high': current['high'], 'low': current['low'],
                       'close': current['close'], 'volume': current['volume']})
    return groups


# ══════════════════════════════════════════════════════════════════════════════
# ROUTE 1 : /api/ohlc — données OHLC via yfinance
# ══════════════════════════════════════════════════════════════════════════════
@smc_bp.route('/api/ohlc')
def get_ohlc():
    """
    Paramètres GET :
        symbol : ex. EURUSD, BTCUSD, SPX, AAPL
        tf     : 1m | 5m | 15m | 1h | 4h | 1d  (défaut : 1h)
        limit  : nombre de bougies max (défaut : 500)
    Retour :
        { symbol, tf, candles: [{time, open, high, low, close, volume}] }
    """
    symbol = request.args.get('symbol', 'EURUSD').strip()
    tf     = request.args.get('tf', '1h').strip()
    limit  = min(int(request.args.get('limit', 500)), 1000)

    if tf not in TF_MAP:
        return jsonify({'error': f'Timeframe invalide : {tf}. Valeurs : 1m 5m 15m 1h 4h 1d'}), 400

    yfSym = _normalize_symbol(symbol)
    interval, period = TF_MAP[tf]

    try:
        ticker = yf.Ticker(yfSym)
        df = ticker.history(period=period, interval=interval, auto_adjust=True)
        if df is None or df.empty:
            return jsonify({'error': f'Aucune donnée pour {symbol} ({yfSym})'}), 404

        candles = []
        for ts, row in df.iterrows():
            candles.append({
                'time':   int(ts.timestamp()),
                'open':   round(float(row['Open']),   8),
                'high':   round(float(row['High']),   8),
                'low':    round(float(row['Low']),    8),
                'close':  round(float(row['Close']),  8),
                'volume': round(float(row.get('Volume', 0)), 2),
            })

        # Rééchantillonnage 4H
        if tf == '4h':
            candles = _resample_4h(candles)

        # Limite
        candles = candles[-limit:]

        return jsonify({'symbol': symbol, 'yfSymbol': yfSym, 'tf': tf, 'count': len(candles), 'candles': candles})

    except Exception:
        return jsonify({'error': traceback.format_exc()}), 500


# ══════════════════════════════════════════════════════════════════════════════
# ROUTE 2 : /api/smc/analyze — Analyse SMC côté serveur (optionnelle)
# ══════════════════════════════════════════════════════════════════════════════
@smc_bp.route('/api/smc/analyze', methods=['POST'])
def analyze_smc():
    """
    Corps JSON : { candles: [...] }
    Effectue l'analyse SMC côté serveur (alternative Python si besoin).
    En pratique, l'analyse est faite en JS côté client — cette route est
    disponible pour des usages avancés (backtesting, alertes, etc.).
    """
    try:
        data = request.get_json(force=True)
        candles = data.get('candles', [])
        if len(candles) < 20:
            return jsonify({'error': 'Minimum 20 bougies requises'}), 400

        # Statistiques basiques sans dépendance externe
        highs  = [c['high']  for c in candles]
        lows   = [c['low']   for c in candles]
        closes = [c['close'] for c in candles]
        vols   = [c.get('volume', 0) for c in candles]

        last   = candles[-1]
        rng100 = max(highs[-100:]) - min(lows[-100:]) if len(candles) >= 100 else max(highs) - min(lows)
        eq50   = (max(highs[-100:]) + min(lows[-100:])) / 2 if len(candles) >= 100 else (max(highs) + min(lows)) / 2
        pct    = ((last['close'] - min(lows[-100:])) / rng100 * 100) if rng100 else 50

        return jsonify({
            'symbol': data.get('symbol', '?'),
            'tf':     data.get('tf', '?'),
            'bars':   len(candles),
            'summary': {
                'lastClose':   last['close'],
                'rangeHigh':   max(highs[-100:]),
                'rangeLow':    min(lows[-100:]),
                'eq50':        round(eq50, 8),
                'pdPct':       round(pct, 1),
                'zone':        'PREMIUM' if pct > 60 else 'DISCOUNT' if pct < 40 else 'EQUILIBRIUM',
                'avgVolume':   round(sum(vols) / len(vols), 2) if any(vols) else 0,
                'priceChange': round((last['close'] - candles[0]['close']) / candles[0]['close'] * 100, 2),
            }
        })
    except Exception:
        return jsonify({'error': traceback.format_exc()}), 500