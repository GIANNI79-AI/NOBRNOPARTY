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
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_heights=[0.78, 0.22])
    fig.add_trace(go.Candlestick(x=df["Date"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="Prezzo"), row=1, col=1)
    for col, name in [("EMA5", "EMA 5"), ("EMA10", "EMA 10"), ("EMA60", "EMA 60"), ("EMA223", "EMA 223"), ("VWAP", "VWAP"), ("MVWAP", "MVWAP")]:
        if col in df: fig.add_trace(go.Scatter(x=df["Date"], y=df[col], name=name, line=dict(width=1.2)), row=1, col=1)

    atr_last = float(df["ATR"].iloc[-1]) if "ATR" in df and pd.notna(df["ATR"].iloc[-1]) else 0
    price_last = float(df["Close"].iloc[-1]) if "Close" in df else 0
    zone_w = max(atr_last * 0.35, price_last * 0.0015) if price_last else 0

    res_levels = sorted([l for l in levels if l["kind"] == "res"], key=lambda x: x["value"])
    sup_levels = sorted([l for l in levels if l["kind"] == "sup"], key=lambda x: x["value"], reverse=True)

    if st.session_state.get("ui_show_zones", True):
        for lvl in res_levels[-3:]:
            fig.add_hrect(y0=lvl["value"]-zone_w, y1=lvl["value"]+zone_w, fillcolor="rgba(255, 0, 70, 0.18)", line_width=0, annotation_text="SUPPLY / RESISTENZA", row=1, col=1)
        for lvl in sup_levels[:3]:
            fig.add_hrect(y0=lvl["value"]-zone_w, y1=lvl["value"]+zone_w, fillcolor="rgba(0, 230, 118, 0.15)", line_width=0, annotation_text="DEMAND / SUPPORTO", row=1, col=1)

    for lvl in levels:
        label = f"{'🧱 Resistenza' if lvl['kind'] == 'res' else '🛟 Supporto'} {'seria' if lvl['power'] == 'A' else 'veloce'}"
        fig.add_hline(y=lvl["value"], line_width=2 if lvl["power"] == "A" else 1, line_dash="dash", annotation_text=label, row=1, col=1)

    if pd.notna(row.get("Livello BR")): fig.add_hline(y=row["Livello BR"], line_width=3, annotation_text="🎉 LIVELLO PARTY / BR-BS", row=1, col=1)
    for y, label in [(row.get("Entry"), "Entry"), (row.get("SL"), "SL"), (row.get("TP1"), "TP1"), (row.get("TP2"), "TP2")]:
        if pd.notna(y): fig.add_hline(y=y, line_dash="dot", annotation_text=label, row=1, col=1)

    fig.add_trace(go.Bar(x=df["Date"], y=df["VolX"], name="Volume Booster x media 20", marker_color="orange"), row=2, col=1)
    fig.add_hline(y=1.8, line_dash="dash", annotation_text="Volume caldo 1.8x", row=2, col=1)
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_layout(height=700, template="plotly_dark", plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font=dict(color="white"), margin=dict(l=10, r=10, t=35, b=10), title=f"{ticker} - Livelli, Supply/Demand e NO BR NO PARTY")
    return fig

# ========================= UI STREAMLIT ===========================

st.set_page_config(page_title="NO BR NO PARTY Scanner", layout="wide")

# ========================= IMPOSTAZIONI APP =========================
UI_PRESETS = {
    "Nero Pro": {"bg":"#000000","sidebar":"#050505","card":"#101010","accent":"#00E676","text":"#FFFFFF","button":"#111111"},
    "Blu Trading": {"bg":"#020617","sidebar":"#07111F","card":"#0B1220","accent":"#38BDF8","text":"#FFFFFF","button":"#082F49"},
    "Rosso Alert": {"bg":"#000000","sidebar":"#090909","card":"#120808","accent":"#FF4B4B","text":"#FFFFFF","button":"#1A0A0A"},
    "Oro Premium": {"bg":"#000000","sidebar":"#070707","card":"#141106","accent":"#FACC15","text":"#FFFFFF","button":"#1E1A08"},
    "Chiaro": {"bg":"#F8FAFC","sidebar":"#FFFFFF","card":"#FFFFFF","accent":"#2563EB","text":"#111827","button":"#E5E7EB"},
}
for k, v in {
    "app_name": "NO BR NO PARTY Scanner - LONG & SHORT",
    "main_emoji": "🚀",
    "radar_emoji": "📡",
    "search_emoji": "🔍",
    "top_emoji": "🔥",
    "theme": "Nero Pro",
    "show_zones": True,
    "show_break_phrase": True,
    "big_buttons": True,
    "rounded": True,
    "compact": False,
}.items():
    st.session_state.setdefault("ui_"+k, v)

with st.sidebar.expander("⚙️ Impostazioni App", expanded=False):
    st.session_state.ui_app_name = st.text_input("Nome app", st.session_state.ui_app_name)
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.ui_main_emoji = st.text_input("Emoji titolo", st.session_state.ui_main_emoji, max_chars=3)
        st.session_state.ui_radar_emoji = st.text_input("Emoji radar", st.session_state.ui_radar_emoji, max_chars=3)
    with c2:
        st.session_state.ui_search_emoji = st.text_input("Emoji ricerca", st.session_state.ui_search_emoji, max_chars=3)
        st.session_state.ui_top_emoji = st.text_input("Emoji top", st.session_state.ui_top_emoji, max_chars=3)
    st.session_state.ui_theme = st.selectbox("Tema", list(UI_PRESETS.keys()), index=list(UI_PRESETS.keys()).index(st.session_state.ui_theme) if st.session_state.ui_theme in UI_PRESETS else 0)
    st.session_state.ui_show_zones = st.toggle("Mostra supporti / resistenze / supply-demand", value=st.session_state.ui_show_zones)
    st.session_state.ui_show_break_phrase = st.toggle('Mostra frase "Se rompe..."', value=st.session_state.ui_show_break_phrase)
    st.session_state.ui_big_buttons = st.toggle("Pulsanti grandi", value=st.session_state.ui_big_buttons)
    st.session_state.ui_rounded = st.toggle("Bordi arrotondati", value=st.session_state.ui_rounded)
    st.session_state.ui_compact = st.toggle("Modalità compatta", value=st.session_state.ui_compact)
    if st.button("↩️ Ripristina", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith("ui_"):
                del st.session_state[key]
        st.rerun()

ui = UI_PRESETS[st.session_state.ui_theme]
radius = "16px" if st.session_state.ui_rounded else "4px"
btn_pad = "0.8rem 1rem" if st.session_state.ui_big_buttons else "0.45rem 0.7rem"
main_pad = "1.2rem 2rem" if st.session_state.ui_compact else "2rem 4rem"

st.markdown(f"""
<style>
.stApp {{background:{ui['bg']} !important; color:{ui['text']} !important;}}
.block-container {{padding:{main_pad} !important;}}
section[data-testid="stSidebar"] {{background:{ui['sidebar']} !important; border-right:1px solid {ui['accent']}66 !important;}}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {{
    color:{ui['text']} !important;
}}
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

APP_TITLE = f"{st.session_state.ui_main_emoji} {st.session_state.ui_app_name}"
RADAR_EMOJI = st.session_state.ui_radar_emoji
SEARCH_EMOJI = st.session_state.ui_search_emoji
TOP_EMOJI = st.session_state.ui_top_emoji
# ====================================================================

st.title(APP_TITLE)

with st.sidebar:
    st.header("🎛️ Comandi Radar")
    chosen_timeframe = st.selectbox("Timeframe Radar", TIMEFRAMES, index=TIMEFRAMES.index("15m"))
    trade_direction = st.selectbox("Direzione Radar", ["LONG", "SHORT"], index=0)
    category_options = ["YouHodler List", "Tutti i 444 Asset"] + [k for k in BYBIT_444_DATABASE.keys() if k != "YouHodler List"]
    category_selector = st.selectbox("Categoria Database", category_options, index=0)
    max_assets = st.slider("Numero massimo coin da scansionare", 10, 444, 80, step=10)
    volume_hot = st.slider("Volume minimo per PARTY", 1.1, 5.0, 1.8, step=0.1)
    distance_watch = st.slider("Distanza max dal BR (%)", 0.1, 5.0, 1.0, step=0.1)
    retest_tol = st.slider("Tolleranza retest (%)", 0.05, 1.5, 0.35, step=0.05)
    min_score = st.slider("BR Score minimo in tabella", 0, 100, 25, step=5)
    require_breakout = st.toggle("Mostra solo trade con rottura già fatta", value=True)

# ==================== SEZIONE NUOVA: BOX DI RICERCA RAPIDO ON-DEMAND ====================
st.markdown(f"### {SEARCH_EMOJI} RICERCA ISTANTANEA DIRETTA (Single Ticker On-Demand)")
st.caption("Usa questo box per analizzare al volo una coin specifica a tua scelta, senza toccare lo scanner generale.")

c_box1, c_box2, c_box3 = st.columns([2, 1, 1])
with c_box1:
    search_input = st.text_input("Inserisci Ticker Singolo (es. SOL, RENDER, BTC, DOGE):", value="").upper().strip()
with c_box2:
    search_tf = st.selectbox("Timeframe Ricerca Diretta", TIMEFRAMES, index=TIMEFRAMES.index("15m"), key="s_tf")
with c_box3:
    search_dir = st.selectbox("Direzione Ricerca Diretta", ["LONG", "SHORT"], index=0, key="s_dir")

if search_input:
    fmt_input = search_input if search_input.endswith("USDT") else f"{search_input}USDT"
    with st.spinner(f"Analisi flash in corso per {fmt_input}..."):
        s_df, s_sym = fetch_ohlcv_safe(fmt_input, search_tf, limit=250)
        if s_df is not None:
            s_row, s_analyzed_df, s_levels = analyze_br(s_df, fmt_input, search_tf, volume_hot, distance_watch, retest_tol, require_breakout=False, direction=search_dir)
            if s_row:
                st.markdown(f"#### 📊 Scheda Rapida: {fmt_input} ({search_tf})")
                sm1, sm2, sm3, sm4, sm5 = st.columns(5)
                sm1.metric("Situazione", s_row["Situazione"])
                sm2.metric("BR Score", f"{s_row['BR Score']}/100")
                sm3.metric("Volume Attuale", f"{s_row['Volume Booster']}x")
                sm4.metric("Direzione", s_row["Direzione"])
                sm5.metric("Operatività", s_row["Tempo"])
                
                if st.session_state.get("ui_show_break_phrase", True):
                    st.success(f"### {s_row.get('Frase Dummies', build_break_phrase(s_row))}")
                z1, z2, z3 = st.columns(3)
                z1.warning(f"🔴 **Supply / Resistenza**\n\n{s_row.get('Supply Zone', 'N/A')}")
                z2.success(f"🟢 **Demand / Supporto**\n\n{s_row.get('Demand Zone', 'N/A')}")
                z3.info(f"🎯 **Livello da guardare**\n\n{format_level(s_row.get('Livello BR', np.nan))}")
                st.info(f"💡 **Motivazione Confluenze:** {s_row['Perché']}")
                
                st_c1, st_c2, st_c3, st_c4 = st.columns(4)
                st_c1.info(f"📊 **Entry Consigliata:** {s_row['Entry']:.6f}")
                st_c2.warning(f"🎯 **Livello Chiave BR:** {s_row['Livello BR']:.6f}" if pd.notna(s_row['Livello BR']) else "🎯 **Livello:** N/A")
                st_c3.error(f"🛑 **Stop Loss (SL):** {s_row['SL']:.6f}" if pd.notna(s_row['SL']) else "🛑 **SL:** N/A")
                st_c4.success(f"💰 **Take Profit 1 (TP1):** {s_row['TP1']:.6f}" if pd.notna(s_row['TP1']) else "💰 **TP1:** N/A")
                
                st.plotly_chart(draw_chart(s_analyzed_df, fmt_input, s_levels, s_row), use_container_width=True, key="search_chart")
        else:
            st.error(f"❌ Impossibile caricare i dati per '{search_input}'. Verifica che sia scambiato USDT su Bybit.")

st.markdown("---")

# ==================== STRUTTURA RADAR DI MASSA ORIGINALE ====================
st.markdown(f"### {RADAR_EMOJI} RADAR MULTI-ASSET GENERALE")

current_tickers = list(ALL_TICKERS) if category_selector == "Tutti i 444 Asset" else BYBIT_444_DATABASE[category_selector]
current_tickers = current_tickers[:max_assets]

col_a, col_b, col_c = st.columns([1,1,2])
with col_a:
    run_scan = st.button("🔄 AVVIA SCANSIONE RADAR DI MASSA", type="primary", use_container_width=True)
with col_b:
    st.metric("TF attivo Radar", chosen_timeframe)
with col_c:
    st.info(f"Filtri Radar -> Direzione: {trade_direction} | Categoria: {category_selector}")

if run_scan:
    rows = []
    cache = {}
    progress = st.progress(0)
    status = st.empty()
    total = len(current_tickers)
    for i, ticker in enumerate(current_tickers, start=1):
        status.write(f"Scansiono {ticker}... {i}/{total}")
        df, used_symbol = fetch_ohlcv_safe(ticker, chosen_timeframe, limit=280)
        if df is not None:
            try:
                row, analyzed_df, levels = analyze_br(df, ticker, chosen_timeframe, volume_hot, distance_watch, retest_tol, require_breakout=require_breakout, direction=trade_direction)
                if row:
                    rows.append(row)
                    cache[ticker] = {"df": analyzed_df, "levels": levels, "row": row, "symbol": used_symbol}
            except Exception:
                pass
        progress.progress(i / total)
    progress.empty()
    status.empty()
    
    if rows:
        out = pd.DataFrame(rows)
        out = out[out["BR Score"] >= min_score].sort_values(["BR Score", "Volume Booster", "Distanza dal PARTY %"], ascending=[False, False, True]).reset_index(drop=True)
        st.session_state.scan_rows = out
        st.session_state.scan_cache = cache
    else:
        st.session_state.scan_rows = pd.DataFrame()
        st.session_state.scan_cache = {}

df_display = st.session_state.scan_rows

if df_display.empty:
    st.info("💡 Nessun dato caricato nel Radar. Premi il pulsante sopra 'AVVIA SCANSIONE RADAR DI MASSA' per popolare la tabella dei 444 asset.")
else:
    top = df_display.head(5)[["Ticker", "Direzione", "Situazione", "Frase Dummies", "Party Meter", "BR Score", "Volume Booster"]] if "Frase Dummies" in df_display.columns else df_display.head(5)[["Ticker", "Direzione", "Situazione", "Party Meter", "BR Score", "Volume Booster"]]
    st.subheader(f"{TOP_EMOJI} Top 5 Active Crypto")
    st.dataframe(top, use_container_width=True, hide_index=True)

    st.subheader("📋 Griglia Scanner Completa")
    st.dataframe(
        df_display,
        use_container_width=True,
        height=380,
        hide_index=True,
        column_config={
            "TradingView": st.column_config.LinkColumn("TradingView", display_text="Apri TV ↗"),
            "Party Meter": st.column_config.ProgressColumn("Party Meter", min_value=0, max_value=10),
            "BR Score": st.column_config.ProgressColumn("BR Score", min_value=0, max_value=100),
            "Distanza dal PARTY %": st.column_config.NumberColumn(format="%.3f%%"),
            "Volume Booster": st.column_config.NumberColumn(format="%.2fx"),
            "Livello BR": st.column_config.NumberColumn(format="%.8f"),
            "Entry": st.column_config.NumberColumn(format="%.8f"),
            "SL": st.column_config.NumberColumn(format="%.8f"),
            "TP1": st.column_config.NumberColumn(format="%.8f"),
            "TP2": st.column_config.NumberColumn(format="%.8f"),
        }
    )

    # SISTEMA DI AGGIORNAMENTO GRAFICO AD ALTA STABILITÀ SENZA RISCHIO SCHERMATA BIANCA
    st.markdown("#### 📈 Seleziona l'Asset Scansionato per visualizzare il Grafico Plotly")
    lista_coin_disponibili = df_display["Ticker"].tolist()
    ticker_scelto = st.selectbox("Scegli quale coin analizzare sotto:", lista_coin_disponibili, index=0)

    pack = st.session_state.scan_cache.get(ticker_scelto)
    if pack:
        row = pack["row"]
        st.subheader(f"📊 Scheda Tecnica Dummies Radar: {ticker_scelto}")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Situazione", row["Situazione"])
        c2.metric("Party Meter", f"{row['Party Meter']}/10")
        c3.metric("Volume Attuale", f"{row['Volume Booster']}x")
        c4.metric("Distanza Livello", f"{row['Distanza dal PARTY %']}%")
        c5.metric("Tempo / Timing", row["Tempo"])
        if st.session_state.get("ui_show_break_phrase", True):
            st.success(f"### {row.get('Frase Dummies', build_break_phrase(row))}")
        zz1, zz2, zz3 = st.columns(3)
        zz1.warning(f"🔴 **Supply / Resistenza**\n\n{row.get('Supply Zone', 'N/A')}")
        zz2.success(f"🟢 **Demand / Supporto**\n\n{row.get('Demand Zone', 'N/A')}")
        zz3.info(f"🎯 **Livello chiave**\n\n{format_level(row.get('Livello BR', np.nan))}")
        st.write(f"**Perché:** {row['Perché']}")
        st.plotly_chart(draw_chart(pack["df"], ticker_scelto, pack["levels"], row), use_container_width=True, key="radar_chart")
