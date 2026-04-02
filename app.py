import math
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Blast Design Tool", layout="wide")

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #04101C !important;
    color: #D6EEF8 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer { visibility: hidden; }

.top-banner {
    background: linear-gradient(90deg, #071A2B, #062A1A);
    border: 1px solid #0D3D5C;
    border-radius: 10px;
    padding: 24px 32px;
    margin-bottom: 28px;
    text-align: center;
}
.top-banner h1 {
    font-family: 'Share Tech Mono', monospace;
    font-size: 22px;
    color: #12A3D8;
    letter-spacing: 5px;
    margin: 0 0 6px 0;
}
.top-banner p {
    font-family: 'Exo 2', sans-serif;
    font-size: 12px;
    color: #4D7A99;
    letter-spacing: 2px;
    margin: 0;
}

.section-head {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #0FBF6A;
    text-transform: uppercase;
    border-left: 3px solid #0FBF6A;
    padding-left: 10px;
    margin: 24px 0 14px 0;
}

label, [data-testid="stNumberInput"] label p {
    font-family: 'Exo 2', sans-serif !important;
    font-size: 13px !important;
    color: #88BDD6 !important;
}

[data-testid="stNumberInput"] input {
    background-color: #040E19 !important;
    color: #12A3D8 !important;
    border: 1px solid #0D3D5C !important;
    border-radius: 5px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 14px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0A7FAD, #0C9A56) !important;
    color: #ffffff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 13px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 14px 40px !important;
    width: 100% !important;
    margin-top: 16px !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.output-panel {
    background: #071A2B;
    border: 1px solid #0D3D5C;
    border-radius: 10px;
    padding: 28px 32px;
    margin-top: 10px;
    height: 100%;
}
.output-panel-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #0FBF6A;
    text-transform: uppercase;
    border-bottom: 1px solid #0D3D5C;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
.r-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 10px 0;
    border-bottom: 1px solid #0A1E2E;
}
.r-row:last-child { border-bottom: none; }
.r-label {
    font-family: 'Exo 2', sans-serif;
    font-size: 14px;
    color: #88BDD6;
}
.r-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 17px;
    color: #D6EEF8;
}
.r-unit {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #4D7A99;
    margin-left: 5px;
}

.cost-banner {
    background: linear-gradient(120deg, #062A3D, #063320);
    border: 1px solid #0FBF6A;
    border-radius: 10px;
    padding: 28px 32px;
    margin-top: 20px;
    text-align: center;
}
.cost-label-txt {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #0FBF6A;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.cost-figure {
    font-family: 'Share Tech Mono', monospace;
    font-size: 46px;
    color: #0FBF6A;
    line-height: 1.1;
}
.cost-note {
    font-family: 'Exo 2', sans-serif;
    font-size: 13px;
    color: #4D7A99;
    margin-top: 8px;
}
.ts {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #4D7A99;
    text-align: right;
    margin-top: 16px;
    letter-spacing: 1px;
}
[data-testid="stDownloadButton"] button {
    background: #071A2B !important;
    color: #12A3D8 !important;
    border: 1px solid #12A3D8 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
    border-radius: 5px !important;
    width: 100% !important;
    margin-top: 16px !important;
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
    <h1>BLAST DESIGN & COST ESTIMATION</h1>
    <p>OPEN-PIT MINING  ·  DRILL & BLAST ENGINEERING TOOL</p>
</div>
""", unsafe_allow_html=True)


# ── INPUTS ────────────────────────────────────────────────────

st.markdown('<div class="section-head">Input Parameters</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    bench_height      = st.number_input("Bench Height (m)",         min_value=0.1,  value=10.0,   step=0.5,   format="%.1f")
    hole_diameter     = st.number_input("Hole Diameter (m)",        min_value=0.01, value=0.115,  step=0.005, format="%.4f")

with c2:
    rock_density      = st.number_input("Rock Density (t/m³)",      min_value=0.1,  value=2.7,    step=0.1,   format="%.2f")
    explosive_density = st.number_input("Explosive Density (t/m³)", min_value=0.1,  value=0.85,   step=0.05,  format="%.2f")

with c3:
    area              = st.number_input("Bench Area (m²)",          min_value=1.0,  value=5000.0, step=100.0, format="%.1f")
    unit_cost         = st.number_input("Explosive Unit Cost ($/t)", min_value=0.0,  value=450.0,  step=10.0,  format="%.2f")

run = st.button("RUN BLAST DESIGN")


# ── OUTPUTS ───────────────────────────────────────────────────

if run:
    try:
        res = run_design(bench_height, hole_diameter, rock_density,
                         explosive_density, unit_cost, area)
        inp = dict(bench_height=bench_height, hole_diameter=hole_diameter,
                   rock_density=rock_density, explosive_density=explosive_density,
                   unit_cost=unit_cost, area=area)
        st.session_state["res"] = res
        st.session_state["inp"] = inp
        st.session_state["ts"]  = datetime.now().strftime("%d %b %Y  %H:%M:%S")
    except Exception as e:
        st.error(f"Calculation error: {e}")

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
                <span class="r-value">{res['burden']:.3f} <span class="r-unit">m</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Spacing</span>
                <span class="r-value">{res['spacing']:.3f} <span class="r-unit">m</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Number of Drill Holes</span>
                <span class="r-value">{res['holes']} <span class="r-unit">holes</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Charge per Hole</span>
                <span class="r-value">{res['charge']:.4f} <span class="r-unit">t</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="output-panel">
            <div class="output-panel-title">Explosive & Rock Volume</div>
            <div class="r-row">
                <span class="r-label">Total Explosive Quantity</span>
                <span class="r-value">{res['total_exp']:.3f} <span class="r-unit">t</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Rock Volume</span>
                <span class="r-value">{res['rock_vol']:.2f} <span class="r-unit">m³</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Powder Factor</span>
                <span class="r-value">{res['pf']:.4f} <span class="r-unit">t/m³</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cost-banner">
        <div class="cost-label-txt">Total Blasting Cost — Bench Estimate</div>
        <div class="cost-figure">${res['cost']:,.2f}</div>
        <div class="cost-note">
            {res['total_exp']:.3f} t explosive &nbsp;&times;&nbsp; ${inp['unit_cost']:.2f} per tonne
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="ts">Calculated: {ts}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    report = make_report(inp, res)
    fname  = f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    st.download_button("SAVE REPORT (.txt)", data=report, file_name=fname, mime="text/plain")
