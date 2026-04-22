import math
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Blast Cost Estimator", layout="wide", page_icon="💣")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400;1,600;1,700&family=Lora:ital,wght@0,400;0,600;1,400;1,600&family=DM+Mono:ital,wght@0,300;0,400;1,300;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300;1,400;1,600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #EEE9E0 !important;
    color: #1A1A18 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer { visibility: hidden; }

[data-testid="stAppViewContainer"] > .main > .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ═══════════════════════════
   MASTHEAD
═══════════════════════════ */
.masthead {
    background: #1A2E1A;
    padding: 52px 72px 44px;
    position: relative;
    overflow: hidden;
}
.masthead::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 80px,
            rgba(255,255,255,0.012) 80px,
            rgba(255,255,255,0.012) 81px
        );
    pointer-events: none;
}
.masthead::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #C0392B 0%, #E05A3A 40%, transparent 100%);
}
.mh-eyebrow {
    font-family: 'DM Mono', monospace;
    font-style: italic;
    font-size: 10px;
    letter-spacing: 6px;
    color: #6B9E6B;
    text-transform: uppercase;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.mh-eyebrow::before {
    content: '';
    display: inline-block;
    width: 28px;
    height: 1px;
    background: #6B9E6B;
}
.mh-title {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 700;
    font-size: 58px;
    color: #EEE9E0;
    line-height: 1.0;
    letter-spacing: -1.5px;
    margin-bottom: 12px;
}
.mh-title em {
    color: #C0392B;
    font-style: italic;
}
.mh-desc {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 300;
    font-size: 16px;
    color: #5A7A5A;
    letter-spacing: 2px;
    margin-top: 6px;
}

/* ═══════════════════════════
   PAGE BODY
═══════════════════════════ */
.page-body {
    padding: 52px 72px 64px;
}

/* ═══════════════════════════
   SECTION RULE
═══════════════════════════ */
.sec-rule {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 0 0 32px 0;
}
.sec-rule-icon {
    font-size: 16px;
    line-height: 1;
}
.sec-rule-txt {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 6px;
    color: #1A2E1A;
    text-transform: uppercase;
}
.sec-rule-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1A2E1A 0%, transparent 100%);
    opacity: 0.18;
}

/* ═══════════════════════════
   INPUT CARDS — underline style
═══════════════════════════ */
.inp-card {
    background: #F8F4EE;
    border-radius: 3px;
    padding: 22px 24px 18px;
    margin-bottom: 18px;
    border-top: 3px solid #1A2E1A;
    transition: box-shadow 0.2s, transform 0.2s;
    position: relative;
}
.inp-card:hover {
    box-shadow: 4px 4px 0 #D4CECC;
    transform: translateY(-1px);
}
.inp-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
}
.inp-card-icon {
    font-size: 15px;
    opacity: 0.9;
}
.inp-card-label {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 12px;
    font-weight: 600;
    color: #1A2E1A;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ═══════════════════════════
   STREAMLIT INPUT OVERRIDES
═══════════════════════════ */
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid #B8B0A8 !important;
    border-radius: 0 !important;
    color: #1A1A18 !important;
    font-family: 'DM Mono', monospace !important;
    font-style: italic !important;
    font-size: 24px !important;
    font-weight: 300 !important;
    padding: 6px 2px 10px !important;
    letter-spacing: 0.5px !important;
    box-shadow: none !important;
    outline: none !important;
    transition: border-color 0.2s !important;
    width: 100% !important;
}
[data-testid="stTextInput"] input:focus {
    border-bottom-color: #C0392B !important;
    box-shadow: 0 2px 0 0 rgba(192,57,43,0.12) !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #C0B8B0 !important;
    font-size: 14px !important;
    font-style: italic !important;
}
[data-testid="stTextInput"] label { display: none !important; }
[data-testid="stTextInput"] > div,
[data-testid="stTextInput"] > div > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ═══════════════════════════
   CALCULATE BUTTON — pill/round
═══════════════════════════ */
.stButton > button {
    background: #C0392B !important;
    color: #F8F4EE !important;
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    font-weight: 700 !important;
    font-size: 17px !important;
    letter-spacing: 1.5px !important;
    border: none !important;
    border-radius: 9999px !important;
    padding: 18px 56px !important;
    width: 100% !important;
    margin-top: 28px !important;
    cursor: pointer !important;
    box-shadow: 0 6px 20px rgba(192,57,43,0.28) !important;
    transition: background 0.2s, box-shadow 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    background: #A93226 !important;
    box-shadow: 0 10px 28px rgba(192,57,43,0.38) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 4px 12px rgba(192,57,43,0.22) !important;
}

/* ═══════════════════════════
   RESULTS AREA
═══════════════════════════ */
.results-shell {
    background: #1A2E1A;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 12px;
}

.res-header {
    padding: 22px 36px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex;
    align-items: center;
    gap: 14px;
}
.res-header-icon { font-size: 16px; }
.res-header-txt {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 300;
    font-size: 11px;
    letter-spacing: 6px;
    color: #6B9E6B;
    text-transform: uppercase;
}

.res-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1px;
    background: rgba(255,255,255,0.04);
}
.res-block {
    background: #1A2E1A;
    padding: 28px 32px;
    transition: background 0.18s;
    position: relative;
    overflow: hidden;
}
.res-block:hover { background: #213621; }
.res-block::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: #C0392B;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.25s ease;
}
.res-block:hover::after { transform: scaleX(1); }

.res-block-label {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 300;
    font-size: 12px;
    color: #5A7A5A;
    letter-spacing: 2px;
    margin-bottom: 10px;
    text-transform: lowercase;
}
.res-block-val {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 700;
    font-size: 32px;
    color: #EEE9E0;
    line-height: 1;
    letter-spacing: -0.5px;
}
.res-block-unit {
    font-family: 'DM Mono', monospace;
    font-style: italic;
    font-size: 10px;
    color: #3A5A3A;
    letter-spacing: 3px;
    margin-top: 7px;
    text-transform: uppercase;
}

/* powder factor gets accent colour */
.res-block.accent { background: #142014; }
.res-block.accent .res-block-val { color: #88CC88; }
.res-block.accent .res-block-label { color: #4A7A4A; }

/* ═══════════════════════════
   COST STRIP
═══════════════════════════ */
.cost-strip {
    background: #C0392B;
    padding: 32px 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    border-top: 1px solid rgba(255,255,255,0.08);
}
.cost-lhs-label {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 300;
    font-size: 11px;
    letter-spacing: 5px;
    color: rgba(238,233,224,0.65);
    text-transform: uppercase;
    margin-bottom: 5px;
}
.cost-lhs-note {
    font-family: 'DM Mono', monospace;
    font-style: italic;
    font-size: 11px;
    color: rgba(238,233,224,0.45);
    letter-spacing: 1px;
}
.cost-figure {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 700;
    font-size: 52px;
    color: #EEE9E0;
    line-height: 1;
    letter-spacing: -2px;
    text-shadow: 0 2px 16px rgba(0,0,0,0.2);
}

/* ═══════════════════════════
   TIMESTAMP
═══════════════════════════ */
.ts-line {
    font-family: 'DM Mono', monospace;
    font-style: italic;
    font-size: 9px;
    letter-spacing: 3px;
    color: #5A7A5A;
    text-align: right;
    padding: 14px 36px;
    background: #142014;
    text-transform: uppercase;
    border-top: 1px solid rgba(255,255,255,0.04);
}

/* ═══════════════════════════
   ERROR
═══════════════════════════ */
.err-shell {
    background: #FDF0EE;
    border: 1px solid #E8C0BC;
    border-left: 5px solid #C0392B;
    border-radius: 3px;
    padding: 18px 24px;
    margin-top: 18px;
}
.err-item {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 13px;
    color: #C0392B;
    line-height: 2.2;
    display: flex;
    align-items: center;
    gap: 8px;
}
.err-bullet { font-style: normal; font-size: 10px; opacity: 0.6; }
</style>
""", unsafe_allow_html=True)


# ── BACKEND ──────────────────────────────────────────────────

def run_design(bench_height, hole_diameter, rock_density,
               explosive_density, unit_cost, area):
    burden    = 25 * hole_diameter * (1 / rock_density)
    spacing   = 1.25 * burden
    holes     = max(1, int(area / (burden * spacing)))
    radius    = hole_diameter / 2
    charge    = math.pi * (radius ** 2) * bench_height * explosive_density
    total_exp = charge * holes
    rock_vol  = area * bench_height
    pf        = total_exp / rock_vol
    cost      = total_exp * unit_cost
    return dict(burden=burden, spacing=spacing, holes=holes, charge=charge,
                total_exp=total_exp, rock_vol=rock_vol, pf=pf, cost=cost)


# ── MASTHEAD ─────────────────────────────────────────────────

st.markdown("""
<div class="masthead">
    <div class="mh-eyebrow">💣 &nbsp; Open-Pit Mining</div>
    <div class="mh-title">Blast Design &amp;<br><em>Cost Estimation</em></div>
    <div class="mh-desc">Drill &amp; Blast Engineering &nbsp;·&nbsp; Bench Analysis Tool</div>
</div>
""", unsafe_allow_html=True)

# ── INPUTS ───────────────────────────────────────────────────

st.markdown("""
<div class="page-body" style="padding-bottom:0;">
    <div class="sec-rule">
        <span class="sec-rule-icon">⚙️</span>
        <span class="sec-rule-txt">Input Parameters</span>
        <span class="sec-rule-line"></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Padding spacer
st.markdown('<div style="padding: 0 72px;">', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown("""
    <div class="inp-card">
        <div class="inp-card-header">
            <span class="inp-card-icon">📏</span>
            <span class="inp-card-label">Bench Height</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    t_bench = st.text_input("_bench_height", value="10.0", placeholder="e.g. 10.0", label_visibility="hidden", key="bench")

    st.markdown("""
    <div class="inp-card" style="margin-top:4px;">
        <div class="inp-card-header">
            <span class="inp-card-icon">🕳️</span>
            <span class="inp-card-label">Hole Diameter</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    t_hole = st.text_input("_hole_dia", value="0.115", placeholder="e.g. 0.115", label_visibility="hidden", key="hole")

with c2:
    st.markdown("""
    <div class="inp-card">
        <div class="inp-card-header">
            <span class="inp-card-icon">🪨</span>
            <span class="inp-card-label">Rock Density</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    t_rock = st.text_input("_rock_den", value="2.7", placeholder="e.g. 2.7", label_visibility="hidden", key="rock")

    st.markdown("""
    <div class="inp-card" style="margin-top:4px;">
        <div class="inp-card-header">
            <span class="inp-card-icon">💥</span>
            <span class="inp-card-label">Explosive Density</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    t_expden = st.text_input("_exp_den", value="0.85", placeholder="e.g. 0.85", label_visibility="hidden", key="expden")

with c3:
    st.markdown("""
    <div class="inp-card">
        <div class="inp-card-header">
            <span class="inp-card-icon">📐</span>
            <span class="inp-card-label">Bench Area</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    t_area = st.text_input("_area", value="5000", placeholder="e.g. 5000", label_visibility="hidden", key="area")

    st.markdown("""
    <div class="inp-card" style="margin-top:4px;">
        <div class="inp-card-header">
            <span class="inp-card-icon">💰</span>
            <span class="inp-card-label">Unit Cost ($/t)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    t_cost = st.text_input("_unit_cost", value="450", placeholder="e.g. 450", label_visibility="hidden", key="cost")

st.markdown('</div>', unsafe_allow_html=True)

# ── BUTTON ───────────────────────────────────────────────────

st.markdown('<div style="padding: 0 72px;">', unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    run = st.button("Estimate Cost")
st.markdown('</div>', unsafe_allow_html=True)


# ── CALCULATE ────────────────────────────────────────────────

if run:
    errors = []

    def parse(val, name):
        try:
            v = float(val)
            if v <= 0:
                errors.append(f"{name} — must be greater than zero")
            return v
        except ValueError:
            errors.append(f"{name} — please enter a valid number")
            return None

    bench_height      = parse(t_bench,  "Bench Height")
    hole_diameter     = parse(t_hole,   "Hole Diameter")
    rock_density      = parse(t_rock,   "Rock Density")
    explosive_density = parse(t_expden, "Explosive Density")
    area              = parse(t_area,   "Bench Area")
    unit_cost         = parse(t_cost,   "Unit Cost")

    if errors:
        items = "".join(
            f'<div class="err-item"><span class="err-bullet">▶</span> {e}</div>'
            for e in errors
        )
        st.markdown(f'<div style="padding:0 72px;"><div class="err-shell">{items}</div></div>',
                    unsafe_allow_html=True)
    else:
        res = run_design(bench_height, hole_diameter, rock_density,
                         explosive_density, unit_cost, area)
        st.session_state["res"] = res
        st.session_state["inp"] = dict(
            bench_height=bench_height, hole_diameter=hole_diameter,
            rock_density=rock_density, explosive_density=explosive_density,
            unit_cost=unit_cost, area=area
        )
        st.session_state["ts"] = datetime.now().strftime("%d %b %Y  —  %H:%M:%S")


# ── OUTPUTS ──────────────────────────────────────────────────

if "res" in st.session_state:
    res = st.session_state["res"]
    inp = st.session_state["inp"]
    ts  = st.session_state["ts"]

    st.markdown("""
    <div style="padding: 0 72px; margin-top: 40px;">
        <div class="sec-rule">
            <span class="sec-rule-icon">📊</span>
            <span class="sec-rule-txt">Results</span>
            <span class="sec-rule-line"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding: 0 72px;">
    <div class="results-shell">

        <div class="res-header">
            <span class="res-header-icon">🔩</span>
            <span class="res-header-txt">Computed output — drill &amp; blast parameters</span>
        </div>

        <div class="res-grid">
            <div class="res-block">
                <div class="res-block-label">burden distance</div>
                <div class="res-block-val">{res['burden']:.3f}</div>
                <div class="res-block-unit">metres</div>
            </div>
            <div class="res-block">
                <div class="res-block-label">hole spacing</div>
                <div class="res-block-val">{res['spacing']:.3f}</div>
                <div class="res-block-unit">metres</div>
            </div>
            <div class="res-block">
                <div class="res-block-label">drill holes</div>
                <div class="res-block-val">{res['holes']}</div>
                <div class="res-block-unit">count</div>
            </div>
            <div class="res-block">
                <div class="res-block-label">charge per hole</div>
                <div class="res-block-val">{res['charge']:.4f}</div>
                <div class="res-block-unit">tonnes</div>
            </div>
            <div class="res-block">
                <div class="res-block-label">total explosive</div>
                <div class="res-block-val">{res['total_exp']:.3f}</div>
                <div class="res-block-unit">tonnes</div>
            </div>
            <div class="res-block">
                <div class="res-block-label">rock volume</div>
                <div class="res-block-val">{res['rock_vol']:.0f}</div>
                <div class="res-block-unit">m³</div>
            </div>
            <div class="res-block accent" style="grid-column: span 3;">
                <div class="res-block-label">powder factor</div>
                <div class="res-block-val">{res['pf']:.4f}</div>
                <div class="res-block-unit">t / m³</div>
            </div>
        </div>

        <div class="cost-strip">
            <div>
                <div class="cost-lhs-label">Total Blasting Cost — Bench Estimate</div>
                <div class="cost-lhs-note">
                    {res['total_exp']:.3f} t &nbsp;×&nbsp; ${inp['unit_cost']:.2f} per tonne
                </div>
            </div>
            <div class="cost-figure">${res['cost']:,.2f}</div>
        </div>

        <div class="ts-line">Calculated: {ts}</div>

    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:64px;"></div>', unsafe_allow_html=True)
