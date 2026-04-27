"""
GLO Analytics Pro — วิเคราะห์สลากกินแบ่งรัฐบาล
=================================================
Real-time data · Statistical Analysis · Bayesian Prediction Engine
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from collections import Counter, defaultdict
from scipy.stats import poisson
import warnings
import json
import re
import time
import sqlite3
import os
import hashlib

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="GLO Analytics Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
# PROFESSIONAL DARK THEME CSS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Sarabun:wght@300;400;600;700&family=Teko:wght@500;600&display=swap');

:root {
    --bg-primary:    #0a0e1a;
    --bg-card:       #0f1628;
    --bg-elevated:   #161d35;
    --accent-gold:   #f5c842;
    --accent-cyan:   #00d4ff;
    --accent-green:  #00ff88;
    --accent-red:    #ff4560;
    --accent-purple: #8b5cf6;
    --text-primary:  #e8eaf6;
    --text-muted:    #7986cb;
    --border:        #1e2a4a;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    font-family: 'Sarabun', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

h1, h2, h3 { font-family: 'Teko', sans-serif !important; letter-spacing: 1px; }

.main-header {
    background: linear-gradient(135deg, #0f1628 0%, #1a2040 50%, #0f1628 100%);
    border: 1px solid var(--border);
    border-bottom: 2px solid var(--accent-gold);
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at top left, rgba(245,200,66,0.08) 0%, transparent 60%);
}
.main-header h1 {
    font-size: 2.8rem !important;
    color: var(--accent-gold) !important;
    margin: 0 !important;
    text-shadow: 0 0 30px rgba(245,200,66,0.4);
}
.main-header .subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: 4px;
    font-family: 'IBM Plex Mono', monospace;
}
.live-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0,255,136,0.1);
    border: 1px solid var(--accent-green);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: var(--accent-green);
    font-family: 'IBM Plex Mono', monospace;
}
.live-dot {
    width: 7px; height: 7px;
    background: var(--accent-green);
    border-radius: 50%;
    animation: pulse 1.4s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent-color, var(--accent-gold));
}
.kpi-label { font-size: 0.78rem; color: var(--text-muted); font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; letter-spacing: 1px; }
.kpi-value { font-family: 'Teko', sans-serif; font-size: 2.2rem; color: var(--text-primary); line-height: 1.1; margin: 4px 0; }
.kpi-sub   { font-size: 0.8rem; color: var(--text-muted); }

.section-header {
    font-family: 'Teko', sans-serif;
    font-size: 1.5rem;
    color: var(--accent-cyan);
    border-left: 3px solid var(--accent-cyan);
    padding-left: 12px;
    margin: 24px 0 16px 0;
    letter-spacing: 1px;
}

.prize-box {
    background: linear-gradient(135deg, var(--bg-elevated) 0%, var(--bg-card) 100%);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.prize-title { font-size: 0.78rem; color: var(--text-muted); font-family: 'IBM Plex Mono', monospace; margin-bottom: 8px; text-transform: uppercase; }
.prize-number {
    font-family: 'Teko', sans-serif;
    font-size: 2.6rem;
    letter-spacing: 6px;
    color: var(--accent-gold);
    text-shadow: 0 0 20px rgba(245,200,66,0.5);
}
.prize-number-sm {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    color: var(--text-primary);
    letter-spacing: 3px;
}

.pred-card {
    background: var(--bg-elevated);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}
.pred-tier { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }
.pred-numbers {
    display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;
}
.pred-num {
    background: rgba(0,0,0,0.3);
    border-radius: 8px;
    padding: 10px 16px;
    font-family: 'Teko', sans-serif;
    font-size: 2rem;
    letter-spacing: 4px;
    border: 1px solid;
    text-align: center;
}
.pred-confidence {
    margin-top: 10px;
    font-size: 0.8rem;
    font-family: 'IBM Plex Mono', monospace;
    color: var(--text-muted);
    text-align: right;
}

.hot-num  { background: rgba(255,69,96,0.15); border-color: var(--accent-red); color: var(--accent-red); }
.cold-num { background: rgba(0,212,255,0.1); border-color: var(--accent-cyan); color: var(--accent-cyan); }
.warm-num { background: rgba(245,200,66,0.1); border-color: var(--accent-gold); color: var(--accent-gold); }

/* Streamlit overrides */
[data-testid="metric-container"] { background: var(--bg-card); border-radius: 8px; border: 1px solid var(--border); padding: 12px; }
.stSelectbox > div > div { background: var(--bg-elevated) !important; border-color: var(--border) !important; color: var(--text-primary) !important; }
div[data-testid="stMetric"] label { color: var(--text-muted) !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.8rem !important; }
.stDataFrame { background: var(--bg-card) !important; border-radius: 8px; overflow: hidden; }
[data-testid="stExpander"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 8px; }
.stTabs [data-baseweb="tab-list"]  { background: var(--bg-card) !important; border-bottom: 1px solid var(--border); gap: 4px; }
.stTabs [data-baseweb="tab"]       { color: var(--text-muted) !important; font-family: 'IBM Plex Mono', monospace !important; border-radius: 6px 6px 0 0; }
.stTabs [aria-selected="true"]     { color: var(--accent-cyan) !important; border-bottom: 2px solid var(--accent-cyan) !important; }
.stButton > button                 { background: var(--bg-elevated); border: 1px solid var(--accent-cyan); color: var(--accent-cyan); font-family: 'IBM Plex Mono', monospace; border-radius: 6px; }
.stButton > button:hover           { background: rgba(0,212,255,0.1); }
div.block-container { padding-top: 1.5rem; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════
GLO_API_BASE   = "https://www.glo.or.th/api/lottery"
HEADERS        = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer":    "https://www.glo.or.th/",
    "Accept":     "application/json, text/plain, */*",
}
DB_PATH = os.path.join(os.path.dirname(__file__), "glo_cache.db")

# ══════════════════════════════════════════════════════════
# SQLITE CACHE LAYER
# ══════════════════════════════════════════════════════════
def _db_conn():
    """Return a SQLite connection; creates DB + table if needed."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lottery_results (
            draw_date TEXT PRIMARY KEY,
            prize1    TEXT,
            near1     TEXT,
            front3    TEXT,
            back3     TEXT,
            back2     TEXT,
            prize2    TEXT,
            prize3    TEXT,
            fetched_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn

def db_get(draw_date: str) -> dict | None:
    """Load a result from SQLite cache. Returns None if not found."""
    try:
        conn = _db_conn()
        row  = conn.execute(
            "SELECT * FROM lottery_results WHERE draw_date=?", (draw_date,)
        ).fetchone()
        conn.close()
        if row:
            cols = ["draw_date","prize1","near1","front3","back3","back2","prize2","prize3","fetched_at"]
            d = dict(zip(cols, row))
            # Deserialise JSON lists
            for field in ["near1","front3","back3","prize2","prize3"]:
                try:
                    d[field] = json.loads(d[field]) if d[field] else []
                except Exception:
                    d[field] = []
            d["date"] = d.pop("draw_date")
            d.pop("fetched_at", None)
            return d
    except Exception:
        pass
    return None

def db_put(result: dict):
    """Save a result dict to SQLite cache."""
    try:
        conn = _db_conn()
        conn.execute("""
            INSERT OR REPLACE INTO lottery_results
              (draw_date, prize1, near1, front3, back3, back2, prize2, prize3)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            result.get("date",""),
            str(result.get("prize1","")),
            json.dumps(result.get("near1",  []), ensure_ascii=False),
            json.dumps(result.get("front3", []), ensure_ascii=False),
            json.dumps(result.get("back3",  []), ensure_ascii=False),
            str(result.get("back2","")),
            json.dumps(result.get("prize2", []), ensure_ascii=False),
            json.dumps(result.get("prize3", []), ensure_ascii=False),
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass

def db_count() -> int:
    """Return number of cached rows."""
    try:
        conn = _db_conn()
        n = conn.execute("SELECT COUNT(*) FROM lottery_results").fetchone()[0]
        conn.close()
        return n
    except Exception:
        return 0

def db_clear():
    """Wipe all cached rows."""
    try:
        conn = _db_conn()
        conn.execute("DELETE FROM lottery_results")
        conn.commit()
        conn.close()
    except Exception:
        pass
CHART_TEMPLATE = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono, Sarabun, sans-serif", color="#e8eaf6"),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(showgrid=True, gridcolor="rgba(30,42,74,0.8)", gridwidth=1),
    yaxis=dict(showgrid=True, gridcolor="rgba(30,42,74,0.8)", gridwidth=1),
)

# ══════════════════════════════════════════════════════════
# HELPERS — Generate draw dates (1st & 16th of every month)
# ══════════════════════════════════════════════════════════
def get_draw_dates(n=60) -> list[str]:
    """Return last n lottery draw dates as dd/mm/yyyy strings."""
    draws = []
    d = date.today()
    # go back to last valid draw
    while d.day not in (1, 16):
        d -= timedelta(days=1)
    for _ in range(n):
        draws.append(d.strftime("%d/%m/%Y"))
        # step back to previous draw
        if d.day == 16:
            d = d.replace(day=1)
        else:
            prev = d - timedelta(days=1)
            d = prev.replace(day=16)
    return draws

# ══════════════════════════════════════════════════════════
# DATA FETCHING
# ══════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_result_by_date(draw_date: str) -> dict | None:
    """Fetch a single lottery result from GLO API."""
    # GLO expects Buddhist Era year; convert if needed
    try:
        parts = draw_date.split("/")
        dd, mm, yyyy_ce = parts[0], parts[1], int(parts[2])
        yyyy_be = yyyy_ce + 543
        be_date = f"{dd}/{mm}/{yyyy_be}"

        url = f"{GLO_API_BASE}/getLotteryResult?date={be_date}"
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code == 200:
            raw = resp.json()
            if raw.get("status") == "0000":
                return _parse_glo_response(raw, draw_date)
    except Exception:
        pass
    return None

def _parse_glo_response(raw: dict, draw_date: str) -> dict:
    """Normalize GLO API response to internal format."""
    try:
        r = raw.get("response", {})
        prizes = r.get("prizes", [])
        result = {
            "date": draw_date,
            "prize1": "",
            "near1": [],
            "front3": [],
            "back3": [],
            "back2": "",
            "prize2": [],
            "prize3": [],
        }
        for p in prizes:
            pid   = str(p.get("id", ""))
            nums  = [n.get("number", "") for n in p.get("number", [])]
            if pid == "1":
                result["prize1"]  = nums[0] if nums else ""
            elif pid == "2":
                result["near1"]   = nums
            elif pid == "3":
                result["prize2"]  = nums
            elif pid == "4":
                result["prize3"]  = nums
            elif pid == "5":
                result["front3"]  = nums
            elif pid == "6":
                result["back3"]   = nums
            elif pid == "7":
                result["back2"]   = nums[0] if nums else ""
        return result
    except Exception:
        return None

def _make_demo_result(draw_date: str, seed: int = 42) -> dict:
    """Generate deterministic demo result when API unavailable."""
    rng = np.random.default_rng(seed)
    six = lambda: str(rng.integers(100000, 999999))
    three = lambda: str(rng.integers(100, 999)).zfill(3)
    two = lambda: str(rng.integers(0, 99)).zfill(2)
    return {
        "date":   draw_date,
        "prize1": six(),
        "near1":  [six(), six()],
        "front3": [three(), three()],
        "back3":  [three(), three()],
        "back2":  two(),
        "prize2": [six() for _ in range(5)],
        "prize3": [six() for _ in range(10)],
    }

@st.cache_data(ttl=3600, show_spinner=False)
def load_historical_data(n_draws: int = 52) -> pd.DataFrame:
    """
    Load historical results with 3-tier priority:
      1. SQLite cache (instant)  ← hits first
      2. GLO API (slow, online)
      3. Demo data (offline fallback)
    """
    dates       = get_draw_dates(n_draws + 5)[:n_draws]
    rows        = []
    need_fetch  = [d for d in dates if db_get(d) is None]
    cached_rows = [db_get(d) for d in dates if db_get(d) is not None]
    rows.extend(cached_rows)

    if need_fetch:
        bar = st.progress(0, text=f"⏳ กำลังโหลด {len(need_fetch)} งวดใหม่จาก GLO API…")
        for i, d in enumerate(need_fetch):
            bar.progress((i + 1) / len(need_fetch), text=f"⏳ โหลดงวด {d} …")
            seed   = int(d.replace("/", "")) % 9999997
            result = fetch_result_by_date(d)
            if result and result.get("prize1"):
                db_put(result)            # 💾 save to SQLite
                rows.append(result)
            else:
                demo = _make_demo_result(d, seed)
                rows.append(demo)        # demo ไม่ save ลง DB
        bar.empty()

    if not rows:
        st.warning("⚠️  ไม่สามารถเชื่อมต่อ GLO API ได้ กำลังใช้ข้อมูลสาธิต")
        rows = [_make_demo_result(d, int(d.replace("/", "")) % 9999997) for d in dates]

    df = pd.DataFrame(rows)
    df["date_parsed"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    df = df.sort_values("date_parsed", ascending=False).reset_index(drop=True)
    return df

# ══════════════════════════════════════════════════════════
# STATISTICAL ANALYSIS
# ══════════════════════════════════════════════════════════
def extract_digits(df: pd.DataFrame) -> dict[str, list[int]]:
    """Extract digit series from prize1 by position."""
    digits = {"units": [], "tens": [], "hundreds": [],
               "thousands": [], "ten_thousands": [], "hundred_thousands": []}
    positions = list(digits.keys())
    for p in df["prize1"].dropna():
        p = str(p).zfill(6)
        if len(p) == 6:
            for idx, pos in enumerate(positions):
                digits[pos].append(int(p[-(idx + 1)]))  # right-to-left
    return digits

def frequency_analysis(digits: dict) -> dict[str, Counter]:
    return {pos: Counter(d) for pos, d in digits.items()}

def compute_poisson_prob(digits: dict, n_draws: int) -> dict[str, dict[int, float]]:
    """
    Poisson probability of each digit appearing ≥1 time next draw.
    λ = average occurrences per draw; P(X≥1) = 1 - e^(-λ)
    """
    probs = {}
    for pos, vals in digits.items():
        counts = Counter(vals)
        probs[pos] = {}
        for d in range(10):
            lam = counts.get(d, 0) / n_draws
            probs[pos][d] = 1 - poisson.pmf(0, lam) if lam > 0 else 0.001
    return probs

def time_series_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute rolling even/odd & high/low ratios for prize1."""
    p1 = df["prize1"].dropna().astype(str).str.zfill(6)
    last2 = p1.str[-2:].astype(int)
    rows = []
    for i, row in df.iterrows():
        n2 = int(str(row["prize1"]).zfill(6)[-2:])
        rows.append({
            "date":  row.get("date_parsed", row["date"]),
            "last2": n2,
            "is_even": n2 % 2 == 0,
            "is_high": n2 >= 50,
        })
    tdf = pd.DataFrame(rows)
    tdf["rolling_even"] = tdf["is_even"].rolling(5, min_periods=1).mean() * 100
    tdf["rolling_high"] = tdf["is_high"].rolling(5, min_periods=1).mean() * 100
    return tdf.sort_values("date")

def compute_consecutive_absence(df: pd.DataFrame) -> dict[str, dict[int, int]]:
    """Count how many draws each digit has NOT appeared (absence streak)."""
    positions = ["units", "tens", "hundreds"]
    streaks = {p: {d: 0 for d in range(10)} for p in positions}

    for _, row in df.iterrows():
        p1 = str(row["prize1"]).zfill(6)
        if len(p1) != 6:
            continue
        for idx, pos in enumerate(positions):
            seen_digit = int(p1[-(idx + 1)])
            for d in range(10):
                if d == seen_digit:
                    streaks[pos][d] = 0
                else:
                    streaks[pos][d] += 1
    return streaks

# ══════════════════════════════════════════════════════════
# BAYESIAN PREDICTION ENGINE
# ══════════════════════════════════════════════════════════
def bayesian_predict(df: pd.DataFrame, n_draws: int = 52) -> dict:
    """
    Bayesian Inference prediction.
    Prior  : uniform Dirichlet (weak)
    Likelihood : frequency of each digit per position
    Update factors:
      - Absence streak (cold = higher posterior)
      - Poisson readiness score
      - Last-5 trend momentum
    Returns top picks for last 2 and last 3 digits.
    """
    digits   = extract_digits(df)
    freq     = frequency_analysis(digits)
    poisson_ = compute_poisson_prob(digits, n_draws)
    absence  = compute_consecutive_absence(df)

    positions = ["units", "tens", "hundreds"]
    posterior = {}

    for pos in positions:
        scores = {}
        for d in range(10):
            # Prior: uniform → alpha=1
            prior = 1.0

            # Likelihood: frequency-based
            cnt   = freq[pos].get(d, 0)
            total = sum(freq[pos].values()) or 1
            like  = (cnt + 1) / (total + 10)      # Laplace smoothed

            # Absence factor: longer absence → higher readiness
            abs_streak    = absence[pos].get(d, 0)
            absence_score = 1 + (abs_streak / n_draws) * 2.5

            # Poisson readiness
            p_ready = poisson_[pos].get(d, 0.1)

            # Last-5 trend (recency bias weight = 1.3 if appeared)
            last5_digits = [int(str(r).zfill(6)[-(list(positions).index(pos) + 1)])
                            for r in df["prize1"].head(5).dropna()]
            recency = 1.3 if d in last5_digits else 1.0

            # Posterior ∝ prior × likelihood × factors
            posterior[pos] = posterior.get(pos, {})
            posterior[pos][d] = prior * like * absence_score * p_ready * recency

        # Normalise
        total_post = sum(posterior[pos].values())
        posterior[pos] = {d: v / total_post for d, v in posterior[pos].items()}

    def top_digits(pos, n=3):
        return sorted(posterior[pos], key=lambda d: posterior[pos][d], reverse=True)[:n]

    def confidence(pos, d):
        return round(posterior[pos][d] * 100, 1)

    # Build 3 prediction sets
    u_top = top_digits("units", 3)
    t_top = top_digits("tens",  3)
    h_top = top_digits("hundreds", 3)

    def form_numbers_2d(u_list, t_list):
        nums = set()
        for t in t_list:
            for u in u_list:
                nums.add(f"{t}{u}")
        return sorted(nums)[:5]

    def form_numbers_3d(h_list, t_list, u_list):
        nums = set()
        for h in h_list:
            for t in t_list:
                for u in u_list:
                    nums.add(f"{h}{t}{u}")
        return sorted(nums, key=lambda x: -(
            posterior["hundreds"][int(x[0])] +
            posterior["tens"][int(x[1])] +
            posterior["units"][int(x[2])]
        ))[:5]

    sets_2d = {
        "primary":   form_numbers_2d(u_top[:2], t_top[:2]),
        "secondary": form_numbers_2d(u_top[1:3], t_top[1:3]),
        "hedge":     form_numbers_2d([u_top[-1]], [t_top[-1]]),
    }
    sets_3d = {
        "primary":   form_numbers_3d(h_top[:2], t_top[:2], u_top[:2]),
        "secondary": form_numbers_3d(h_top[1:], t_top[1:], u_top[1:]),
        "hedge":     form_numbers_3d([h_top[-1]], [t_top[-1]], [u_top[-1]]),
    }

    conf_score = {
        "primary":   round(np.mean([confidence("units", u_top[0]),
                                    confidence("tens",  t_top[0]),
                                    confidence("hundreds", h_top[0])]), 1),
        "secondary": round(np.mean([confidence("units", u_top[1]),
                                    confidence("tens",  t_top[1]),
                                    confidence("hundreds", h_top[1])]), 1),
        "hedge":     round(np.mean([confidence("units", u_top[2]),
                                    confidence("tens",  t_top[2]),
                                    confidence("hundreds", h_top[2])]), 1),
    }

    return {
        "sets_2d": sets_2d,
        "sets_3d": sets_3d,
        "confidence": conf_score,
        "posterior":  posterior,
        "top_digits": {"units": u_top, "tens": t_top, "hundreds": h_top},
    }

# ══════════════════════════════════════════════════════════
# CHART BUILDERS
# ══════════════════════════════════════════════════════════
def chart_frequency_heatmap(freq: dict) -> go.Figure:
    positions = ["units", "tens", "hundreds", "thousands", "ten_thousands", "hundred_thousands"]
    labels    = ["หน่วย", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน"]
    matrix = np.zeros((10, len(positions)))
    for j, pos in enumerate(positions):
        total = sum(freq[pos].values()) or 1
        for d in range(10):
            matrix[d][j] = round(freq[pos].get(d, 0) / total * 100, 1)

    fig = go.Figure(go.Heatmap(
        z=matrix,
        x=labels,
        y=[str(d) for d in range(10)],
        colorscale=[[0, "#0f1628"], [0.3, "#1e2a4a"], [0.6, "#f5c842"], [1, "#ff4560"]],
        text=matrix.round(1),
        texttemplate="%{text}%",
        textfont=dict(size=11, family="IBM Plex Mono"),
        showscale=True,
        colorbar=dict(title=dict(text="ความถี่ %", font=dict(color="#7986cb"))),
    ))
    fig.update_layout(
        title="🔥 Frequency Heatmap — ความถี่เลขแต่ละหลัก (%)",
        **CHART_TEMPLATE,
        height=350,
    )
    return fig

def chart_hot_cold_bar(freq: dict, pos: str, label: str) -> go.Figure:
    counts = [freq[pos].get(d, 0) for d in range(10)]
    colors = ["#ff4560" if c >= np.percentile(counts, 70) else
              "#00d4ff" if c <= np.percentile(counts, 30) else "#f5c842"
              for c in counts]
    fig = go.Figure(go.Bar(
        x=[str(d) for d in range(10)],
        y=counts,
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0.3)", width=1)),
        text=counts,
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=12),
    ))
    fig.update_layout(
        title=f"📊 Hot/Cold — หลัก{label}",
        xaxis_title="เลข",
        yaxis_title="ความถี่",
        **CHART_TEMPLATE,
        height=300,
        showlegend=False,
    )
    return fig

def chart_poisson_readiness(poisson_probs: dict, pos: str, label: str) -> go.Figure:
    probs  = [poisson_probs[pos].get(d, 0) * 100 for d in range(10)]
    colors = [f"rgba(245,200,66,{0.3 + p/150})" for p in probs]
    fig = go.Figure(go.Bar(
        x=[str(d) for d in range(10)],
        y=probs,
        marker=dict(color=colors, line=dict(color="#f5c842", width=1)),
        text=[f"{p:.1f}%" for p in probs],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=11, color="#f5c842"),
    ))
    fig.update_layout(
        title=f"🎲 Poisson Readiness — หลัก{label} (โอกาสออกงวดหน้า %)",
        xaxis_title="เลข",
        yaxis_title="ความน่าจะเป็น (%)",
        **CHART_TEMPLATE,
        height=300,
    )
    return fig

def chart_time_series(ts_df: pd.DataFrame) -> go.Figure:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=["เลขท้าย 2 ตัว (รางวัลที่ 1)", "% คู่/สูง แบบ Rolling 5 งวด"],
                        vertical_spacing=0.12)
    fig.add_trace(go.Scatter(
        x=ts_df["date"], y=ts_df["last2"],
        mode="lines+markers",
        line=dict(color="#00d4ff", width=1.5),
        marker=dict(size=5, color="#f5c842"),
        name="เลขท้าย 2 ตัว",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=ts_df["date"], y=ts_df["rolling_even"],
        mode="lines", fill="tozeroy",
        line=dict(color="#00ff88", width=2),
        fillcolor="rgba(0,255,136,0.1)",
        name="% เลขคู่",
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=ts_df["date"], y=ts_df["rolling_high"],
        mode="lines", fill="tozeroy",
        line=dict(color="#8b5cf6", width=2),
        fillcolor="rgba(139,92,246,0.1)",
        name="% เลขสูง (≥50)",
    ), row=2, col=1)
    fig.add_hline(y=50, line_dash="dash", line_color="rgba(255,255,255,0.2)",
                  annotation_text="50%", row=2, col=1)
    fig.update_layout(
        title="📈 Time-Series Pattern Analysis",
        **CHART_TEMPLATE,
        height=420,
        legend=dict(orientation="h", y=-0.08),
    )
    return fig

def chart_posterior(posterior: dict) -> go.Figure:
    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=["หน่วย (Posterior)", "สิบ (Posterior)", "ร้อย (Posterior)"])
    positions = ["units", "tens", "hundreds"]
    colors    = ["#ff4560", "#00d4ff", "#f5c842"]
    for j, (pos, col) in enumerate(zip(positions, colors)):
        probs = [posterior[pos].get(d, 0) * 100 for d in range(10)]
        fig.add_trace(go.Bar(
            x=[str(d) for d in range(10)],
            y=probs,
            marker=dict(color=[f"rgba{tuple(int(col.lstrip('#')[i:i+2], 16) for i in (0,2,4)) + (0.6,)}"
                                if p < max(probs) * 0.8 else col for p in probs]),
            name=pos,
            showlegend=False,
        ), row=1, col=j+1)
    fig.update_layout(
        title="🔮 Bayesian Posterior Distribution",
        **CHART_TEMPLATE,
        height=320,
    )
    return fig

def chart_absence_heatmap(absence: dict) -> go.Figure:
    positions = ["units", "tens", "hundreds"]
    labels    = ["หน่วย", "สิบ", "ร้อย"]
    matrix = np.array([[absence[p].get(d, 0) for p in positions] for d in range(10)], dtype=float)
    fig = go.Figure(go.Heatmap(
        z=matrix,
        x=labels,
        y=[str(d) for d in range(10)],
        colorscale=[[0, "#0f1628"], [0.5, "#1a3a5c"], [1, "#00d4ff"]],
        text=matrix.astype(int),
        texttemplate="%{text} งวด",
        textfont=dict(size=11, family="IBM Plex Mono"),
        showscale=True,
        colorbar=dict(title=dict(text="งวดที่ไม่ออก", font=dict(color="#7986cb"))),
    ))
    fig.update_layout(
        title="🧊 Absence Streak Heatmap — เลขที่ไม่ออกมากี่งวดแล้ว",
        **CHART_TEMPLATE,
        height=340,
    )
    return fig

# ══════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════
def main():
    # ── SIDEBAR ──────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚙️ ตั้งค่า")
        n_draws = st.slider("จำนวนงวดย้อนหลัง", 20, 52, 40, 2,
                            help="ยิ่งมากยิ่งแม่น แต่ใช้เวลานาน")
        st.divider()
        st.markdown("### 📅 งวดปัจจุบัน")
        draws    = get_draw_dates(2)
        next_draw = draws[0]
        st.info(f"**{next_draw}** (งวดล่าสุด)")
        st.divider()
        refresh = st.button("🔄  Refresh ข้อมูล", use_container_width=True)
        if refresh:
            st.cache_data.clear()
            st.rerun()
        st.divider()
        # DB stats
        cached_n = db_count()
        st.markdown(f"""
<div style='background:#0f1628;border:1px solid #1e2a4a;border-radius:8px;padding:12px;
  font-family:IBM Plex Mono;font-size:0.72rem;color:#7986cb;line-height:2'>
<div style='color:#00ff88;margin-bottom:4px'>💾 SQLite Cache</div>
บันทึกแล้ว: <b style='color:#e8eaf6'>{cached_n} งวด</b><br>
ไฟล์: <span style='color:#f5c842'>glo_cache.db</span>
</div>
""", unsafe_allow_html=True)
        if st.button("🗑️  ล้าง Cache DB", use_container_width=True):
            db_clear()
            st.cache_data.clear()
            st.success("ล้างแล้ว!")
            st.rerun()
        st.divider()
        st.markdown("""
<div style='font-family:IBM Plex Mono;font-size:0.7rem;color:#7986cb;line-height:1.8'>
⚠️ <b>คำเตือน</b><br>
ระบบนี้ใช้เพื่อวัตถุประสงค์<br>
ทางสถิติและการศึกษาเท่านั้น<br>
ผลลัพธ์ไม่ใช่การรับประกัน<br>
ความถูกต้องในอนาคต
</div>
""", unsafe_allow_html=True)

    # ── HEADER ───────────────────────────────────────────
    st.markdown(f"""
<div class="main-header">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px">
    <div>
      <h1>🎯 GLO Analytics Pro</h1>
      <div class="subtitle">วิเคราะห์สลากกินแบ่งรัฐบาล · Bayesian Prediction Engine · Real-time Data</div>
    </div>
    <div style="text-align:right">
      <div class="live-badge"><span class="live-dot"></span>LIVE DATA</div>
      <div style="font-family:IBM Plex Mono;font-size:0.75rem;color:#7986cb;margin-top:6px">
        Updated: {datetime.now().strftime('%d %b %Y %H:%M')}
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── LOAD DATA ─────────────────────────────────────────
    with st.spinner(""):
        df = load_historical_data(n_draws)

    if df.empty:
        st.error("❌ ไม่สามารถโหลดข้อมูลได้ กรุณาลองใหม่อีกครั้ง")
        return

    latest = df.iloc[0]
    digits    = extract_digits(df)
    freq      = frequency_analysis(digits)
    poisson_p = compute_poisson_prob(digits, len(df))
    ts_df     = time_series_analysis(df)
    absence   = compute_consecutive_absence(df)
    prediction = bayesian_predict(df, len(df))

    # ── KPI ROW ───────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    p1_str = str(latest["prize1"]).zfill(6)

    with k1:
        st.markdown(f"""
<div class="kpi-card" style="--accent-color:#f5c842">
  <div class="kpi-label">🏆 รางวัลที่ 1 งวดล่าสุด</div>
  <div class="kpi-value" style="color:#f5c842;font-size:2.8rem;letter-spacing:6px">{p1_str}</div>
  <div class="kpi-sub">งวด {latest['date']}</div>
</div>""", unsafe_allow_html=True)

    with k2:
        b2 = str(latest.get("back2", "??")).zfill(2)
        st.markdown(f"""
<div class="kpi-card" style="--accent-color:#00d4ff">
  <div class="kpi-label">🎴 เลขท้าย 2 ตัว</div>
  <div class="kpi-value" style="color:#00d4ff;letter-spacing:4px">{b2}</div>
  <div class="kpi-sub">เลขท้าย 2 ตัว รางวัลที่ 1</div>
</div>""", unsafe_allow_html=True)

    with k3:
        b3 = latest.get("back3", ["???"])
        b3_str = " / ".join(b3) if isinstance(b3, list) else str(b3)
        st.markdown(f"""
<div class="kpi-card" style="--accent-color:#00ff88">
  <div class="kpi-label">🎴 เลขท้าย 3 ตัว</div>
  <div class="kpi-value" style="color:#00ff88;font-size:1.6rem">{b3_str}</div>
  <div class="kpi-sub">เลขท้าย 3 ตัว (ล่าง)</div>
</div>""", unsafe_allow_html=True)

    with k4:
        f3 = latest.get("front3", ["???"])
        f3_str = " / ".join(f3) if isinstance(f3, list) else str(f3)
        st.markdown(f"""
<div class="kpi-card" style="--accent-color:#8b5cf6">
  <div class="kpi-label">🎴 เลขหน้า 3 ตัว</div>
  <div class="kpi-value" style="color:#8b5cf6;font-size:1.6rem">{f3_str}</div>
  <div class="kpi-sub">เลขหน้า 3 ตัว (บน)</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MAIN TABS ─────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔮 Prediction Engine",
        "🔥 Frequency Analysis",
        "🎲 Poisson & Readiness",
        "📈 Time-Series",
        "📋 ตารางข้อมูล",
    ])

    # ════ TAB 1: PREDICTION ENGINE ════
    with tab1:
        st.markdown('<div class="section-header">🔮 Bayesian Prediction Engine — เลขเด่นงวดหน้า</div>', unsafe_allow_html=True)

        def pred_card(title, emoji, color, numbers_2d, numbers_3d, conf, desc):
            nums2 = "  ".join([f'<span class="pred-num" style="border-color:{color};color:{color};background:rgba(0,0,0,0.3)">{n}</span>' for n in numbers_2d])
            nums3 = "  ".join([f'<span class="pred-num" style="border-color:{color};color:{color};font-size:1.6rem;background:rgba(0,0,0,0.3)">{n}</span>' for n in numbers_3d])
            st.markdown(f"""
<div class="pred-card" style="border-color:{color}20;border-left:3px solid {color}">
  <div class="pred-tier" style="color:{color}">{emoji} {title}</div>
  <div style="font-size:0.78rem;color:#7986cb;margin-bottom:10px">{desc}</div>
  <div style="font-size:0.78rem;color:#7986cb;font-family:IBM Plex Mono;margin-bottom:6px">เลขท้าย 2 ตัว</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">{nums2}</div>
  <div style="font-size:0.78rem;color:#7986cb;font-family:IBM Plex Mono;margin:10px 0 6px">เลขท้าย 3 ตัว</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">{nums3}</div>
  <div class="pred-confidence">Confidence Score: <span style="color:{color}">{conf}%</span></div>
</div>
<br>
""", unsafe_allow_html=True)

        col_l, col_r = st.columns([3, 1])
        with col_l:
            pred_card(
                "ชุดเน้น — ความมั่นใจสูงสุด", "🥇", "#f5c842",
                prediction["sets_2d"]["primary"],
                prediction["sets_3d"]["primary"],
                prediction["confidence"]["primary"],
                "คำนวณจาก Posterior Distribution สูงสุด × Poisson Readiness × Absence Streak"
            )
            pred_card(
                "ชุดรอง — สำรอง", "🥈", "#00d4ff",
                prediction["sets_2d"]["secondary"],
                prediction["sets_3d"]["secondary"],
                prediction["confidence"]["secondary"],
                "เลขที่มีน้ำหนัก Posterior รองลงมา เหมาะสำหรับกระจายความเสี่ยง"
            )
            pred_card(
                "ชุดกันเหนียว — Hedge Set", "🧿", "#8b5cf6",
                prediction["sets_2d"]["hedge"],
                prediction["sets_3d"]["hedge"],
                prediction["confidence"]["hedge"],
                "เลขที่หายไปนานที่สุด (Cold streak สูง) มีโอกาส 'สุกงอม' พร้อมออก"
            )

        with col_r:
            st.markdown("""
<div style="background:#0f1628;border:1px solid #1e2a4a;border-radius:10px;padding:16px;font-family:IBM Plex Mono;font-size:0.72rem;color:#7986cb;line-height:2">
<div style="color:#f5c842;font-size:0.85rem;margin-bottom:8px">📖 วิธีอ่านผล</div>
<b style="color:#e8eaf6">Bayesian Inference</b><br>
P(เลข|ข้อมูล) ∝<br>
P(ข้อมูล|เลข) × P(เลข)<br><br>
<b style="color:#00d4ff">Factors:</b><br>
• Frequency likelihood<br>
• Poisson λ readiness<br>
• Absence streak score<br>
• Recency momentum<br><br>
<b style="color:#00ff88">ชุดเน้น</b> = ผลรวม Posterior สูงสุด<br>
<b style="color:#00d4ff">ชุดรอง</b> = อันดับ 2<br>
<b style="color:#8b5cf6">กันเหนียว</b> = Cold streak นาน<br><br>
<div style="color:#ff4560">⚠️ ไม่ใช่การรับประกัน</div>
</div>
""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.plotly_chart(chart_posterior(prediction["posterior"]), use_container_width=True)

    # ════ TAB 2: FREQUENCY ANALYSIS ════
    with tab2:
        st.markdown('<div class="section-header">🔥 Frequency Analysis — ความถี่เลข Hot & Cold</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_frequency_heatmap(freq), use_container_width=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.plotly_chart(chart_hot_cold_bar(freq, "units",    "หน่วย"),   use_container_width=True)
        with c2: st.plotly_chart(chart_hot_cold_bar(freq, "tens",     "สิบ"),     use_container_width=True)
        with c3: st.plotly_chart(chart_hot_cold_bar(freq, "hundreds", "ร้อย"),   use_container_width=True)

        st.plotly_chart(chart_absence_heatmap(absence), use_container_width=True)

        # Hot/Cold summary table
        st.markdown('<div class="section-header">📊 สรุปเลข Hot & Cold</div>', unsafe_allow_html=True)
        summary_rows = []
        for pos, label in [("units","หน่วย"),("tens","สิบ"),("hundreds","ร้อย")]:
            sorted_freq = sorted(freq[pos].items(), key=lambda x: x[1], reverse=True)
            hot  = [str(d) for d,_ in sorted_freq[:3]]
            cold = [str(d) for d,_ in sorted_freq[-3:]]
            summary_rows.append({"หลัก": label,
                                  "🔥 Hot (ออกบ่อย)":    " · ".join(hot),
                                  "🧊 Cold (ไม่ค่อยออก)": " · ".join(cold)})
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    # ════ TAB 3: POISSON ════
    with tab3:
        st.markdown('<div class="section-header">🎲 Poisson Distribution — โอกาสออกงวดหน้า</div>', unsafe_allow_html=True)
        st.markdown("""
<div style="background:#0f1628;border:1px solid #1e2a4a;border-radius:8px;padding:14px;font-family:IBM Plex Mono;font-size:0.78rem;color:#7986cb;margin-bottom:16px">
λ (lambda) = จำนวนครั้งที่เลขนั้นออกเฉลี่ยต่องวด  |  P(X≥1) = 1 - e^(-λ)  — ความน่าจะเป็นที่จะออกอย่างน้อย 1 ครั้ง
</div>
""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.plotly_chart(chart_poisson_readiness(poisson_p, "units",    "หน่วย"),   use_container_width=True)
        with c2: st.plotly_chart(chart_poisson_readiness(poisson_p, "tens",     "สิบ"),     use_container_width=True)
        with c3: st.plotly_chart(chart_poisson_readiness(poisson_p, "hundreds", "ร้อย"),   use_container_width=True)

        # Poisson table
        pos_labels = {"units":"หน่วย","tens":"สิบ","hundreds":"ร้อย"}
        rows = []
        for d in range(10):
            row = {"เลข": str(d)}
            for p, lbl in pos_labels.items():
                prob = poisson_p[p].get(d, 0) * 100
                row[f"หลัก{lbl} (%)"] = f"{prob:.1f}%"
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ════ TAB 4: TIME-SERIES ════
    with tab4:
        st.markdown('<div class="section-header">📈 Time-Series Pattern — แนวโน้มย้อนหลัง</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_time_series(ts_df), use_container_width=True)

        # Last 2-digit distribution
        back2_vals = df["back2"].dropna().astype(str).str.zfill(2).tolist()
        back2_int  = [int(v) for v in back2_vals if v.isdigit()]
        fig_dist = go.Figure(go.Histogram(
            x=back2_int, nbinsx=25,
            marker=dict(color="#00d4ff", line=dict(color="rgba(0,0,0,0.3)", width=1)),
        ))
        fig_dist.update_layout(
            title="📊 Distribution — เลขท้าย 2 ตัว ย้อนหลัง",
            xaxis_title="เลขท้าย 2 ตัว",
            yaxis_title="ความถี่",
            **CHART_TEMPLATE, height=280,
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    # ════ TAB 5: TABLE ════
    with tab5:
        st.markdown('<div class="section-header">📋 ตารางผลสลากย้อนหลัง</div>', unsafe_allow_html=True)
        display_df = df[["date", "prize1", "back2", "back3", "front3"]].copy()
        display_df.columns = ["งวด", "รางวัลที่ 1", "เลขท้าย 2 ตัว", "เลขท้าย 3 ตัว (ล่าง)", "เลขหน้า 3 ตัว (บน)"]
        display_df["เลขท้าย 3 ตัว (ล่าง)"] = display_df["เลขท้าย 3 ตัว (ล่าง)"].apply(
            lambda x: " / ".join(x) if isinstance(x, list) else str(x))
        display_df["เลขหน้า 3 ตัว (บน)"] = display_df["เลขหน้า 3 ตัว (บน)"].apply(
            lambda x: " / ".join(x) if isinstance(x, list) else str(x))
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=600)
        csv = display_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️  ดาวน์โหลด CSV", csv, "glo_history.csv", "text/csv", use_container_width=True)

    # ── FOOTER ───────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;margin-top:32px;padding:16px;border-top:1px solid #1e2a4a;
  font-family:IBM Plex Mono;font-size:0.72rem;color:#7986cb">
  GLO Analytics Pro · Powered by Streamlit · Data: สำนักงานสลากกินแบ่งรัฐบาล (GLO) <br>
  ⚠️ เพื่อการศึกษาทางสถิติเท่านั้น — ไม่รับประกันความถูกต้องของการทำนาย
</div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
