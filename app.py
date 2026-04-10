"""
X-BIM: Extraterrestrial Building Information Modeling
======================================================
Author  : Systems Architect / Full-Stack Developer
Model   : Google Gemini 2.5 Flash (gemini-2.5-flash-preview-04-17)
Outputs : MBSE CSV (Cameo) + UE5 Python procedural habitat script
"""

import os
import io
import csv
import json
import base64
import textwrap
import requests
import streamlit as st
from pathlib import Path

# ── Load hero background image as base64 ──
_here = Path(__file__).parent
_hero_img_path = _here / "hero_bg.png"
if _hero_img_path.exists():
    _hero_b64 = base64.b64encode(_hero_img_path.read_bytes()).decode()
    _hero_css_bg = f"url('data:image/png;base64,{_hero_b64}')"
else:
    _hero_css_bg = "none"

# ──────────────────────────────────────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="X-BIM · Extraterrestrial BIM",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS — monochrome: white bg, near-black text, no colored boxes
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600&family=DM+Mono:wght@400;500&display=swap');

    /* ─── BASE ─── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.01em;
    }
    .stApp { background-color: #F5F2ED !important; color: #1C1C1C !important; }

    /* ─── GLOBAL TEXT ─── */
    p, div, li, td, th, a, small, strong, em,
    .stMarkdown, .stMarkdown p, .stMarkdown span { color: #1C1C1C !important; }

    /* ─── HERO: force ALL children white ─── */
    .xbim-hero, .xbim-hero *,
    .xbim-hero h1, .xbim-hero p, .xbim-hero span, .xbim-hero div { color: #FFFFFF !important; }

    h2, h3, h4 { color: #1C1C1C !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; }
    h3 { font-size: 0.80rem !important; text-transform: uppercase !important; letter-spacing: 0.12em !important;
         border-bottom: 1px solid #D8D3CC; padding-bottom: 10px; margin-bottom: 16px; }

    /* ─── SIDEBAR ─── */
    section[data-testid="stSidebar"] {
        background-color: #F5F2ED !important;
        border-right: 1px solid #D8D3CC !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1C1C1C !important;
        background-color: transparent !important;
    }
    section[data-testid="stSidebar"] h2 {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1.0rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: #2A2A2A !important;
        padding-bottom: 10px !important;
        border-bottom: 1px solid #D8D3CC !important;
        margin-bottom: 4px !important;
    }
    section[data-testid="stSidebar"] label {
        font-size: 0.68rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: #888880 !important;
    }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        background-color: #F5F2ED !important;
        color: #1C1C1C !important;
        border: 1px solid #CCCAC5 !important;
        border-radius: 0 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ─── DROPDOWNS (portal-rendered) ─── */
    [data-baseweb="select"] > div {
        background-color: #F5F2ED !important;
        color: #1C1C1C !important;
        border-color: #CCCAC5 !important;
        border-radius: 0 !important;
    }
    [data-baseweb="select"] * { color: #1C1C1C !important; }
    [data-baseweb="popover"] { background-color: #F5F2ED !important; }
    [data-baseweb="popover"] > div, [data-baseweb="popover"] ul, [data-baseweb="menu"] {
        background-color: #F5F2ED !important; color: #1C1C1C !important;
        border: 1px solid #D8D3CC !important; border-radius: 0 !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.07) !important;
    }
    [data-baseweb="menu"] li, [data-baseweb="option"], li[role="option"],
    [data-baseweb="menu"] [role="option"] {
        background-color: #F5F2ED !important; color: #1C1C1C !important;
        font-size: 0.86rem !important; letter-spacing: 0.02em !important;
    }
    [data-baseweb="menu"] li:hover, [data-baseweb="option"]:hover,
    li[role="option"]:hover, [data-baseweb="menu"] [aria-selected="true"],
    [data-baseweb="option"][aria-selected="true"] {
        background-color: #EAE6DF !important; color: #1C1C1C !important;
    }

    /* ─── SLIDER ─── */
    [data-testid="stSlider"] [role="slider"] {
        background-color: #C9933A !important;
        border-color: #C9933A !important;
    }
    [data-testid="stTickBarMin"], [data-testid="stTickBarMax"] {
        background: transparent !important; color: #888880 !important;
        font-size: 0.70rem !important; letter-spacing: 0.06em !important;
    }

    /* ─── METRICS ROW ─── */
    [data-testid="metric-container"] {
        background: transparent !important; border: none !important;
        border-bottom: 1px solid #D8D3CC !important;
        border-radius: 0 !important; padding: 16px 4px 12px !important;
        box-shadow: none !important;
    }
    [data-testid="metric-container"] * { color: #1C1C1C !important; }
    [data-testid="stMetricValue"] {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 300 !important; font-size: 1.8rem !important;
        letter-spacing: -0.01em !important;
        font-variant-numeric: tabular-nums !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.62rem !important; letter-spacing: 0.14em !important;
        text-transform: uppercase !important; color: #888880 !important;
    }

    /* ─── EXPANDERS ─── */
    .stExpander {
        background: transparent !important;
        border: none !important;
        border-bottom: 1px solid #D8D3CC !important;
        border-radius: 0 !important; box-shadow: none !important;
    }
    .stExpander *, .stExpander summary { color: #1C1C1C !important; background: transparent !important; }
    .stExpander summary {
        font-size: 0.82rem !important; font-weight: 500 !important;
        letter-spacing: 0.04em !important;
    }

    /* ─── BUTTONS ─── */
    .stDownloadButton > button, .stButton > button {
        background: transparent !important;
        color: #1C1C1C !important;
        border: 1px solid #1C1C1C !important;
        border-radius: 0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        padding: 11px 28px !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button *, .stButton > button *,
    .stDownloadButton > button p, .stDownloadButton > button span,
    .stButton > button p, .stButton > button span {
        color: #1C1C1C !important; background: transparent !important;
    }
    .stDownloadButton > button:hover, .stButton > button:hover {
        background: #1C1C1C !important; color: #F5F2ED !important;
    }
    .stDownloadButton > button:hover *, .stButton > button:hover * {
        color: #F5F2ED !important;
    }

    /* ─── HEADER TOOLBAR ─── */
    header[data-testid="stHeader"] {
        background-color: #F5F2ED !important;
        border-bottom: 1px solid #D8D3CC !important;
    }
    header[data-testid="stHeader"] svg { fill: #1C1C1C !important; color: #1C1C1C !important; }
    [data-testid="stMainMenuButton"] {
        background: transparent !important; border: none !important; box-shadow: none !important;
    }
    [data-testid="stMainMenuButton"] svg, [data-testid="stMainMenuButton"] * {
        fill: #1C1C1C !important; color: #1C1C1C !important; background: transparent !important;
    }
    [data-testid="stMainMenuButton"]:hover { background: #EAE6DF !important; }
    [data-testid="stAppDeployButton"] button, header[data-testid="stHeader"] button {
        background: transparent !important; color: #1C1C1C !important;
        border: 1px solid #CCCAC5 !important; border-radius: 0 !important;
        font-size: 0.72rem !important; letter-spacing: 0.1em !important;
    }
    header[data-testid="stHeader"] button:hover { background: #EAE6DF !important; }

    /* ─── NUMBER INPUT STEPPERS ─── */
    button[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"] {
        background: #F5F2ED !important; color: #1C1C1C !important;
        border: 1px solid #CCCAC5 !important; border-radius: 0 !important;
    }
    button[data-testid="stNumberInputStepUp"] *,
    button[data-testid="stNumberInputStepDown"] * {
        color: #1C1C1C !important; fill: #1C1C1C !important;
    }

    /* ─── CODE BLOCKS ─── */
    code, pre {
        font-family: 'DM Mono', monospace !important;
        background: #EAE6DF !important; color: #1C1C1C !important;
        border: 1px solid #D8D3CC !important; border-radius: 0 !important;
    }

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #D8D3CC !important; padding: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important; color: #999993 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 400 !important; font-size: 0.70rem !important;
        text-transform: uppercase !important; letter-spacing: 0.14em !important;
        border-radius: 0 !important; padding: 12px 20px !important;
        transition: color 0.15s !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1C1C1C !important;
        border-bottom: 1.5px solid #C9933A !important;  /* amber accent underline */
        font-weight: 600 !important; background: transparent !important;
    }

    /* ─── HERO BANNER ─── */
    .xbim-hero {
        background-image: var(--hero-bg);
        background-size: cover;
        background-position: center 40%;
        border: none;
        border-top: 1px solid #1C1C1C;
        border-bottom: 1px solid #D8D3CC;
        padding: 0;
        margin-bottom: 0;
        position: relative;
        overflow: hidden;
    }
    /* dark semi-transparent overlay — keeps text sharp */
    .xbim-hero-overlay {
        background: rgba(28, 28, 28, 0.62);
        padding: 44px 52px 40px;
        position: relative;
        z-index: 1;
    }
    .xbim-hero::after {
        content: 'XBIM — 2026';
        position: absolute; bottom: 14px; right: 24px;
        font-family: 'DM Mono', monospace;
        font-size: 0.58rem; color: rgba(255,255,255,0.45); letter-spacing: 0.18em;
        text-transform: uppercase; z-index: 2;
    }
    /* Outfit 800 for the X-BIM title — clean geometric, Google-product aesthetic */
    .xbim-hero h1,
    .xbim-hero .xbim-hero-overlay h1 {
        margin: 0 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 3.0rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.10em !important;
        line-height: 1.0 !important;
        color: #FFFFFF !important;
        text-transform: uppercase !important;
        -webkit-font-smoothing: antialiased !important;
    }
    .xbim-hero p,
    .xbim-hero .xbim-hero-overlay p {
        margin: 12px 0 0 !important;
        font-size: 0.66rem !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
        color: rgba(255,255,255,0.65) !important;
    }

    /* ─── TAG CHIPS ─── */
    .tag {
        display: inline-block;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.55);
        border-radius: 0;
        padding: 4px 11px;
        font-size: 0.60rem;
        color: rgba(255,255,255,0.92) !important;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin: 3px 2px;
        font-family: 'DM Sans', sans-serif;
    }
    /* all tags identical — no amber accent */
    .tag-accent {
        border-color: rgba(255,255,255,0.55) !important;
        color: rgba(255,255,255,0.92) !important;
    }

    /* ─── DIVIDERS ─── */
    hr { border-color: #D8D3CC !important; margin: 24px 0 !important; }

    /* ─── INPUTS ─── */
    input, textarea {
        background-color: #F5F2ED !important; color: #1C1C1C !important;
        border-radius: 0 !important;
    }
    .stSelectbox *, .stTextInput *, .stTextArea *,
    .stNumberInput *, .stSlider *, .stAlert * { color: #1C1C1C !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inject hero background as a CSS variable (data-URI avoids any static-file serving issues)
st.markdown(
    f"<style>:root {{ --hero-bg: {_hero_css_bg}; }}</style>",
    unsafe_allow_html=True,
)




# ──────────────────────────────────────────────────────────────────────────────
# Hero Banner
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="xbim-hero">
      <div class="xbim-hero-overlay">
        <div style="display:flex; align-items:center; gap:28px;">
          <!-- BIM logo box: 2px white border, white mono text -->
          <div style="width:72px;height:72px;border:2px solid #FFFFFF;display:flex;
                      align-items:center;justify-content:center;font-family:'DM Mono',monospace;
                      font-size:0.66rem;font-weight:600;letter-spacing:0.22em;
                      color:#FFFFFF !important;flex-shrink:0;text-transform:uppercase;
                      -webkit-font-smoothing:antialiased;">BIM</div>
          <div>
            <!-- X-BIM: inline white forces override of any global rule -->
            <h1 style="margin:0 !important; color:#FFFFFF !important;
                        font-family:'Outfit',sans-serif !important; font-weight:800 !important;
                        font-size:3.0rem !important; letter-spacing:0.10em !important;
                        text-transform:uppercase !important; line-height:1.0 !important;
                        -webkit-font-smoothing:antialiased;">X&#8209;BIM</h1>
            <!-- subtitle: larger, white -->
            <p style="margin:16px 0 0 !important; color:#FFFFFF !important;
                      font-size:1.05rem !important; letter-spacing:0.10em !important;
                      text-transform:uppercase !important; font-family:'DM Sans',sans-serif !important;
                      font-weight:400 !important; opacity:0.88;">
              Extraterrestrial Building Information Modeling &nbsp;&middot;&nbsp;
              AI-Powered Habitat Design for Deep Space
            </p>
          </div>
        </div>
        <!-- Tags: all white, border white, explicit inline color -->
        <div style="margin-top:26px; padding-top:18px; border-top:1px solid rgba(255,255,255,0.22);">
          <span style="display:inline-block;border:1px solid rgba(255,255,255,0.6);padding:4px 12px;
                       font-size:0.62rem;color:#FFFFFF;letter-spacing:0.14em;text-transform:uppercase;
                       font-family:'DM Sans',sans-serif;font-weight:500;margin:3px 2px;">LUNAR</span>
          <span style="display:inline-block;border:1px solid rgba(255,255,255,0.6);padding:4px 12px;
                       font-size:0.62rem;color:#FFFFFF;letter-spacing:0.14em;text-transform:uppercase;
                       font-family:'DM Sans',sans-serif;font-weight:500;margin:3px 2px;">MARTIAN</span>
          <span style="display:inline-block;border:1px solid rgba(255,255,255,0.6);padding:4px 12px;
                       font-size:0.62rem;color:#FFFFFF;letter-spacing:0.14em;text-transform:uppercase;
                       font-family:'DM Sans',sans-serif;font-weight:500;margin:3px 2px;">RADIATION SHIELDING</span>
          <span style="display:inline-block;border:1px solid rgba(255,255,255,0.6);padding:4px 12px;
                       font-size:0.62rem;color:#FFFFFF;letter-spacing:0.14em;text-transform:uppercase;
                       font-family:'DM Sans',sans-serif;font-weight:500;margin:3px 2px;">ISRU</span>
          <span style="display:inline-block;border:1px solid rgba(255,255,255,0.6);padding:4px 12px;
                       font-size:0.62rem;color:#FFFFFF;letter-spacing:0.14em;text-transform:uppercase;
                       font-family:'DM Sans',sans-serif;font-weight:500;margin:3px 2px;">MBSE / CAMEO</span>
          <span style="display:inline-block;border:1px solid rgba(255,255,255,0.6);padding:4px 12px;
                       font-size:0.62rem;color:#FFFFFF;letter-spacing:0.14em;text-transform:uppercase;
                       font-family:'DM Sans',sans-serif;font-weight:500;margin:3px 2px;">UNREAL ENGINE 5</span>
          <span style="display:inline-block;border:1px solid rgba(255,255,255,0.6);padding:4px 12px;
                       font-size:0.62rem;color:#FFFFFF;letter-spacing:0.14em;text-transform:uppercase;
                       font-family:'DM Sans',sans-serif;font-weight:500;margin:3px 2px;">NASA HABITABILITY</span>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────────────────────
# Sidebar — Inputs
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding-bottom:10px;
                    border-bottom:1px solid #D8D3CC;margin-bottom:4px;">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="#2A2A2A">
            <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58
              c0.18-0.14,0.23-0.41,0.12-0.61l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94
              L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29
              L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12
              s0.02,0.64,0.07,0.94l-2.03,1.58c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96
              c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54
              c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61
              L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
          </svg>
          <span style="font-family:'DM Sans',sans-serif;font-size:1.0rem;font-weight:600;
                       letter-spacing:0.12em;text-transform:uppercase;color:#2A2A2A;">Mission Parameters</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")

    planet = st.selectbox(
        "Planetary Destination",
        ["Moon", "Mars"],
        help="Select the target celestial body for habitat deployment.",
    )

    radiation_cm = st.slider(
        "Radiation Shielding Thickness (cm)",
        min_value=5,
        max_value=200,
        value=50,
        step=5,
        help="Regolith / polyethylene equivalent shielding depth.",
    )

    isru_raw = st.text_area(
        "ISRU Materials",
        value="Lunar regolith, basalt fibre, water ice, aluminium oxide",
        height=120,
        help="Comma-separated list of In-Situ Resource Utilisation materials available on-site.",
    )
    isru_materials = [m.strip() for m in isru_raw.split(",") if m.strip()]

    st.markdown("---")
    st.markdown("### Gemini API Key")

    # Priority: secrets.toml → env var → empty (user types it in)
    _secret_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
    _env_key    = os.environ.get("GEMINI_API_KEY", "")
    _default_key = _secret_key or _env_key

    api_key = st.text_input(
        "API Key",
        type="password",
        value=_default_key,
        help="Key is auto-loaded from .streamlit/secrets.toml or GEMINI_API_KEY env var.",
    )
    if _default_key:
        st.success("API key loaded from secrets / env var.")

    st.markdown("---")
    st.markdown("### Habitat Geometry")
    hab_length = st.number_input("Length (m)", min_value=2.0, max_value=200.0, value=20.0, step=1.0)
    hab_width  = st.number_input("Width  (m)", min_value=2.0, max_value=200.0, value=10.0, step=1.0)
    hab_height = st.number_input("Height (m)", min_value=2.0, max_value=50.0,  value=5.0,  step=0.5)

    generate_btn = st.button("Generate X-BIM Analysis", use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Summary metrics row
# ──────────────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Destination",     planet)
col2.metric("Shielding",      f"{radiation_cm} cm")
col3.metric("ISRU Materials", len(isru_materials))
col4.metric("Habitat Volume",  f"{hab_length * hab_width * hab_height:.0f} m³")

st.markdown("---")

# ──────────────────────────────────────────────────────────────────────────────
# Helper: build Gemini prompt
# ──────────────────────────────────────────────────────────────────────────────
def build_prompt(planet: str, radiation_cm: int, isru_materials: list[str]) -> str:
    isru_str = ", ".join(isru_materials)
    return f"""
You are an expert aerospace structural engineer and systems architect specialising in
extraterrestrial habitat design. Generate a thorough engineering analysis for the
following mission parameters:

MISSION PARAMETERS
==================
- Planetary Destination : {planet}
- Radiation Shielding   : {radiation_cm} cm (regolith equivalent)
- ISRU Materials        : {isru_str}

OUTPUT FORMAT — You MUST return ONLY a single valid JSON object with these keys:
{{
  "structural_spec": {{
    "primary_structure"   : "<material / construction method>",
    "foundation_type"     : "<foundation approach>",
    "pressure_vessel"     : "<pressure vessel design>",
    "key_loads"           : ["<load 1>", "<load 2>", "..."],
    "safety_factor"       : <number>,
    "summary"             : "<2-3 sentence narrative>"
  }},
  "thermal_requirements": {{
    "surface_temp_range_C": "<min to max °C>",
    "internal_setpoint_C" : <number>,
    "insulation_strategy" : "<approach>",
    "active_thermal_ctrl" : "<HVAC / heat-pipe approach>",
    "heat_rejection"      : "<radiator / passive approach>",
    "summary"             : "<2-3 sentence narrative>"
  }},
  "requirements_table": [
    {{
      "req_id"     : "REQ-001",
      "category"   : "<Structure|Thermal|Radiation|ISRU|Life Support|Power>",
      "requirement": "<shall statement>",
      "rationale"  : "<why this is needed>",
      "verification": "<Test|Analysis|Inspection|Demonstration>",
      "priority"   : "<High|Medium|Low>"
    }}
  ]
}}

Generate at least 12 requirements covering: structure, thermal, radiation, ISRU
utilisation, life support interfaces, and power. Be specific with numbers and cite
{planet}-specific environmental conditions. Return ONLY the JSON — no markdown fences,
no preamble, no trailing text.
""".strip()


# ──────────────────────────────────────────────────────────────────────────────
# Helper: call Gemini
# ──────────────────────────────────────────────────────────────────────────────
def call_gemini(api_key: str, prompt: str) -> dict:
    """
    Calls the Gemini REST API directly via requests — no SDK, no routing surprises.
    Uses the v1beta endpoint which is what Google AI Studio keys are issued for.
    Model: gemini-1.5-flash  (free tier: 1,500 req/day, 15 RPM)
    """
    url = (
        "https://generativelanguage.googleapis.com"
        "/v1beta/models/gemini-3.1-flash-lite-preview:generateContent"
        f"?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "topP": 0.95,
        },
    }
    resp = requests.post(url, json=payload, timeout=90)

    if not resp.ok:
        raise RuntimeError(
            f"{resp.status_code} {resp.reason}: {resp.text[:400]}"
        )

    raw = (
        resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        .strip()
    )

    # Strip markdown code fences
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:])
    if raw.endswith("```"):
        raw = "\n".join(raw.split("\n")[:-1])
    raw = raw.strip()

    # Isolate the outermost JSON object
    start = raw.find("{")
    end   = raw.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("Gemini response contained no JSON object.")
    return json.loads(raw[start:end])


# ──────────────────────────────────────────────────────────────────────────────
# Helper: build MBSE CSV (Cameo Systems Modeler compatible)
# ──────────────────────────────────────────────────────────────────────────────
def build_mbse_csv(data: dict, planet: str, radiation_cm: int, isru_materials: list) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    # ── header block ──
    writer.writerow(["# X-BIM MBSE Requirements Export"])
    writer.writerow(["# Compatible with: Cameo Systems Modeler / SysML Requirements Table"])
    writer.writerow(["# Planet", planet])
    writer.writerow(["# Radiation Shielding (cm)", radiation_cm])
    writer.writerow(["# ISRU Materials", "; ".join(isru_materials)])
    writer.writerow([])

    # ── column headers (Cameo SysML format) ──
    writer.writerow([
        "Req ID", "Name", "Category", "Requirement Text",
        "Rationale", "Verification Method", "Priority",
        "Status", "Owner", "Source",
    ])

    for req in data.get("requirements_table", []):
        writer.writerow([
            req.get("req_id", ""),
            f"XBIM-{planet.upper()}-{req.get('req_id', '')}",
            req.get("category", ""),
            req.get("requirement", ""),
            req.get("rationale", ""),
            req.get("verification", ""),
            req.get("priority", ""),
            "Draft",
            "X-BIM AI",
            f"Gemini Analysis — {planet} Habitat",
        ])

    return output.getvalue()


# ──────────────────────────────────────────────────────────────────────────────
# Helper: build UE5 Python script
# ──────────────────────────────────────────────────────────────────────────────
def build_ue5_script(
    planet: str,
    radiation_cm: int,
    isru_materials: list,
    length: float,
    width: float,
    height: float,
    data: dict,
) -> str:
    isru_str  = ", ".join(isru_materials)
    struct    = data.get("structural_spec", {})
    thermal   = data.get("thermal_requirements", {})
    reqs      = data.get("requirements_table", [])
    req_lines = "\n".join(
        f'    # {r["req_id"]}: {r["requirement"][:80]}' for r in reqs[:8]
    )

    return textwrap.dedent(f"""
    \"\"\"
    X-BIM Unreal Engine 5 — Procedural Habitat Generator
    ======================================================
    Planet            : {planet}
    Shielding         : {radiation_cm} cm
    ISRU Materials    : {isru_str}
    Structural system : {struct.get('primary_structure', 'N/A')}
    Foundation        : {struct.get('foundation_type', 'N/A')}
    Pressure vessel   : {struct.get('pressure_vessel', 'N/A')}
    Internal temp     : {thermal.get('internal_setpoint_C', 22)} °C
    Insulation        : {thermal.get('insulation_strategy', 'N/A')}

    Top Requirements (excerpt):
{req_lines}

    Usage
    -----
    1. Open Unreal Engine 5 (5.3+).
    2. In the menu bar: Tools → Execute Python Script → select this file.
    3. The habitat bounding boxes will be spawned at world origin.
    \"\"\"

    import unreal

    # ── Configuration ─────────────────────────────────────────────────────────
    HABITAT_CONFIG = {{
        "planet"         : "{planet}",
        "shielding_cm"   : {radiation_cm},
        "isru_materials" : {isru_materials!r},
        "length_m"       : {length},
        "width_m"        : {width},
        "height_m"       : {height},
        "scale_factor"   : 100.0,          # 1 m  →  100 UE units
        "struct_system"  : "{struct.get('primary_structure', 'Regolith shell')}",
        "foundation"     : "{struct.get('foundation_type', 'Spread footing')}",
        "setpoint_c"     : {thermal.get('internal_setpoint_C', 22)},
    }}

    MODULES = [
        {{"name": "Habitat Core",        "offset_x": 0.0,   "offset_y": 0.0,   "scale_x": 1.0,  "scale_y": 1.0,  "scale_z": 1.0,  "color": (0.2, 0.6, 1.0)}},
        {{"name": "Airlock",             "offset_x": 1.2,   "offset_y": 0.0,   "scale_x": 0.2,  "scale_y": 0.3,  "scale_z": 0.6,  "color": (1.0, 0.5, 0.1)}},
        {{"name": "Radiation Shield",    "offset_x": 0.0,   "offset_y": 0.0,   "scale_x": 1.1,  "scale_y": 1.1,  "scale_z": 1.05, "color": (0.3, 0.8, 0.3)}},
        {{"name": "Solar / Power Bay",   "offset_x": -1.3,  "offset_y": 0.0,   "scale_x": 0.25, "scale_y": 0.8,  "scale_z": 0.05, "color": (1.0, 0.9, 0.0)}},
        {{"name": "Thermal Radiator",    "offset_x": 0.0,   "offset_y": 1.2,   "scale_x": 0.8,  "scale_y": 0.05, "scale_z": 0.4,  "color": (0.8, 0.2, 0.2)}},
        {{"name": "ISRU Processing Bay", "offset_x": 0.0,   "offset_y": -1.2,  "scale_x": 0.4,  "scale_y": 0.2,  "scale_z": 0.5,  "color": (0.7, 0.4, 0.9)}},
    ]

    # ── Helpers ───────────────────────────────────────────────────────────────
    def get_editor_world() -> unreal.World:
        return unreal.EditorLevelLibrary.get_editor_world()


    def spawn_bbox(
        world: unreal.World,
        name: str,
        location: unreal.Vector,
        scale: unreal.Vector,
        color_rgb: tuple,
    ) -> unreal.StaticMeshActor:
        \"\"\"Spawn a cube StaticMeshActor representing one habitat module.\"\"\"
        actor: unreal.StaticMeshActor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor,
            location,
        )
        actor.set_actor_label(name)

        mesh_comp: unreal.StaticMeshComponent = actor.static_mesh_component
        cube_mesh = unreal.EditorAssetLibrary.load_asset(
            "/Engine/BasicShapes/Cube.Cube"
        )
        mesh_comp.set_static_mesh(cube_mesh)
        mesh_comp.set_world_scale3d(scale)

        # Apply a simple vertex-color material tint for visual distinction
        mat = unreal.EditorAssetLibrary.load_asset(
            "/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"
        )
        mesh_comp.set_material(0, mat)

        # Tag the actor with metadata
        actor.tags = [
            unreal.Name(f"XBIM_{{name.replace(' ', '_')}}"),
            unreal.Name(f"Planet_{{HABITAT_CONFIG['planet']}}"),
            unreal.Name(f"Shielding_{{HABITAT_CONFIG['shielding_cm']}}cm"),
        ]

        return actor


    # ── Main Spawn Routine ────────────────────────────────────────────────────
    def spawn_habitat() -> None:
        world  = get_editor_world()
        sf     = HABITAT_CONFIG["scale_factor"]
        L      = HABITAT_CONFIG["length_m"] * sf
        W      = HABITAT_CONFIG["width_m"]  * sf
        H      = HABITAT_CONFIG["height_m"] * sf

        unreal.log(f"[X-BIM] Spawning {{HABITAT_CONFIG['planet']}} habitat — "
                   f"{{HABITAT_CONFIG['length_m']}}m × {{HABITAT_CONFIG['width_m']}}m × {{HABITAT_CONFIG['height_m']}}m")

        spawned_actors = []

        for mod in MODULES:
            loc = unreal.Vector(
                mod["offset_x"] * L,
                mod["offset_y"] * W,
                H * 0.5,                   # rest on ground plane
            )
            scale = unreal.Vector(
                mod["scale_x"] * L / 100.0,
                mod["scale_y"] * W / 100.0,
                mod["scale_z"] * H / 100.0,
            )

            actor = spawn_bbox(
                world,
                name      = f"XBIM_{{mod['name']}}",
                location  = loc,
                scale     = scale,
                color_rgb = mod["color"],
            )
            spawned_actors.append(actor)
            unreal.log(f"  [+] Spawned: {{mod['name']}}  @ {{loc}}")

        unreal.log(
            f"[X-BIM] Done — {{len(spawned_actors)}} modules spawned.\\n"
            f"        Structural system : {{HABITAT_CONFIG['struct_system']}}\\n"
            f"        Foundation        : {{HABITAT_CONFIG['foundation']}}\\n"
            f"        Internal setpoint : {{HABITAT_CONFIG['setpoint_c']}} °C"
        )


    if __name__ == "__main__":
        spawn_habitat()
    """).strip()


# ──────────────────────────────────────────────────────────────────────────────
# Main generation flow
# ──────────────────────────────────────────────────────────────────────────────
if generate_btn:
    if not api_key:
        st.error("⚠️  Please enter your Gemini API key in the sidebar.")
        st.stop()
    if not isru_materials:
        st.error("⚠️  Please specify at least one ISRU material.")
        st.stop()

    with st.spinner("Querying Gemini — generating habitat engineering analysis…"):
        try:
            prompt  = build_prompt(planet, radiation_cm, isru_materials)
            data    = call_gemini(api_key, prompt)
        except json.JSONDecodeError as e:
            st.error(f"❌  Gemini returned invalid JSON: {e}")
            st.stop()
        except Exception as e:
            st.error(f"❌  Gemini API error: {e}")
            st.stop()

    # ── Store in session state for persistence across reruns ──
    st.session_state["xbim_data"]   = data
    st.session_state["xbim_planet"] = planet
    st.session_state["xbim_rad"]    = radiation_cm
    st.session_state["xbim_isru"]   = isru_materials
    st.session_state["xbim_dims"]   = (hab_length, hab_width, hab_height)

# ──────────────────────────────────────────────────────────────────────────────
# Results — only show if we have data
# ──────────────────────────────────────────────────────────────────────────────
if "xbim_data" in st.session_state:
    data          = st.session_state["xbim_data"]
    s_planet      = st.session_state["xbim_planet"]
    s_rad         = st.session_state["xbim_rad"]
    s_isru        = st.session_state["xbim_isru"]
    s_len, s_wid, s_hei = st.session_state["xbim_dims"]

    struct  = data.get("structural_spec", {})
    thermal = data.get("thermal_requirements", {})
    reqs    = data.get("requirements_table", [])

    st.success(f"Analysis complete — {len(reqs)} requirements generated for **{s_planet}** habitat.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Structural Spec",
        "Thermal Requirements",
        "Requirements Table",
        "Downloads",
    ])

    # ── Tab 1: Structural Spec ──────────────────────────────────────────────
    with tab1:
        st.subheader("Structural Specification")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Primary Structure**")
            st.info(struct.get("primary_structure", "—"))
            st.markdown("**Foundation Type**")
            st.info(struct.get("foundation_type", "—"))
            st.markdown("**Pressure Vessel**")
            st.info(struct.get("pressure_vessel", "—"))
        with c2:
            st.markdown("**Safety Factor**")
            sf_val = struct.get("safety_factor", "—")
            st.metric("Factor of Safety", sf_val)
            st.markdown("**Key Structural Loads**")
            for load in struct.get("key_loads", []):
                st.markdown(f"- {load}")
        st.markdown("---")
        st.markdown("### Engineering Narrative")
        st.markdown(struct.get("summary", "—"))

    # ── Tab 2: Thermal Requirements ─────────────────────────────────────────
    with tab2:
        st.subheader("Thermal Requirements")
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown("**Surface Temperature Range**")
            st.warning(thermal.get("surface_temp_range_C", "—"))
            st.markdown("**Internal Setpoint**")
            st.metric("°C", thermal.get("internal_setpoint_C", "—"))
            st.markdown("**Insulation Strategy**")
            st.info(thermal.get("insulation_strategy", "—"))
        with tc2:
            st.markdown("**Active Thermal Control**")
            st.info(thermal.get("active_thermal_ctrl", "—"))
            st.markdown("**Heat Rejection**")
            st.info(thermal.get("heat_rejection", "—"))
        st.markdown("---")
        st.markdown("### Thermal Narrative")
        st.markdown(thermal.get("summary", "—"))

    # ── Tab 3: Requirements Table ───────────────────────────────────────────
    with tab3:
        st.subheader(f"Systems Requirements — {s_planet} Habitat ({len(reqs)} items)")

        # Priority filter
        priorities = ["All"] + sorted({r.get("priority", "") for r in reqs})
        selected_priority = st.selectbox("Filter by Priority", priorities)

        filtered = reqs if selected_priority == "All" else [
            r for r in reqs if r.get("priority") == selected_priority
        ]

        # Category filter
        cats = ["All"] + sorted({r.get("category", "") for r in reqs})
        selected_cat = st.selectbox("Filter by Category", cats)
        if selected_cat != "All":
            filtered = [r for r in filtered if r.get("category") == selected_cat]

        st.markdown(f"Showing **{len(filtered)}** of **{len(reqs)}** requirements.")

        for req in filtered:
            priority_label = {"High": "[H]", "Medium": "[M]", "Low": "[L]"}.get(
                req.get("priority", ""), "[ ]"
            )
            with st.expander(
                f"{priority_label}  {req.get('req_id', '')} — {req.get('requirement', '')[:80]}…"
            ):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"**Full Requirement:** {req.get('requirement', '')}")
                    st.markdown(f"**Rationale:** {req.get('rationale', '')}")
                with col_b:
                    st.markdown(f"**Category:** `{req.get('category', '')}`")
                    st.markdown(f"**Verification:** `{req.get('verification', '')}`")
                    st.markdown(f"**Priority:** `{req.get('priority', '')}`")

    # ── Tab 4: Downloads ────────────────────────────────────────────────────
    with tab4:
        st.subheader("Export Artefacts")
        st.markdown(
            "Download the generated outputs for integration with your MBSE "
            "toolchain and Unreal Engine 5 pipeline."
        )

        dl1, dl2 = st.columns(2)

        # ── MBSE CSV ──
        with dl1:
            st.markdown("### MBSE CSV — Cameo Systems Modeler")
            st.markdown(
                "A SysML-compatible requirements table exportable directly "
                "into **Cameo Systems Modeler** via the CSV Import wizard."
            )
            csv_str  = build_mbse_csv(data, s_planet, s_rad, s_isru)
            csv_name = f"XBIM_{s_planet}_MBSE_Requirements.csv"
            st.download_button(
                label     = "Download MBSE CSV",
                data      = csv_str,
                file_name = csv_name,
                mime      = "text/csv",
                use_container_width=True,
            )
            with st.expander("Preview CSV"):
                st.code(csv_str[:2000], language="text")

        # ── UE5 Script ──
        with dl2:
            st.markdown("### UE5 Python — Procedural Habitat Generator")
            st.markdown(
                "Run this script inside **Unreal Engine 5** (Tools → Execute Python "
                "Script) to procedurally spawn all habitat bounding boxes at world origin."
            )
            ue5_script  = build_ue5_script(
                s_planet, s_rad, s_isru, s_len, s_wid, s_hei, data
            )
            ue5_name = f"XBIM_{s_planet}_UE5_Habitat.py"
            st.download_button(
                label     = "Download UE5 Python Script",
                data      = ue5_script,
                file_name = ue5_name,
                mime      = "text/x-python",
                use_container_width=True,
            )
            with st.expander("Preview UE5 Script"):
                st.code(ue5_script[:3000], language="python")

        st.markdown("---")
        st.markdown("### Raw JSON Response")
        with st.expander("View Gemini JSON payload"):
            st.json(data)

# ──────────────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#4a6a8a; font-size:0.82rem;'>"
    "X-BIM · Extraterrestrial Building Information Modeling · "
    "Powered by Google Gemini &nbsp;|&nbsp; Built for deep-space habitat design"
    "</p>",
    unsafe_allow_html=True,
)
