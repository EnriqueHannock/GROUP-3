import math
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Blast Design Tool", layout="wide")

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

/* Input labels */
label p, .stTextInput label p {
    font-family: 'Exo 2', sans-serif !important;
    font-size: 13px !important;
    color: #88BDD6 !important;
}

/* Text input fields - clean, no spinners */
[data-testid="stTextInput"] input {
    background-color: #040E19 !important;
    color: #12A3D8 !important;
    border: 1px solid #0D3D5C !important;
    border-radius: 5px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #12A3D8 !important;
    box-shadow: 0 0 0 2px rgba(18,163,216,0.12) !important;
}

/* Run button */
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

/* Output panels */
.output-panel {
    background: #071A2B;
    border: 1px solid #0D3D5C;
    border-radius: 10px;
    padding: 28px 32px;
    margin-top: 10px;
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

/* Cost banner */
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

/* Error box */
.err-box {
    background: #1A0A0A;
    border: 1px solid #8B1A1A;
    border-radius: 6px;
    padding: 12px 18px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    color: #E05555;
    margin-top: 12px;
}

.ts {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #4D7A99;
    text-align: right;
    margin-top: 16px;
    letter-spacing: 1px;
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


# ── INPUTS  (st.text_input — no +/- spinners) ─────────────────

st.markdown('<div class="section-head">Input Parameters</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    t_bench  = st.text_input("Bench Height (m)",         value="10.0",  placeholder="e.g. 10.0")
    t_hole   = st.text_input("Hole Diameter (m)",        value="0.115", placeholder="e.g. 0.115")

with c2:
    t_rock   = st.text_input("Rock Density (t/m³)",      value="2.7",   placeholder="e.g. 2.7")
    t_expden = st.text_input("Explosive Density (t/m³)", value="0.85",  placeholder="e.g. 0.85")

with c3:
    t_area   = st.text_input("Bench Area (m²)",          value="5000",  placeholder="e.g. 5000")
    t_cost   = st.text_input("Explosive Unit Cost ($/t)", value="450",   placeholder="e.g. 450")

run = st.button("RUN BLAST DESIGN")


# ── RUN ───────────────────────────────────────────────────────

if run:
    errors = []

    def parse(val, name):
        try:
            v = float(val)
            if v <= 0:
                errors.append(f"{name} must be greater than 0.")
            return v
        except ValueError:
            errors.append(f"{name} — invalid number entered.")
            return None

    bench_height      = parse(t_bench,  "Bench Height")
    hole_diameter     = parse(t_hole,   "Hole Diameter")
    rock_density      = parse(t_rock,   "Rock Density")
    explosive_density = parse(t_expden, "Explosive Density")
    area              = parse(t_area,   "Bench Area")
    unit_cost         = parse(t_cost,   "Explosive Unit Cost")

    if errors:
        err_html = "".join(f"<div>&#x26A0; {e}</div>" for e in errors)
        st.markdown(f'<div class="err-box">{err_html}</div>', unsafe_allow_html=True)
    else:
        res = run_design(bench_height, hole_diameter, rock_density,
                         explosive_density, unit_cost, area)
        inp = dict(bench_height=bench_height, hole_diameter=hole_diameter,
                   rock_density=rock_density, explosive_density=explosive_density,
                   unit_cost=unit_cost, area=area)
        st.session_state["res"] = res
        st.session_state["inp"] = inp
        st.session_state["ts"]  = datetime.now().strftime("%d %b %Y  %H:%M:%S")


# ── OUTPUTS ───────────────────────────────────────────────────

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
                <span class="r-value">{res['burden']:.3f}<span class="r-unit"> m</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Spacing</span>
                <span class="r-value">{res['spacing']:.3f}<span class="r-unit"> m</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Number of Drill Holes</span>
                <span class="r-value">{res['holes']}<span class="r-unit"> holes</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Charge per Hole</span>
                <span class="r-value">{res['charge']:.4f}<span class="r-unit"> t</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="output-panel">
            <div class="output-panel-title">Explosive & Rock Volume</div>
            <div class="r-row">
                <span class="r-label">Total Explosive Quantity</span>
                <span class="r-value">{res['total_exp']:.3f}<span class="r-unit"> t</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Rock Volume</span>
                <span class="r-value">{res['rock_vol']:.2f}<span class="r-unit"> m³</span></span>
            </div>
            <div class="r-row">
                <span class="r-label">Powder Factor</span>
                <span class="r-value">{res['pf']:.4f}<span class="r-unit"> t/m³</span></span>
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
