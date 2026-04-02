import math
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Blast Design Tool", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Mono:wght@300;400;500&family=Barlow+Condensed:wght@300;400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #030D17 !important;
    color: #D6EEF8 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer { visibility: hidden; }

/* ══════════════════════════════════════
   TOP BANNER
   Font: Orbitron — heavy geometric caps
   Used for: main title only
══════════════════════════════════════ */
.top-banner {
    background: linear-gradient(100deg, #061525 0%, #052215 100%);
    border: 1px solid #0C3550;
    border-top: 3px solid #12A3D8;
    border-radius: 0 0 12px 12px;
    padding: 30px 40px 24px;
    margin-bottom: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.top-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 28px,
        rgba(12,163,216,0.03) 28px,
        rgba(12,163,216,0.03) 29px
    );
    pointer-events: none;
}
.banner-title {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 28px;
    color: #12A3D8;
    letter-spacing: 6px;
    margin: 0 0 8px 0;
    text-transform: uppercase;
    text-shadow: 0 0 30px rgba(18,163,216,0.3);
}
.banner-sub {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 300;
    font-size: 13px;
    color: #3D6E8A;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin: 0;
}

/* ══════════════════════════════════════
   SECTION HEADINGS
   Font: Barlow Condensed — wide tracking
   Used for: "Input Parameters", "Results"
══════════════════════════════════════ */
.section-head {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 5px;
    color: #0FBF6A;
    text-transform: uppercase;
    border-left: 3px solid #0FBF6A;
    padding-left: 12px;
    margin: 28px 0 16px 0;
    line-height: 1;
}

/* ══════════════════════════════════════
   INPUT LABELS
   Font: Rajdhani — semi-condensed, clean
   Used for: field labels above inputs
══════════════════════════════════════ */
label p, .stTextInput label p {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 1.5px !important;
    color: #5A9EBF !important;
    text-transform: uppercase !important;
}

/* ══════════════════════════════════════
   INPUT FIELDS
   Font: IBM Plex Mono — precise numeric
   Used for: typed values in inputs
══════════════════════════════════════ */
[data-testid="stTextInput"] input {
    background-color: #040F1A !important;
    color: #7DD4F5 !important;
    border: 1px solid #0C3550 !important;
    border-bottom: 2px solid #0A6A99 !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 400 !important;
    font-size: 16px !important;
    padding: 10px 14px !important;
    letter-spacing: 1px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #12A3D8 !important;
    border-bottom-color: #0FBF6A !important;
    box-shadow: 0 3px 0 0 rgba(15,191,106,0.15) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #1D4A63 !important;
    font-size: 13px !important;
}

/* ══════════════════════════════════════
   RUN BUTTON
   Font: Orbitron — matches title weight
══════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #0A7FAD 0%, #0C9A56 100%) !important;
    color: #ffffff !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 5px !important;
    padding: 16px 40px !important;
    width: 100% !important;
    margin-top: 18px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.82 !important; }

/* ══════════════════════════════════════
   OUTPUT PANEL WRAPPER
══════════════════════════════════════ */
.output-panel {
    background: #061422;
    border: 1px solid #0C3550;
    border-radius: 10px;
    padding: 26px 30px;
    margin-top: 10px;
}

/* ══════════════════════════════════════
   OUTPUT PANEL TITLE
   Font: Barlow Condensed bold — matches section heads
   but smaller & different colour
══════════════════════════════════════ */
.output-panel-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 10px;
    letter-spacing: 4px;
    color: #12A3D8;
    text-transform: uppercase;
    border-bottom: 1px solid #0C2E45;
    padding-bottom: 10px;
    margin-bottom: 18px;
}

/* ══════════════════════════════════════
   RESULT ROWS
══════════════════════════════════════ */
.r-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 11px 0;
    border-bottom: 1px solid #081828;
}
.r-row:last-child { border-bottom: none; }

/* Label: Rajdhani regular — readable, not loud */
.r-label {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 500;
    font-size: 15px;
    color: #6BAAC8;
    letter-spacing: 0.5px;
}

/* Value: IBM Plex Mono medium — precise number display */
.r-value {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 500;
    font-size: 19px;
    color: #E2F4FF;
    letter-spacing: 1px;
}

/* Unit: IBM Plex Mono light — clearly secondary */
.r-unit {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 300;
    font-size: 11px;
    color: #2D6680;
    margin-left: 5px;
    letter-spacing: 0.5px;
}

/* ══════════════════════════════════════
   COST BANNER
══════════════════════════════════════ */
.cost-banner {
    background: linear-gradient(115deg, #051E2E 0%, #042415 100%);
    border: 1px solid #0FBF6A;
    border-left: 5px solid #0FBF6A;
    border-radius: 10px;
    padding: 30px 36px;
    margin-top: 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}

/* Cost label: Barlow Condensed wide */
.cost-label-txt {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 600;
    font-size: 12px;
    letter-spacing: 4px;
    color: #0FBF6A;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* Cost note: Rajdhani light */
.cost-note {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 400;
    font-size: 14px;
    color: #2D6645;
    letter-spacing: 0.5px;
}

/* Cost figure: Orbitron — the hero number */
.cost-figure {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 52px;
    color: #0FBF6A;
    line-height: 1;
    text-shadow: 0 0 40px rgba(15,191,106,0.25);
    letter-spacing: 2px;
}

/* ══════════════════════════════════════
   ERROR BOX
   Font: IBM Plex Mono — monospace warning
══════════════════════════════════════ */
.err-box {
    background: #140808;
    border: 1px solid #6B1515;
    border-left: 4px solid #E05555;
    border-radius: 5px;
    padding: 14px 18px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 400;
    font-size: 12px;
    color: #E05555;
    margin-top: 14px;
    letter-spacing: 0.5px;
    line-height: 1.9;
}

/* ══════════════════════════════════════
   TIMESTAMP
   Font: IBM Plex Mono light — tiny & subtle
══════════════════════════════════════ */
.ts {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 300;
    font-size: 10px;
    color: #1E4D63;
    text-align: right;
    margin-top: 18px;
    letter-spacing: 2px;
    text-transform: uppercase;
}
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


# ── TITLE ────────────────────────────────────────────────────

st.markdown("""
<div class="top-banner">
    <div class="banner-title">Blast Design &amp; Cost Estimation</div>
    <div class="banner-sub">Open-Pit Mining &nbsp;·&nbsp; Drill &amp; Blast Engineering Tool</div>
</div>
""", unsafe_allow_html=True)


# ── INPUTS ───────────────────────────────────────────────────

st.markdown('<div class="section-head">Input Parameters</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    t_bench  = st.text_input("Bench Height (m)",          value="10.0",  placeholder="e.g. 10.0")
    t_hole   = st.text_input("Hole Diameter (m)",         value="0.115", placeholder="e.g. 0.115")

with c2:
    t_rock   = st.text_input("Rock Density (t/m³)",       value="2.7",   placeholder="e.g. 2.7")
    t_expden = st.text_input("Explosive Density (t/m³)",  value="0.85",  placeholder="e.g. 0.85")

with c3:
    t_area   = st.text_input("Bench Area (m²)",           value="5000",  placeholder="e.g. 5000")
    t_cost   = st.text_input("Explosive Unit Cost ($/t)",  value="450",   placeholder="e.g. 450")

run = st.button("Run Blast Design")


# ── RUN ──────────────────────────────────────────────────────

if run:
    errors = []

    def parse(val, name):
        try:
            v = float(val)
            if v <= 0:
                errors.append(f"{name} must be greater than 0")
            return v
        except ValueError:
            errors.append(f"{name} — enter a valid number")
            return None

    bench_height      = parse(t_bench,  "Bench Height")
    hole_diameter     = parse(t_hole,   "Hole Diameter")
    rock_density      = parse(t_rock,   "Rock Density")
    explosive_density = parse(t_expden, "Explosive Density")
    area              = parse(t_area,   "Bench Area")
    unit_cost         = parse(t_cost,   "Explosive Unit Cost")

    if errors:
        err_html = "".join(f"<div>&#x25B6; {e}</div>" for e in errors)
        st.markdown(f'<div class="err-box">{err_html}</div>', unsafe_allow_html=True)
    else:
        res = run_design(bench_height, hole_diameter, rock_density,
                         explosive_density, unit_cost, area)
        inp = dict(bench_height=bench_height, hole_diameter=hole_diameter,
                   rock_density=rock_density, explosive_density=explosive_density,
                   unit_cost=unit_cost, area=area)
        st.session_state["res"] = res
        st.session_state["inp"] = inp
        st.session_state["ts"]  = datetime.now().strftime("%d %b %Y  —  %H:%M:%S")


# ── OUTPUTS ──────────────────────────────────────────────────

if "res" in st.session_state:
    res = st.session_state["res"]
    inp = st.session_state["inp"]
    ts  = st.session_state["ts"]

    st.markdown('<div class="section-head">Results</div>', unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(f"""
        <div class="output-panel">
            <div class="output-panel-title">Drill Design</div>
            <div class="r-row">
                <span class="r-label">Burden</span>
                <span class="r-value">{res['burden']:.3f}<span class="r-unit">m</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Spacing</span>
                <span class="r-value">{res['spacing']:.3f}<span class="r-unit">m</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Number of Drill Holes</span>
                <span class="r-value">{res['holes']}<span class="r-unit">holes</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Charge per Hole</span>
                <span class="r-value">{res['charge']:.4f}<span class="r-unit">t</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="output-panel">
            <div class="output-panel-title">Explosive &amp; Rock Volume</div>
            <div class="r-row">
                <span class="r-label">Total Explosive Quantity</span>
                <span class="r-value">{res['total_exp']:.3f}<span class="r-unit">t</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Rock Volume</span>
                <span class="r-value">{res['rock_vol']:.2f}<span class="r-unit">m³</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Powder Factor</span>
                <span class="r-value">{res['pf']:.4f}<span class="r-unit">t/m³</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cost-banner">
        <div>
            <div class="cost-label-txt">Total Blasting Cost — Bench Estimate</div>
            <div class="cost-note">{res['total_exp']:.3f} t explosive &nbsp;&times;&nbsp; ${inp['unit_cost']:.2f} per tonne</div>
        </div>
        <div class="cost-figure">${res['cost']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="ts">Calculated: {ts}</div>', unsafe_allow_html=True)
