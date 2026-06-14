import streamlit as st
import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ================================================================
#  NO BR NO PARTY SCANNER - COMPLETE & DEBUGGED EDITION
# ================================================================

BYBIT_444_DATABASE = {
    "Core L1": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOTUSDT", "LTCUSDT", "TRXUSDT", "ATOMUSDT", "XLMUSDT", "ETCUSDT", "VETUSDT", "XMRUSDT", "NEOUSDT", "ZECUSDT", "DASHUSDT", "XTZUSDT", "QTUMUSDT", "WAVESUSDT", "ICXUSDT"],
    "AI & DePIN": ["TAOUSDT", "RENDERUSDT", "INJUSDT", "GRASSUSDT", "VIRTUALUSDT", "THETAUSDT", "PYTHUSDT", "AKTUSDT", "AIOZUSDT", "AIXBTUSDT", "ZEREBROUSDT", "0GUSDT", "AGIUSDT", "GLMUSDT", "PHAUSDT", "ARKMUSDT", "UAIUSDT", "COAIUSDT", "GOATUSDT"],
    "New L1": ["SUIUSDT", "APTUSDT", "SEIUSDT", "ICPUSDT", "MINAUSDT", "BERAUSDT", "HYPEUSDT", "KASUSDT", "FLOWUSDT", "FLRUSDT", "XIONUSDT", "PEAQUSDT", "ALCHUSDT", "ONTUSDT", "ONGUSDT", "SAGAUSDT", "ASTRUSDT"],
    "L2 & Scaling": ["ARBUSDT", "OPUSDT", "STRKUSDT", "MATICUSDT", "POLUSDT", "METISUSDT", "MANTAUSDT", "BLASTUSDT", "ZETAUSDT", "TAIKOUSDT", "CELOUSDT", "STXUSDT", "ZKUSDT", "ZROUSDT", "AXLUSDT", "WUSDT", "LINEAUSDT", "MOVEUSDT", "DYMUSDT", "SCRTUSDT", "BOBAUSDT", "VANRYUSDT", "LUMIAUSDT"],
    "DeFi & Restaking": ["AAVEUSDT", "PENDLEUSDT", "EIGENUSDT", "ENAUSDT", "UNIUSDT", "CRVUSDT", "COMPUSDT", "SUSHIUSDT", "1INCHUSDT", "RUNEUSDT", "CAKEUSDT", "YFIUSDT", "CVXUSDT", "LDOUSDT", "JTOUSDT", "RAYDIUMUSDT", "ORCAUSDT", "CETUSUSDT", "VELODROMEUSDT", "AEROUSDT", "COTIUSDT", "LQTYUSDT", "DYDXUSDT", "API3USDT", "XVSUSDT", "AUCTIONUSDT", "KMNOUSDT", "SOLVUSDT", "USUALUSDT", "DEEPUSDT"],
    "Meme Coins": ["DOGEUSDT", "1000PEPEUSDT", "SHIB1000USDT", "WIFUSDT", "1000BONKUSDT", "POPCATUSDT", "PNUTUSDT", "MEWUSDT", "DEGENUSDT", "BOMEUSDT", "SPXUSDT", "CHILLGUYUSDT", "1000FLOKIUSDT", "1000TURBOUSDT", "10000SATSUSDT", "1000CATUSDT", "1000000MOGUSDT", "1000NEIROCTOUSDT", "MEMEUSDT", "MOODENGUSDT", "TRUMPUSDT", "MELANIAUSDT", "1000000CHEEMSUSDT", "1000000BABYDOGEUSDT", "BABYUSDT", "1000TOSHIUSDT"],
    "RWA": ["ONDOUSDT", "XAUTUSDT", "PAXGUSDT", "CFGUSDT", "OMUSDT", "TRIAUSDT", "ACUUSDT", "STOUSDT", "XAUUSDT", "XAGUSDT"],
    "Gaming & Meta": ["IMXUSDT", "GALAUSDT", "SANDUSDT", "MANAUSDT", "AXSUSDT", "YGGUSDT", "PIXELUSDT", "BIGTIMEUSDT", "PORTALUSDT", "BEAMUSDT", "MAGICUSDT", "ENJUSDT", "BLURUSDT", "MAVIAUSDT", "AGLDUSDT", "SUPERUSDT", "RONINUSDT", "MOCAUSDT"],
    "Web3 Infra": ["FILUSDT", "ARUSDT", "STORJUSDT", "GRTUSDT", "LINKUSDT", "TIAUSDT", "CKBUSDT", "ANKRUSDT", "HBARUSDT", "DIAUSDT", "RLCUSDT", "SYSUSDT", "GLMUSDT", "LPTUSDT", "JASMYUSDT", "IOTXUSDT", "QNTUSDT", "WOOUSDT", "MASKUSDT"],
    "Emerging & New": ["RAVEUSDT", "AKEUSDT", "TNSRUSDT", "SIRENUSDT", "NOMUSDT", "MAGMAUSDT", "NAORISUSDT", "ARCUSDT", "PARTIUSDT", "EVAAUSDT", "SAPIENUSDT", "VVVUSDT", "PTBUSDT", "HUMAUSDT", "MORPHOUSDT", "LABUSDT", "SWARMSUSDT", "SPORTFUNUSDT", "SHELLUSDT", "BOBBOBUSDT", "ZBTUSDT", "AVAAIUSDT", "LIGHTUSDT", "BLESSUSDT", "SAFEUSDT", "IRYSUSDT", "USELESSUSDT", "HFTUSDT", "NOTUSDT", "ENSOUSDT", "REZUSDT", "RSRUSDT", "NIGHTUSDT", "SOSOUSDT", "GPSUSDT", "IPUSDT", "EDUUSDT", "ETHFIUSDT", "COOKIEUSDT", "PENGUUSDT", "ERAUSDT", "ALPINEUSDT", "PROVEUSDT", "WHITEWHALEUSALEUSDT", "TACUSDT", "ZKCUSDT", "1000TAGUSDT", "ENSUSDT", "SOMIUSDT", "TRUSTUSDT", "KAIAUSDT", "LISTAUSDT", "SQDUSDT", "VINEUSDT", "AZTECUSDT", "BSUUSDT", "MYXUSDT", "ZAMAUSDT", "PROMPTUSDT", "EIGENUSDT", "TWTUSDT", "CLUSDT", "BANANAUSDT", "MIRAUSDT", "XCNUSDT", "ASTERUSDT", "ACHUSDT", "AUSDT", "B3USDT", "SNTUSDT", "SAHARAUSDT", "RPLUSDT", "BIOUSDT", "YBUSDT", "SKYUSDT", "ASRUSDT", "LSKUSDT", "NEWTUSDT", "SUNUSDT", "JELLYJELLYUSDT", "MTLUSDT", "1000BTTUSDT", "THEUSDT", "STGUSDT", "OGUSDT", "CTCUSDT", "HEIUSDT", "MAVUSDT", "ROBOUSDT", "DOLOUSDT", "OKBUSDT", "LAUSDT", "PRLUSDT", "KSMUSDT", "PUNDIXUSDT", "COWUSDT", "RVNUSDT", "XAIUSDT", "HPOS10IUSDT", "CVCUSDT", "LPTUSDT", "VANAUSDT", "ZILUSDT", "HIGHUSDT", "SUSDT", "VELVETUSDT", "USD1USDT", "SENTUSDT", "PLUMEUSDT", "IOUSDT", "HOMEUSDT", "USDEUSDT", "GODSUSDT", "TUSDT", "ANKRUSDT", "USDCUSDT", "JCTUSDT", "RLUSDUSDT", "BANKUSDT", "1000XECUSDT", "AERGOUSDT", "WLFIUSDT", "POLYXUSDT", "CROUSDT", "STEEMUSDT", "HANAUSDT", "FLUXUSDT", "STBLUSDT", "WALUSDT", "MUBARAKUSDT", "BTRUSDT", "YZYUSDT", "ANIMEUSDT", "XDCUSDT", "METUSDT", "EDGEUSDT", "FLUIDUSDT", "XPLUSDT", "HAEDALUSDT", "PYRUSDT", "BROCCOLIUSDT", "HMSTRUSDT", "MOCAUSDT", "MAGICUSDT", "ESUSDT", "FFUSDT", "SSVUSDT", "WAXPUSDT", "SOPHUSDT", "FUSDT", "ORBSUSDT", "ORDERUSDT", "NXPCUSDT", "SPKUSDT", "BATUSDT", "ASPUSDT", "GRIFFINUSDT", "GUNUSDT", "FLOCKUSDT", "UMAUSDT", "ACXUSDT", "KATUSDT", "MITOUSDT", "ESPUSDT", "BNTUSDT", "BELUSDT", "MMTUSDT", "APEXUSDT", "USTCUSDT", "HEMIUSDT", "WCTUSDT", "SONICUSDT", "CROSSUSDT", "OLUSDT", "FORMUSDT", "ZORAUSDT", "WETUSDT", "ALLOUSDT"]
}

YOUHODLER_LIST = [
    "BTCUSDT", "ETHUSDT", "BCHUSDT", "BNBUSDT", "DASHUSDT", "EOSUSDT", "LTCUSDT", "XLMUSDT",
    "XRPUSDT", "DOTUSDT", "XTZUSDT", "SOLUSDT", "TRXUSDT", "ADAUSDT", "DOGEUSDT",
    "ATOMUSDT", "AVAXUSDT", "FILUSDT", "CAKEUSDT", "NEARUSDT", "EGLDUSDT", "ZILUSDT", "GMTUSDT",
    "BATUSDT", "COMPUSDT", "LINKUSDT", "MKRUSDT", "SNXUSDT", "UNIUSDT", "YFIUSDT", "1INCHUSDT",
    "BNTUSDT", "OMGUSDT", "PAXGUSDT", "REPUSDT", "SUSHIUSDT", "ZRXUSDT", "AAVEUSDT",
    "MANAUSDT", "SANDUSDT", "AXSUSDT", "ILVUSDT", "GALAUSDT", "APEUSDT",
    "1000PEPEUSDT", "SHIB1000USDT", "TONUSDT", "LISTAUSDT"
]
BYBIT_444_DATABASE["YouHodler List"] = YOUHODLER_LIST

ALL_TICKERS = sorted(set(t for sub in BYBIT_444_DATABASE.values() for t in sub))
TIMEFRAMES = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "1d"]

if "scan_rows" not in st.session_state:
    st.session_state.scan_rows = pd.DataFrame()
if "scan_cache" not in st.session_state:
    st.session_state.scan_cache = {}

@st.cache_resource
def get_exchange_client():
    exchange = ccxt.bybit({'enableRateLimit': True, 'options': {'defaultType': 'swap'}})
    try:
        exchange.load_markets()
    except Exception:
        pass
    return exchange

bybit = get_exchange_client()

def clean_ticker_for_api(t: str):
    base_name = t.upper().replace("USDT", "").strip()
    no_prefix = base_name
    for prefix in ["1000000", "100000", "10000", "1000"]:
        if no_prefix.startswith(prefix):
            no_prefix = no_prefix.replace(prefix, "", 1)
            break
    return [
        f"{base_name}USDT", f"{base_name}/USDT", f"{base_name}/USDT:USDT", f"{t}:USDT",
        f"{no_prefix}/USDT", f"{no_prefix}/USDT:USDT", f"1000{no_prefix}/USDT:USDT"
    ]

def fetch_ohlcv_safe(display_ticker: str, timeframe: str, limit: int = 260):
    for symbol in clean_ticker_for_api(display_ticker):
        try:
            candles = bybit.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            if candles and len(candles) > 80:
                df = pd.DataFrame(candles, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
                df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms")
                return df, symbol
        except Exception:
            continue
    return None, None

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["EMA5"] = df["Close"].ewm(span=5, adjust=False).mean()
    df["EMA10"] = df["Close"].ewm(span=10, adjust=False).mean()
    df["EMA60"] = df["Close"].ewm(span=60, adjust=False).mean()
    df["EMA223"] = df["Close"].ewm(span=223, adjust=False).mean()

    typical = (df["High"] + df["Low"] + df["Close"]) / 3
    pv = typical * df["Volume"]
    df["VWAP"] = pv.rolling(21, min_periods=3).sum() / df["Volume"].rolling(21, min_periods=3).sum().replace(0, np.nan)
    df["MVWAP"] = df["VWAP"].ewm(span=21, adjust=False).mean()

    df["VolMedia20"] = df["Volume"].rolling(20, min_periods=5).mean()
    df["VolX"] = df["Volume"] / df["VolMedia20"].replace(0, np.nan)

    prev_close = df["Close"].shift(1)
    tr = pd.concat([df["High"] - df["Low"], (df["High"] - prev_close).abs(), (df["Low"] - prev_close).abs()], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14, min_periods=5).mean()
    return df

def _confirmed_pivots(series: pd.Series, left: int, right: int, mode: str):
    vals = series.to_numpy(dtype=float)
    pivots = []
    n = len(vals)
    for center in range(left, n - right):
        window = vals[center-left:center+right+1]
        val = vals[center]
        if mode == "high" and np.isfinite(val) and val == np.nanmax(window):
            pivots.append({"center": center, "confirmed_at": center + right, "value": float(val)})
        elif mode == "low" and np.isfinite(val) and val == np.nanmin(window):
            pivots.append({"center": center, "confirmed_at": center + right, "value": float(val)})
    return pivots

def pine_style_levels(df: pd.DataFrame, left: int = 50, right: int = 25, quick_right: int = 5):
    quick_highs = _confirmed_pivots(df["High"], left, quick_right, "high")
    quick_lows = _confirmed_pivots(df["Low"], left, quick_right, "low")
    main_highs = _confirmed_pivots(df["High"], left, right, "high")
    main_lows = _confirmed_pivots(df["Low"], left, right, "low")

    levels = []
    if quick_highs: levels.append({"name": "Resistenza veloce", "kind": "res", "power": "B", "value": quick_highs[-1]["value"]})
    if quick_lows: levels.append({"name": "Supporto veloce", "kind": "sup", "power": "B", "value": quick_lows[-1]["value"]})
    for idx, p in enumerate(main_highs[-3:][::-1], start=1):
        levels.append({"name": f"Resistenza seria {idx}", "kind": "res", "power": "A", "value": p["value"]})
    for idx, p in enumerate(main_lows[-3:][::-1], start=1):
        levels.append({"name": f"Supporto serio {idx}", "kind": "sup", "power": "A", "value": p["value"]})

    unique = []
    for lvl in sorted(levels, key=lambda x: x["value"]):
        if not any(abs(lvl["value"] - u["value"]) / max(lvl["value"], 1e-12) < 0.0015 and lvl["kind"] == u["kind"] for u in unique):
            unique.append(lvl)
    return unique

def analyze_br(df: pd.DataFrame, ticker: str, timeframe: str, volume_hot: float, distance_watch: float, retest_tol: float, require_breakout: bool = True, direction: str = "LONG"):
    if len(df) > 120:
        df = df.iloc[:-1].copy()

    direction = (direction or "LONG").upper()
    is_short = direction == "SHORT"

    df = add_indicators(df)
    levels = pine_style_levels(df)
    if df.empty:
        return None, df, levels

    last = df.iloc[-1]
    prev = df.iloc[-2]
    price = float(last["Close"])
    atr = float(last.get("ATR", np.nan) or 0)
    volx = float(last.get("VolX", np.nan) or 0)

    resistance_levels = [l for l in levels if l["kind"] == "res" and np.isfinite(l["value"])]
    support_levels = [l for l in levels if l["kind"] == "sup" and np.isfinite(l["value"])]

    breakout_levels = support_levels if is_short else resistance_levels
    if not breakout_levels:
        return None, df, levels

    broken = []
    for lvl in breakout_levels:
        value = lvl["value"]
        if is_short and prev["Close"] >= value > price: broken.append(lvl)
        elif not is_short and prev["Close"] <= value < price: broken.append(lvl)
    broken = sorted(broken, key=lambda x: (x["power"] == "A", x["value"]), reverse=not is_short)

    if is_short:
        near_levels = sorted([l for l in breakout_levels if l["value"] < price], key=lambda x: price - x["value"])
    else:
        near_levels = sorted([l for l in breakout_levels if l["value"] > price], key=lambda x: x["value"] - price)
    nearest_level = near_levels[0] if near_levels else None

    retest_ok, just_breakout, distance_pct = False, False, None
    br_level, br_name, level_power = None, "", ""

    if broken:
        just_breakout = True
        chosen = broken[0]
        br_level = chosen["value"]
        br_name = chosen["name"]
        level_power = chosen["power"]
        recent = df.tail(6)
        tolerance = max(retest_tol / 100, (atr / price) * 0.35 if price else 0)
        if is_short:
            retest_ok = bool(((recent["High"] >= br_level * (1 - tolerance)) & (recent["Close"] < br_level)).any())
        else:
            retest_ok = bool(((recent["Low"] <= br_level * (1 + tolerance)) & (recent["Close"] > br_level)).any())
        distance_pct = 0.0
    elif nearest_level:
        br_level = nearest_level["value"]
        br_name = nearest_level["name"]
        level_power = nearest_level["power"]
        distance_pct = ((price - br_level) / price) * 100 if is_short else ((br_level - price) / price) * 100

    if require_breakout and not just_breakout:
        return None, df, levels

    vwap_ok = bool(price < last["VWAP"] and price < last["MVWAP"]) if is_short else bool(price > last["VWAP"] and price > last["MVWAP"]) if np.isfinite(last["VWAP"]) else False
    ema_fast_ok = bool(last["EMA5"] < last["EMA10"] < last["EMA60"]) if is_short else bool(last["EMA5"] > last["EMA10"] > last["EMA60"]) if np.isfinite(last["EMA60"]) else False
    ema_big_ok = bool(last["EMA60"] < last["EMA223"]) if is_short else bool(last["EMA60"] > last["EMA223"]) if np.isfinite(last["EMA223"]) else False
    volume_ok = volx >= volume_hot
    volume_warming = volx >= max(1.25, volume_hot * 0.70)
    candle_ok = bool(last["Close"] < last["Open"]) if is_short else bool(last["Close"] > last["Open"])

    score = 0
    why = []
    if just_breakout:
        score += 35 if level_power == "A" else 25
        why.append(f"{'BS' if is_short else 'BR'} fatto su {br_name}")
    if retest_ok: score += 20; why.append("retest ok")
    if volume_ok: score += 18; why.append("volume bomba")
    elif volume_warming: score += 10; why.append("volume sale")
    if vwap_ok: score += 10; why.append("sotto VWAP" if is_short else "sopra VWAP")
    if ema_fast_ok: score += 10; why.append("EMA short ok" if is_short else "EMA long ok")
    if ema_big_ok: score += 4
    if candle_ok: score += 3

    score = int(min(score, 100))
    party_meter = int(round(score / 10))
    word = "SHORT" if is_short else "LONG"
    break_word = "SUPPORTO ROTTO" if is_short else "BREAK"

    if just_breakout and not volume_warming:
        score, party_meter = min(score, 44), int(round(min(score, 44) / 10))
        situation, tempo = f"😴 {break_word} MA SENZA VOLUME - NO {word}", "💤 Aspetta"
    elif just_breakout and (not vwap_ok or not ema_fast_ok):
        score, party_meter = min(score, 49), int(round(min(score, 49) / 10))
        situation, tempo = f"⚠️ {break_word} SPORCO - NO {word}", "🕐 Serve conferma"
    elif just_breakout and volume_ok and vwap_ok and ema_fast_ok and score >= 82:
        situation, tempo = f"🚀 {word} CONFERMATO", "🔥 Adesso"
    elif just_breakout and volume_warming and vwap_ok and ema_fast_ok and score >= 65:
        situation, tempo = f"🟢 {word} VALIDO", "🔥 Adesso"
    elif just_breakout and retest_ok and volume_warming:
        situation, tempo = f"✅ {word} + RETEST", "⏳ Conferma fresca"
    elif just_breakout and score >= 45:
        situation, tempo = f"☕ {word} DEBOLE - NO {word}", "🕐 Serve qualità"
    elif volx < 0.8:
        situation, tempo = f"😴 {word} SENZA SPINTA", "💤 Lenta"
    else:
        situation, tempo = f"🚽 {word} NON INTERESSANTE", "💤 Ignora"

    entry = price
    if is_short:
        nearest_res_above = sorted([r for r in resistance_levels if r["value"] > price], key=lambda x: x["value"] - price)
        sl = max(nearest_res_above[0]["value"], br_level if br_level else price) + max(atr * 0.20, price * 0.001) if nearest_res_above else (br_level + max(atr * 0.50, price * 0.002) if br_level else price + max(atr * 1.2, price * 0.006))
        risk = max(sl - entry, price * 0.002)
        tp1, tp2 = entry - risk * 1.5, entry - risk * 2.5
    else:
        nearest_support_below = sorted([s for s in support_levels if s["value"] < price], key=lambda x: price - x["value"])
        sl = min(nearest_support_below[0]["value"], br_level if br_level else price) - max(atr * 0.20, price * 0.001) if nearest_support_below else (br_level - max(atr * 0.50, price * 0.002) if br_level else price - max(atr * 1.2, price * 0.006))
        risk = max(entry - sl, price * 0.002)
        tp1, tp2 = entry + risk * 1.5, entry + risk * 2.5

    nearest_res_for_info = sorted([r for r in resistance_levels if r["value"] >= price], key=lambda x: x["value"] - price)
    nearest_sup_for_info = sorted([s for s in support_levels if s["value"] <= price], key=lambda x: price - x["value"])
    res_info = nearest_res_for_info[0]["value"] if nearest_res_for_info else (resistance_levels[-1]["value"] if resistance_levels else np.nan)
    sup_info = nearest_sup_for_info[0]["value"] if nearest_sup_for_info else (support_levels[-1]["value"] if support_levels else np.nan)
    zone_w = max(atr * 0.35, price * 0.0015) if price else 0
    phrase = "📉 Se perde " + format_level(br_level) + " può scendere" if is_short else "🚀 Se rompe " + format_level(br_level) + " può volare"

    return {
        "TradingView": f"https://www.tradingview.com/chart/?symbol=BYBIT:{ticker}.P", "Ticker": ticker, "Direzione": word, "Situazione": situation,
        "Party Meter": party_meter, "BR Score": score, "Timeframe": timeframe, "Distanza dal PARTY %": round(distance_pct, 3) if distance_pct is not None else np.nan,
        "Volume Booster": round(volx, 2), "Livello BR": br_level, "Tipo Livello": "SERIO" if level_power == "A" else "VELOCE", "Break Obbligatorio": "✅",
        "Entry": entry, "SL": sl, "TP1": tp1, "TP2": tp2, "VWAP OK": "✅" if vwap_ok else "❌", "EMA OK": "✅" if ema_fast_ok else "❌",
        "Perché": ", ".join(why) if why else "niente di speciale", "Frase Dummies": phrase, "Resistenza Vicina": res_info, "Supporto Vicino": sup_info, "Supply Zone": level_zone_text(res_info, zone_w), "Demand Zone": level_zone_text(sup_info, zone_w), "Tempo": tempo
    }, df, levels


def format_level(v):
    try:
        return f"{float(v):.6g}"
    except Exception:
        return "N/A"

def build_break_phrase(row):
    direction = str(row.get("Direzione", "LONG")).upper()
    lvl = row.get("Livello BR", np.nan)
    if pd.isna(lvl):
        return "Nessun livello chiave trovato"
    lvl_txt = format_level(lvl)
    situation = str(row.get("Situazione", "")).upper()
    if direction == "SHORT":
        if "CONFERMATO" in situation or "VALIDO" in situation:
            return f"⚡ Ha perso {lvl_txt}: può scendere"
        return f"📉 Se perde {lvl_txt} può scendere"
    else:
        if "CONFERMATO" in situation or "VALIDO" in situation:
            return f"⚡ Ha rotto {lvl_txt}: può volare"
        return f"🚀 Se rompe {lvl_txt} può volare"

def level_zone_text(center, width):
    if center is None or pd.isna(center):
        return "N/A"
    lo = float(center) - float(width)
    hi = float(center) + float(width)
    return f"{format_level(lo)} - {format_level(hi)}"




def draw_chart(df: pd.DataFrame, ticker: str, levels, row):
    """
    V7 - Grafico TradingView pulito:
    - Prezzo
    - VWAP
    - EMA 60
    - una Supply principale
    - una Demand principale
    - BREAK / Entry / Stop / TP1 / TP2 con frecce leggibili
    - Volumi verdi e rossi
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.035,
        row_heights=[0.78, 0.22]
    )

    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Prezzo",
            increasing_line_color="#00E676",
            decreasing_line_color="#FF4B4B",
            increasing_fillcolor="#00E676",
            decreasing_fillcolor="#FF4B4B",
            line=dict(width=1.1),
        ),
        row=1, col=1
    )

    # Solo 2 guide: VWAP + EMA60
    if "VWAP" in df:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["VWAP"],
                name="VWAP",
                line=dict(width=2.0, color="#38BDF8")
            ),
            row=1, col=1
        )

    if "EMA60" in df:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["EMA60"],
                name="EMA 60",
                line=dict(width=2.0, color="#A855F7")
            ),
            row=1, col=1
        )

    price = float(df["Close"].iloc[-1])
    atr_last = float(df["ATR"].iloc[-1]) if "ATR" in df and pd.notna(df["ATR"].iloc[-1]) else price * 0.004
    zone_w = max(atr_last * 0.22, price * 0.001)

    resistance_levels = sorted([l for l in levels if l.get("kind") == "res"], key=lambda x: x["value"])
    support_levels = sorted([l for l in levels if l.get("kind") == "sup"], key=lambda x: x["value"], reverse=True)

    res_above = [l for l in resistance_levels if l["value"] >= price]
    sup_below = [l for l in support_levels if l["value"] <= price]

    main_res = res_above[0]["value"] if res_above else (resistance_levels[-1]["value"] if resistance_levels else np.nan)
    main_sup = sup_below[0]["value"] if sup_below else (support_levels[0]["value"] if support_levels else np.nan)

    # Evita etichette tutte appiccicate: posizione sinistra fissa
    label_x = df["Date"].iloc[max(1, int(len(df) * 0.08))]

    def add_hline_clean(y, color, dash="dash", width=1.8):
        if pd.isna(y):
            return
        fig.add_hline(
            y=float(y),
            line_color=color,
            line_dash=dash,
            line_width=width,
            row=1,
            col=1
        )

    def label_left(y, text, color, ay=0):
        if pd.isna(y):
            return
        fig.add_annotation(
            x=label_x,
            y=float(y),
            text=text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=color,
            ax=-45,
            ay=ay,
            font=dict(size=12, color="#FFFFFF"),
            bgcolor=color,
            bordercolor=color,
            borderwidth=1,
            borderpad=5,
            opacity=0.96,
            row=1,
            col=1
        )

    # Supply / Demand principali
    if st.session_state.get("ui_show_zones", True):
        if not pd.isna(main_res):
            fig.add_hrect(
                y0=float(main_res) - zone_w,
                y1=float(main_res) + zone_w,
                fillcolor="rgba(255,75,75,0.16)",
                line_width=0,
                row=1, col=1
            )
            add_hline_clean(main_res, "#FF4B4B", "dash", 1.8)
            label_left(main_res, f"🔴 SUPPLY {format_level(main_res)}", "#7F1D1D", -8)

        if not pd.isna(main_sup):
            fig.add_hrect(
                y0=float(main_sup) - zone_w,
                y1=float(main_sup) + zone_w,
                fillcolor="rgba(0,230,118,0.14)",
                line_width=0,
                row=1, col=1
            )
            add_hline_clean(main_sup, "#00E676", "dash", 1.8)
            label_left(main_sup, f"🟢 DEMAND {format_level(main_sup)}", "#064E3B", 8)

    entry = row.get("Entry", np.nan)
    sl = row.get("SL", np.nan)
    tp1 = row.get("TP1", np.nan)
    tp2 = row.get("TP2", np.nan)
    br = row.get("Livello BR", np.nan)

    # Livelli operativi
    add_hline_clean(br, "#FACC15", "solid", 2.5)
    label_left(br, f"🚀 BREAK {format_level(br)}", "#854D0E", -3)

    add_hline_clean(entry, "#38BDF8", "dot", 2.0)
    label_left(entry, f"📊 ENTRY {format_level(entry)}", "#075985", -22)

    add_hline_clean(sl, "#FF4B4B", "solid", 2.0)
    label_left(sl, f"🛑 STOP {format_level(sl)}", "#7F1D1D", 22)

    add_hline_clean(tp1, "#FFFFFF", "dot", 1.7)
    label_left(tp1, f"🎯 TP1 {format_level(tp1)}", "#1F2937", -28)

    add_hline_clean(tp2, "#FFFFFF", "dot", 1.7)
    label_left(tp2, f"🎯 TP2 {format_level(tp2)}", "#1F2937", 28)

    # Frase dummies grande in alto
    phrase = row.get("Frase Dummies", build_break_phrase(row))
    fig.add_annotation(
        x=0.01, y=1.10,
        xref="paper", yref="paper",
        text=f"<b>{phrase}</b>",
        showarrow=False,
        font=dict(size=18, color="#FFFFFF"),
        bgcolor="rgba(0,0,0,0.78)",
        bordercolor="#FACC15",
        borderwidth=1,
        borderpad=8,
        align="left"
    )

    # Volumi verdi / rossi
    volume_colors = np.where(df["Close"] >= df["Open"], "#00E676", "#FF4B4B")
    vol_y = df["VolX"] if "VolX" in df else df["Volume"]
    fig.add_trace(
        go.Bar(
            x=df["Date"],
            y=vol_y,
            name="Volume",
            marker_color=volume_colors,
            opacity=0.88
        ),
        row=2,
        col=1
    )
    fig.add_hline(
        y=1.8,
        line_dash="dash",
        line_color="#FFFFFF",
        line_width=1,
        annotation_text="Volume caldo 1.8x",
        row=2,
        col=1
    )

    fig.update_xaxes(rangeslider_visible=False)
    fig.update_layout(
        height=720,
        template="plotly_dark",
        plot_bgcolor="#0B0F19",
        paper_bgcolor="#0B0F19",
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=82, b=10),
        title=f"{ticker} - V7 TradingView Clean",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.12)", zeroline=False, row=1, col=1)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.12)", zeroline=False, row=2, col=1)
    return fig


# ========================= UI STREAMLIT V5 =========================
st.set_page_config(page_title="NO BR NO PARTY V7", layout="wide")

UI_PRESETS = {
    "Nero Pro": {"bg":"#000000","sidebar":"#050505","card":"#101010","accent":"#00E676","text":"#FFFFFF","button":"#111111"},
    "Blu Trading": {"bg":"#020617","sidebar":"#07111F","card":"#0B1220","accent":"#38BDF8","text":"#FFFFFF","button":"#082F49"},
    "Rosso Alert": {"bg":"#000000","sidebar":"#090909","card":"#120808","accent":"#FF4B4B","text":"#FFFFFF","button":"#1A0A0A"},
    "Oro Premium": {"bg":"#000000","sidebar":"#070707","card":"#141106","accent":"#FACC15","text":"#FFFFFF","button":"#1E1A08"},
    "Chiaro": {"bg":"#F8FAFC","sidebar":"#FFFFFF","card":"#FFFFFF","accent":"#2563EB","text":"#111827","button":"#E5E7EB"},
}
DEFAULT_UI = {
    "app_name": "NO BR NO PARTY V7",
    "main_emoji": "🚀",
    "radar_emoji": "📡",
    "search_emoji": "🔍",
    "top_emoji": "🔥",
    "coin_emoji": "🪙",
    "settings_emoji": "⚙️",
    "theme": "Nero Pro",
    "show_zones": True,
    "show_break_phrase": True,
    "big_buttons": True,
    "rounded": True,
    "compact": False,
    "dummies": True,
}
for k, v in DEFAULT_UI.items():
    st.session_state.setdefault("ui_"+k, v)
st.session_state.setdefault("favorites", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

def apply_css():
    ui = UI_PRESETS.get(st.session_state.ui_theme, UI_PRESETS["Nero Pro"])
    radius = "16px" if st.session_state.ui_rounded else "4px"
    btn_pad = "0.8rem 1rem" if st.session_state.ui_big_buttons else "0.45rem 0.7rem"
    main_pad = "1.2rem 2rem" if st.session_state.ui_compact else "2rem 4rem"
    st.markdown(f"""
    <style>
    .stApp {{background:{ui['bg']} !important; color:{ui['text']} !important;}}
    .block-container {{padding:{main_pad} !important;}}
    section[data-testid="stSidebar"] {{background:{ui['sidebar']} !important; border-right:1px solid {ui['accent']}66 !important;}}
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {{color:{ui['text']} !important;}}
    h1, h2, h3, h4, h5, h6, p, label {{color:{ui['text']} !important;}}
    [data-testid="stMetric"], div[data-testid="stAlert"], div[data-testid="stExpander"] {{
        background:{ui['card']} !important; border-radius:{radius} !important; border:1px solid {ui['accent']}33 !important;
    }}
    div.stButton > button {{
        background:{ui['button']} !important; color:{ui['text']} !important; border:1px solid {ui['accent']} !important;
        border-radius:{radius} !important; padding:{btn_pad} !important; font-weight:800 !important;
    }}
    div.stButton > button:hover {{background:{ui['accent']} !important; color:#000 !important;}}
    hr {{border-color:{ui['accent']}55 !important;}}
    a {{color:{ui['accent']} !important;}}
    </style>
    """, unsafe_allow_html=True)

def settings_panel(location="sidebar"):
    target = st.sidebar if location == "sidebar" else st
    with target.expander(f"{st.session_state.ui_settings_emoji} Impostazioni App", expanded=False):
        st.session_state.ui_app_name = st.text_input("Nome app", st.session_state.ui_app_name, key=f"{location}_name")
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.ui_main_emoji = st.text_input("Emoji titolo", st.session_state.ui_main_emoji, max_chars=3, key=f"{location}_main_emoji")
            st.session_state.ui_radar_emoji = st.text_input("Emoji radar", st.session_state.ui_radar_emoji, max_chars=3, key=f"{location}_radar_emoji")
            st.session_state.ui_coin_emoji = st.text_input("Emoji coin", st.session_state.ui_coin_emoji, max_chars=3, key=f"{location}_coin_emoji")
        with c2:
            st.session_state.ui_search_emoji = st.text_input("Emoji ricerca", st.session_state.ui_search_emoji, max_chars=3, key=f"{location}_search_emoji")
            st.session_state.ui_top_emoji = st.text_input("Emoji top", st.session_state.ui_top_emoji, max_chars=3, key=f"{location}_top_emoji")
            st.session_state.ui_settings_emoji = st.text_input("Emoji impostazioni", st.session_state.ui_settings_emoji, max_chars=3, key=f"{location}_settings_emoji")
        st.session_state.ui_theme = st.selectbox("Tema", list(UI_PRESETS.keys()), index=list(UI_PRESETS.keys()).index(st.session_state.ui_theme), key=f"{location}_theme")
        st.session_state.ui_show_zones = st.toggle("Mostra supply / demand", value=st.session_state.ui_show_zones, key=f"{location}_zones")
        st.session_state.ui_show_break_phrase = st.toggle('Mostra frase "Se rompe..."', value=st.session_state.ui_show_break_phrase, key=f"{location}_phrase")
        st.session_state.ui_dummies = st.toggle("Modalità Dummies", value=st.session_state.ui_dummies, key=f"{location}_dummies")
        st.session_state.ui_big_buttons = st.toggle("Pulsanti grandi", value=st.session_state.ui_big_buttons, key=f"{location}_big")
        st.session_state.ui_rounded = st.toggle("Bordi arrotondati", value=st.session_state.ui_rounded, key=f"{location}_round")
        st.session_state.ui_compact = st.toggle("Modalità compatta", value=st.session_state.ui_compact, key=f"{location}_compact")
        if st.button("↩️ Ripristina impostazioni", use_container_width=True, key=f"{location}_reset"):
            for k, v in DEFAULT_UI.items():
                st.session_state["ui_"+k] = v
            st.rerun()

def verdict_from_score(score):
    try: score = int(score)
    except Exception: score = 0
    if score >= 82: return "🟢 PARTY VERO"
    if score >= 65: return "🟡 BUONO"
    if score >= 45: return "🟠 ASPETTA"
    return "🔴 NON ENTRARE"

def render_title():
    st.title(f"{st.session_state.ui_main_emoji} {st.session_state.ui_app_name}")
    st.caption("Versione V7: grafico TradingView pulito, frecce sui livelli, supply/demand leggibili e frasi dummies.")


def render_premium_summary(row):
    phrase = row.get("Frase Dummies", build_break_phrase(row))
    score = row.get("BR Score", 0)
    verdict = verdict_from_score(score)
    card_class = "party-card" if score >= 65 else "danger-card"
    st.markdown(f"""
    <div class="{card_class}">
        <div style="font-size:1.45rem;font-weight:900;margin-bottom:.35rem;">{phrase}</div>
        <div style="font-size:1.05rem;font-weight:800;">{verdict} &nbsp; | &nbsp; Score {score}/100 &nbsp; | &nbsp; Volume {row.get('Volume Booster','--')}x</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.warning(f"🔴 **SUPPLY / Resistenza**\n\n{row.get('Supply Zone', 'N/A')}")
    c2.success(f"🟢 **DEMAND / Supporto**\n\n{row.get('Demand Zone', 'N/A')}")
    c3.info(f"🎯 **Livello BREAK**\n\n{format_level(row.get('Livello BR', np.nan))}")
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("📊 Entry", format_level(row.get("Entry", np.nan)))
    e2.metric("🛑 Stop", format_level(row.get("SL", np.nan)))
    e3.metric("💰 TP1", format_level(row.get("TP1", np.nan)))
    e4.metric("⏱️ Timing", row.get("Tempo", "N/A"))

def render_coin_analyzer(prefix_key="coin"):
    st.markdown(f"### {st.session_state.ui_coin_emoji} Analizza una coin")
    c_box1, c_box2, c_box3 = st.columns([2, 1, 1])
    with c_box1:
        search_input = st.text_input("Ticker", value="BTC", placeholder="BTC, SOL, AERO...", key=f"{prefix_key}_ticker").upper().strip()
    with c_box2:
        search_tf = st.selectbox("Timeframe", TIMEFRAMES, index=TIMEFRAMES.index("15m"), key=f"{prefix_key}_tf")
    with c_box3:
        search_dir = st.selectbox("Direzione", ["LONG", "SHORT"], index=0, key=f"{prefix_key}_dir")
    c_btn1, c_btn2 = st.columns([1,1])
    with c_btn1:
        run = st.button("🔎 Analizza", type="primary", use_container_width=True, key=f"{prefix_key}_run")
    with c_btn2:
        addfav = st.button("⭐ Aggiungi ai preferiti", use_container_width=True, key=f"{prefix_key}_fav")
    fmt_input = search_input if search_input.endswith("USDT") else f"{search_input}USDT"
    if addfav and fmt_input not in st.session_state.favorites:
        st.session_state.favorites.append(fmt_input)
        st.success(f"{fmt_input} aggiunta ai preferiti")
    if run or search_input:
        with st.spinner(f"Analisi in corso per {fmt_input}..."):
            s_df, s_sym = fetch_ohlcv_safe(fmt_input, search_tf, limit=250)
            if s_df is not None:
                s_row, s_analyzed_df, s_levels = analyze_br(s_df, fmt_input, search_tf, 1.8, 1.0, 0.35, require_breakout=False, direction=search_dir)
                if s_row:
                    render_premium_summary(s_row)
                    st.plotly_chart(draw_chart(s_analyzed_df, fmt_input, s_levels, s_row), use_container_width=True, key=f"{prefix_key}_chart")
                    with st.expander("Dettagli tecnici"):
                        st.write(s_row)
                else:
                    st.warning("Dati caricati, ma nessun livello utile trovato.")
            else:
                st.error(f"Impossibile caricare dati per {fmt_input}.")

def render_radar(prefix_key="radar"):
    st.markdown(f"### {st.session_state.ui_radar_emoji} Radar automatico")
    f1, f2, f3 = st.columns(3)
    with f1:
        chosen_timeframe = st.selectbox("Timeframe Radar", TIMEFRAMES, index=TIMEFRAMES.index("15m"), key=f"{prefix_key}_tf")
        trade_direction = st.selectbox("Direzione Radar", ["LONG", "SHORT"], index=0, key=f"{prefix_key}_dir")
    with f2:
        category_options = ["YouHodler List", "Tutti i 444 Asset"] + [k for k in BYBIT_444_DATABASE.keys() if k != "YouHodler List"]
        category_selector = st.selectbox("Categoria", category_options, index=0, key=f"{prefix_key}_cat")
        max_assets = st.slider("Numero massimo coin", 10, 444, 40, step=10, key=f"{prefix_key}_max")
    with f3:
        volume_hot = st.slider("Volume minimo", 1.1, 5.0, 1.8, step=0.1, key=f"{prefix_key}_vol")
        min_score = st.slider("Score minimo", 0, 100, 45, step=5, key=f"{prefix_key}_score")
    require_breakout = st.toggle("Solo rottura già fatta", value=False, key=f"{prefix_key}_break")
    if st.button("🔄 Avvia scansione radar", type="primary", use_container_width=True, key=f"{prefix_key}_scan"):
        current_tickers = list(ALL_TICKERS) if category_selector == "Tutti i 444 Asset" else BYBIT_444_DATABASE[category_selector]
        current_tickers = current_tickers[:max_assets]
        rows, cache = [], {}
        progress = st.progress(0)
        status = st.empty()
        for i, ticker in enumerate(current_tickers, start=1):
            status.write(f"Scansiono {ticker}... {i}/{len(current_tickers)}")
            df, used_symbol = fetch_ohlcv_safe(ticker, chosen_timeframe, limit=280)
            if df is not None:
                try:
                    row, analyzed_df, levels = analyze_br(df, ticker, chosen_timeframe, volume_hot, 1.0, 0.35, require_breakout=require_breakout, direction=trade_direction)
                    if row:
                        row["Verdetto"] = verdict_from_score(row["BR Score"])
                        rows.append(row)
                        cache[ticker] = {"df": analyzed_df, "levels": levels, "row": row, "symbol": used_symbol}
                except Exception:
                    pass
            progress.progress(i / len(current_tickers))
        progress.empty(); status.empty()
        st.session_state.scan_rows = pd.DataFrame(rows)
        if not st.session_state.scan_rows.empty:
            st.session_state.scan_rows = st.session_state.scan_rows[st.session_state.scan_rows["BR Score"] >= min_score].sort_values(["BR Score", "Volume Booster"], ascending=[False, False]).reset_index(drop=True)
        st.session_state.scan_cache = cache
    df_display = st.session_state.get("scan_rows", pd.DataFrame())
    if df_display.empty:
        st.info("Premi Avvia scansione radar per popolare la tabella.")
    else:
        cols = [c for c in ["Ticker","Direzione","Verdetto","Situazione","Frase Dummies","BR Score","Volume Booster","Livello BR"] if c in df_display.columns]
        st.dataframe(df_display[cols], use_container_width=True, hide_index=True, height=360)
        ticker_scelto = st.selectbox("Apri grafico coin", df_display["Ticker"].tolist(), key=f"{prefix_key}_select_coin")
        pack = st.session_state.scan_cache.get(ticker_scelto)
        if pack:
            row = pack["row"]
            render_premium_summary(row)
            st.plotly_chart(draw_chart(pack["df"], ticker_scelto, pack["levels"], row), use_container_width=True, key=f"{prefix_key}_radar_chart")

def render_home():
    st.markdown(f"### {st.session_state.ui_top_emoji} Home")
    st.markdown("""
    <div class="party-card">
        <b>📱 Versione V7 Mobile/PWA pronta.</b><br>
        Apri questa app da Android o iPhone e usa "Aggiungi alla schermata Home".
    </div>
    """, unsafe_allow_html=True)
    h1, h2, h3 = st.columns(3)
    h1.metric("🟢 PARTY VERO", "Score ≥ 82")
    h2.metric("🟡 BUONO", "65 - 81")
    h3.metric("🔴 NON ENTRARE", "< 45")
    if st.session_state.favorites:
        st.write("⭐ **Preferiti rapidi:**")
        cols = st.columns(min(4, len(st.session_state.favorites)))
        for i, fav in enumerate(st.session_state.favorites[:4]):
            cols[i % len(cols)].metric(fav, "Vai in Coin")
    st.markdown("#### Regola d'oro")
    st.write("Non entrare perché il prezzo si muove. Entra solo quando rompe il livello giusto con volume e struttura chiara.")

def render_favorites():
    st.markdown("### ⭐ Preferiti")
    fav_text = st.text_area("Lista coin preferite, una per riga", value="\n".join(st.session_state.favorites), height=160)
    if st.button("💾 Salva preferiti", use_container_width=True):
        st.session_state.favorites = [x.strip().upper() for x in fav_text.splitlines() if x.strip()]
        st.success("Preferiti salvati per questa sessione.")
    st.write(st.session_state.favorites)

apply_css()

st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container {padding: 0.75rem 0.75rem !important;}
    h1 {font-size: 2rem !important; line-height: 1.1 !important;}
    h2, h3 {font-size: 1.35rem !important;}
    [data-testid="stMetric"] {padding: 0.75rem !important;}
    div.stButton > button {min-height: 52px !important; font-size: 1rem !important;}
    .stTabs [data-baseweb="tab-list"] {gap: 0.2rem !important; overflow-x: auto !important;}
    .stTabs [data-baseweb="tab"] {padding: 0.75rem 0.75rem !important; white-space: nowrap !important;}
}
.party-card {
    background: linear-gradient(135deg, rgba(0,230,118,.10), rgba(56,189,248,.06));
    border: 1px solid rgba(0,230,118,.45);
    border-radius: 18px;
    padding: 1rem;
    margin: .6rem 0;
}
.danger-card {
    background: linear-gradient(135deg, rgba(255,75,75,.12), rgba(250,204,21,.04));
    border: 1px solid rgba(255,75,75,.45);
    border-radius: 18px;
    padding: 1rem;
    margin: .6rem 0;
}
</style>
""", unsafe_allow_html=True)

render_title()

tab_home, tab_coin, tab_radar, tab_fav, tab_settings = st.tabs([
    "🏠 Home", "🪙 Coin", "📡 Radar", "⭐ Preferiti", "⚙️ Impostazioni"
])

with tab_home:
    render_home()
with tab_coin:
    render_coin_analyzer("tabs_coin")
with tab_radar:
    render_radar("tabs_radar")
with tab_fav:
    render_favorites()
with tab_settings:
    settings_panel("top")
