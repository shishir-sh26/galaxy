"""
CosmicAtlas – Streamlit Space Exploration Application
======================================================
A cinematic, interactive space exploration app with:
  • Animated starfield + nebula (JS canvas)
  • Interactive solar system planet cards
  • Deep space objects explorer
  • Space Explorer AI (n8n webhook)
  • Cosmic Data Dashboard (live NASA / Open-Notify APIs)
"""

import streamlit as st
import requests
import json
import time
import math
import random
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ── Load Environment ───────────────────────────────────────
load_dotenv()

# ── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="CosmicAtlas – Explore the Universe",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load CSS & Inject JS ────────────────────────────────────
def load_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""

css  = load_file("space_ui.css")
js   = load_file("animations/starfield.js")

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown(f"<script>{js}</script>",  unsafe_allow_html=True)

# ── N8N Config ─────────────────────────────────────────────
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/space-ai")
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

# ── Celestial Body Data ─────────────────────────────────────
PLANETS = [
    {
        "name": "THE SUN", "emoji": "☀️",
        "color": "#ffcc33", "glow": "#ffae00",
        "gradient": "radial-gradient(circle at 35% 30%, #fff700, #ffae00 45%, #ff7700 75%, #ff3300 100%)",
        "distance": "0 km", "size": "1.39M km", "moons": "8 planets",
        "temp": "15 million°C", "day": "27 Earth days",
        "fact": "The Sun contains 99.86% of the mass in the entire solar system.",
    },
    {
        "name": "MERCURY", "emoji": "⚫",
        "color": "#b5b5b5", "glow": "#888888",
        "gradient": "radial-gradient(circle at 35% 30%, #d4d4d4, #888888 55%, #444 100%)",
        "distance": "57.9M km", "size": "4,879 km", "moons": "0",
        "temp": "430°C / -180°C", "day": "58.6 Earth days",
        "fact": "The smallest planet — a year lasts just 88 Earth days.",
    },
    {
        "name": "VENUS", "emoji": "🟡",
        "color": "#f5deb3", "glow": "#e8c56d",
        "gradient": "radial-gradient(circle at 35% 30%, #ffeaa7, #f0a500 55%, #c67c00 100%)",
        "distance": "108.2M km", "size": "12,104 km", "moons": "0",
        "temp": "465°C", "day": "243 Earth days",
        "fact": "Hotter than Mercury despite being farther from the Sun.",
    },
    {
        "name": "EARTH", "emoji": "🌍",
        "color": "#4fa3e0", "glow": "#00d4ff",
        "gradient": "radial-gradient(circle at 35% 30%, #87ceeb, #4fa3e0 40%, #2a7d3e 70%, #1a4d6a 100%)",
        "distance": "149.6M km", "size": "12,742 km", "moons": "1",
        "temp": "15°C avg", "day": "24 hours",
        "fact": "The only known planet harboring life in the universe.",
    },
    {
        "name": "MARS", "emoji": "🔴",
        "color": "#c1440e", "glow": "#ff6633",
        "gradient": "radial-gradient(circle at 35% 30%, #e8704a, #c1440e 55%, #7a1c00 100%)",
        "distance": "227.9M km", "size": "6,779 km", "moons": "2",
        "temp": "−63°C avg", "day": "24h 37m",
        "fact": "Home to Olympus Mons — the tallest volcano in the solar system.",
    },
    {
        "name": "JUPITER", "emoji": "🟠",
        "color": "#c88b3a", "glow": "#ffaa44",
        "gradient": "radial-gradient(circle at 35% 30%, #f0c87a, #c88b3a 45%, #8b5a1a 75%, #d4a04a 100%)",
        "distance": "778.5M km", "size": "139,820 km", "moons": "95",
        "temp": "−145°C", "day": "9h 56m",
        "fact": "The Great Red Spot is a storm larger than Earth, raging for 400+ years.",
    },
    {
        "name": "SATURN", "emoji": "🪐",
        "color": "#e4d191", "glow": "#ffe080",
        "gradient": "radial-gradient(circle at 35% 30%, #fef3b0, #e4d191 50%, #b8a040 100%)",
        "distance": "1.43B km", "size": "116,460 km", "moons": "146",
        "temp": "−178°C", "day": "10h 42m",
        "fact": "Saturn's rings are made of ice and rock, spanning 282,000 km.",
    },
    {
        "name": "URANUS", "emoji": "🔵",
        "color": "#7de8e8", "glow": "#00ffea",
        "gradient": "radial-gradient(circle at 35% 30%, #aff5f5, #7de8e8 55%, #3ab8b8 100%)",
        "distance": "2.87B km", "size": "50,724 km", "moons": "28",
        "temp": "−224°C", "day": "17h 14m",
        "fact": "Uranus rotates on its side — its axial tilt is 97.77°.",
    },
    {
        "name": "NEPTUNE", "emoji": "🌀",
        "color": "#3f54ba", "glow": "#5577ff",
        "gradient": "radial-gradient(circle at 35% 30%, #6688ff, #3f54ba 55%, #1a2472 100%)",
        "distance": "4.50B km", "size": "49,244 km", "moons": "16",
        "temp": "−218°C", "day": "16h 6m",
        "fact": "Winds on Neptune reach 2,100 km/h — the fastest in the solar system.",
    },
]

# ── Deep Space Objects ──────────────────────────────────────
DEEP_SPACE = [
    {
        "icon": "🌀", "title": "Milky Way Galaxy",
        "color": "#ffffff", "glow_var": "rgba(255,255,255,0.1)",
        "desc": "Our home galaxy — a barred spiral containing 200–400 billion stars across 100,000 light-years.",
        "fact": "📏 Diameter: ~100,000 light-years | ⭐ Stars: ~300 billion",
    },
    {
        "icon": "🕳️", "title": "Sagittarius A*",
        "color": "#dddddd", "glow_var": "rgba(200,200,200,0.1)",
        "desc": "The supermassive black hole at the center of the Milky Way, 4 million times the mass of our Sun.",
        "fact": "📏 Event Horizon: ~24M km | 🌡️ Accretion disk: > 1 trillion °C",
    },
    {
        "icon": "💥", "title": "Crab Nebula",
        "color": "#cccccc", "glow_var": "rgba(180,180,180,0.1)",
        "desc": "The remnant of a supernova explosion observed in 1054 AD — an expanding cloud of glowing gas and dust.",
        "fact": "📏 Diameter: ~11 light-years | 📅 Supernova: July 4, 1054",
    },
    {
        "icon": "🌌", "title": "Andromeda Galaxy",
        "color": "#eeeeee", "glow_var": "rgba(240,240,240,0.1)",
        "desc": "Our nearest large galactic neighbor — a spiral galaxy 2.537 million light-years away, destined to collide with the Milky Way.",
        "fact": "📏 Diameter: ~220,000 ly | 🔭 Visible to the naked eye",
    },
    {
        "icon": "🌸", "title": "Orion Nebula",
        "color": "#bbbbbb", "glow_var": "rgba(150,150,150,0.1)",
        "desc": "A stellar nursery 1,344 light-years away where new stars are actively being born from clouds of gas and dust.",
        "fact": "📏 Diameter: ~24 light-years | ⭐ Contains 2,000+ young stars",
    },
    {
        "icon": "💫", "title": "Pillars of Creation",
        "color": "#d4d4d4", "glow_var": "rgba(210,210,210,0.1)",
        "desc": "Iconic towers of cosmic gas and dust in the Eagle Nebula — stellar nurseries stretching up to 4–5 light-years.",
        "fact": "📏 Height: ~4-5 light-years | 📅 Imaged by Hubble: 1995",
    },
    {
        "icon": "⚡", "title": "Neutron Star PSR",
        "color": "#ffffff", "glow_var": "rgba(255,255,255,0.15)",
        "desc": "The ultra-dense remnant of a massive star — packing more than 1 solar mass into a sphere just 20 km across.",
        "fact": "📏 Diameter: ~20 km | 🌡️ Surface: ~600,000°C",
    },
    {
        "icon": "🌊", "title": "Gravitational Waves",
        "color": "#cccccc", "glow_var": "rgba(180,180,180,0.08)",
        "desc": "Ripples in spacetime caused by violent cosmic events like merging black holes — first detected by LIGO in 2015.",
        "fact": "🏆 Nobel Prize: 2017 | 📡 Detected by LIGO & Virgo",
    },
]

# ── Journey Waypoints ───────────────────────────────────────
JOURNEY = [
    ("🌍 Earth Orbit",      "400 km above Earth — where the ISS glides at 28,000 km/h"),
    ("🌙 The Moon",         "384,400 km away — 3 days by Apollo spacecraft"),
    ("☀️ Inner Solar System", "Mercury, Venus, Earth & Mars in the habitable zone"),
    ("🪨 Asteroid Belt",    "Between Mars & Jupiter — millions of rocky remnants"),
    ("🌀 Gas Giants",       "Jupiter & Saturn — massive worlds of swirling storms"),
    ("🧊 Ice Giants",       "Uranus & Neptune — the cold blue frontier"),
    ("❄️ Kuiper Belt",      "30–50 AU — home of Pluto and icy dwarf planets"),
    ("🌑 Heliopause",       "Interstellar space begins — where solar wind fades to nothing"),
    ("🌌 Milky Way Core",   "26,000 light-years to the galactic center"),
    ("✨ Observable Universe", "93 billion light-years — the edge of what we can see"),
]

# ── Utility: n8n request ────────────────────────────────────
def ask_space_ai(message: str) -> str:
    """Send a question to the n8n Space AI workflow."""
    try:
        resp = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": message},
            timeout=30,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code == 200:
            data = resp.json()
            # Handle both wrapped and unwrapped response formats
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            return data.get("response") or data.get("output") or data.get("text") or str(data)
        else:
            return f"⚠️ AI service responded with status {resp.status_code}. Please check your n8n workflow."
    except requests.exceptions.ConnectionError:
        return (
            "🔌 **n8n not connected** — Start your n8n instance at `http://localhost:5678` "
            "and import `n8n_workflow.json`. The Space AI will then answer your questions!"
        )
    except requests.exceptions.Timeout:
        return "⏳ The AI is contemplating the cosmos... Request timed out. Try again!"
    except Exception as e:
        return f"🛸 Unexpected error: {e}"

# ── Utility: NASA / Open-Notify APIs ───────────────────────
@st.cache_data(ttl=120)
def get_iss_location():
    try:
        r = requests.get("http://api.open-notify.org/iss-now.json", timeout=8)
        if r.status_code == 200:
            d = r.json()
            return {
                "lat": float(d["iss_position"]["latitude"]),
                "lon": float(d["iss_position"]["longitude"]),
                "timestamp": d["timestamp"],
            }
    except Exception:
        pass
    return {"lat": 51.5, "lon": -0.1, "timestamp": 0, "error": True}

@st.cache_data(ttl=3600)
def get_near_earth_asteroids():
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        url = (
            f"https://api.nasa.gov/neo/rest/v1/feed?"
            f"start_date={today}&end_date={today}&api_key={NASA_API_KEY}"
        )
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            neos = []
            for date_key in data.get("near_earth_objects", {}).values():
                for neo in date_key[:5]:
                    cd = neo["close_approach_data"][0] if neo["close_approach_data"] else {}
                    neos.append({
                        "name": neo["name"].strip("()"),
                        "diameter_m": round(
                            (neo["estimated_diameter"]["meters"]["estimated_diameter_min"] +
                             neo["estimated_diameter"]["meters"]["estimated_diameter_max"]) / 2
                        ),
                        "velocity_kmh": round(float(cd.get("relative_velocity", {}).get("kilometers_per_hour", 0))),
                        "miss_km": round(float(cd.get("miss_distance", {}).get("kilometers", 0))),
                        "hazardous": "🔴 YES" if neo["is_potentially_hazardous_asteroid"] else "🟢 No",
                    })
            return neos[:8]
    except Exception:
        pass
    return []

@st.cache_data(ttl=7200)
def get_apod():
    try:
        r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}", timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

# ═══════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px;">
      <span style="font-family:'Orbitron',sans-serif; font-size:1.1rem;
                   color:#00d4ff; letter-spacing:0.15em;">🌌 COSMIC ATLAS</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Exo 2',sans-serif; font-size:0.8rem;
                color:rgba(232,244,253,0.5); letter-spacing:0.1em; text-transform:uppercase;">
        Navigation
    </div>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "", ["🌌 Hero", "🪐 Solar System", "🕳️ Deep Space",
             "🤖 Space AI", "📡 Cosmic Dashboard", "🗺️ Journey"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Exo 2',sans-serif; font-size:0.75rem; color:rgba(232,244,253,0.35); text-align:center;">
        n8n Webhook<br>
        <span style="color:rgba(0,212,255,0.5);">localhost:5678/webhook/space-ai</span>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  HERO SECTION
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-section cosmic-section">
  <div class="hero-galaxy-bg"></div>
  <h1 class="hero-title">CosmicAtlas</h1>
  <p class="hero-subtitle">Explore the Universe Beyond Earth</p>
  <p class="hero-tagline">From our solar system to the edge of the observable universe</p>
  <div class="scroll-indicator">
    <span>Scroll to explore</span>
    <div class="scroll-arrow"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  SOLAR SYSTEM SECTION
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="cosmic-section" id="solar-system">
  <h2 class="section-heading">☀️ Solar System</h2>
  <p class="section-subheading">Eight worlds orbiting our star</p>
  <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

# Build planet grid in Streamlit columns
cols = st.columns(4)
for i, planet in enumerate(PLANETS):
    with cols[i % 4]:
        st.markdown(f"""
        <div class="planet-card">
          <div class="planet-orb"
               style="background:{planet['gradient']};
                      box-shadow: 0 0 30px {planet['glow']}55, 0 0 60px {planet['glow']}22;"></div>
          <div class="planet-name">{planet['name']}</div>
          <div class="planet-stats">
            <div class="stat-row">
              <span>Distance</span>
              <span class="stat-value">{planet['distance']}</span>
            </div>
            <div class="stat-row">
              <span>Diameter</span>
              <span class="stat-value">{planet['size']}</span>
            </div>
            <div class="stat-row">
              <span>Moons</span>
              <span class="stat-value">{planet['moons']}</span>
            </div>
            <div class="stat-row">
              <span>Temp</span>
              <span class="stat-value">{planet['temp']}</span>
            </div>
            <div class="stat-row">
              <span>Day length</span>
              <span class="stat-value">{planet['day']}</span>
            </div>
          </div>
          <div style="margin-top:14px; font-family:'Exo 2',sans-serif; font-size:0.75rem;
                      color:rgba(0,212,255,0.65); line-height:1.5; font-style:italic;">
            {planet['fact']}
          </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  DEEP SPACE SECTION
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="cosmic-section" id="deep-space" style="background:
  radial-gradient(ellipse 100% 50% at 80% 50%, rgba(107,47,160,0.08), transparent);">
  <h2 class="section-heading">🕳️ Deep Space</h2>
  <p class="section-subheading">Beyond the solar system — galaxies, nebulae & black holes</p>
  <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

cols2 = st.columns(4)
for i, obj in enumerate(DEEP_SPACE):
    with cols2[i % 4]:
        st.markdown(f"""
        <div class="deep-card" style="--card-glow:{obj['glow_var']};">
          <span class="deep-card-icon">{obj['icon']}</span>
          <div class="deep-card-title" style="color:{obj['color']};">{obj['title']}</div>
          <div class="deep-card-desc">{obj['desc']}</div>
          <div class="deep-card-fact">{obj['fact']}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  SPACE EXPLORER AI SECTION
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="cosmic-section" id="space-ai">
  <h2 class="section-heading">🤖 Space Explorer AI</h2>
  <p class="section-subheading">Ask anything about the cosmos — powered by n8n</p>
  <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "ai",
            "content": "🌌 Welcome to CosmicAtlas AI! I'm your astrophysics guide. Ask me anything — from the birth of stars to the fate of the universe!"
        }
    ]

col_chat, col_tips = st.columns([2, 1])

with col_chat:
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-header">
      <div class="chat-status-dot"></div>
      <span class="chat-title">COSMOS AI — ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

    # Build message HTML
    messages_html = '<div class="chat-body" id="chat-body">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            messages_html += f"""
            <div class="msg-user">
              <div class="msg-label">YOU</div>
              {msg['content']}
            </div>"""
        else:
            messages_html += f"""
            <div class="msg-ai">
              <div class="msg-label">COSMOS AI</div>
              {msg['content']}
            </div>"""
    messages_html += '</div>'
    st.markdown(messages_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Auto-scroll to bottom
    st.markdown("""
    <script>
    setTimeout(() => {
      const el = document.getElementById('chat-body');
      if (el) el.scrollTop = el.scrollHeight;
    }, 200);
    </script>
    """, unsafe_allow_html=True)

    # Input area
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            user_q = st.text_input(
                "Ask the cosmos...",
                placeholder="e.g. What happens inside a black hole?",
                label_visibility="collapsed",
            )
        with col_btn:
            submitted = st.form_submit_button("🚀 Send")

    if submitted and user_q.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        with st.spinner("🌌 Consulting the cosmos..."):
            answer = ask_space_ai(user_q)
        st.session_state.chat_history.append({"role": "ai", "content": answer})
        st.rerun()

with col_tips:
    st.markdown("""
    <div class="deep-card" style="height:100%;">
      <span class="deep-card-icon">💡</span>
      <div class="deep-card-title" style="color:#00d4ff; margin-bottom:16px;">Explore Topics</div>
      <div style="display:flex; flex-direction:column; gap:8px;">
    """, unsafe_allow_html=True)

    suggestions = [
        ("🕳️", "What is a black hole?"),
        ("🌟", "How are stars born?"),
        ("🪐", "Tell me about Saturn's rings"),
        ("🌌", "How big is the universe?"),
        ("🚀", "What is dark matter?"),
        ("💫", "How does gravity work?"),
        ("☀️", "Will the Sun die?"),
        ("👽", "Is there life on Mars?"),
    ]

    for emoji, suggestion in suggestions:
        if st.button(f"{emoji} {suggestion}", key=f"sug_{suggestion[:15]}"):
            st.session_state.chat_history.append({"role": "user", "content": suggestion})
            with st.spinner("🌌 Consulting the cosmos..."):
                answer = ask_space_ai(suggestion)
            st.session_state.chat_history.append({"role": "ai", "content": answer})
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  COSMIC DATA DASHBOARD
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="cosmic-section" id="dashboard">
  <h2 class="section-heading">📡 Cosmic Data Dashboard</h2>
  <p class="section-subheading">Live data from space — updated in real time</p>
  <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🪨 Near-Earth Asteroids", "🛰️ ISS Tracker", "🔭 NASA Picture of the Day"])

# ── Tab 1: Asteroids ────────────────────────────────────────
with tab1:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.markdown("""
        <div class="metric-card">
          <div class="metric-icon">🪨</div>
          <div class="metric-value" id="neo-count">—</div>
          <div class="metric-label">NEOs Today</div>
        </div>""", unsafe_allow_html=True)
    with metric_cols[1]:
        st.markdown("""
        <div class="metric-card">
          <div class="metric-icon">⚡</div>
          <div class="metric-value">~25 km/s</div>
          <div class="metric-label">Avg Velocity</div>
        </div>""", unsafe_allow_html=True)
    with metric_cols[2]:
        st.markdown("""
        <div class="metric-card">
          <div class="metric-icon">📡</div>
          <div class="metric-value">NASA NEO</div>
          <div class="metric-label">Data Source</div>
        </div>""", unsafe_allow_html=True)
    with metric_cols[3]:
        st.markdown("""
        <div class="metric-card">
          <div class="metric-icon">🔴</div>
          <div class="metric-value">Live</div>
          <div class="metric-label">Feed Status</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    neos = get_near_earth_asteroids()
    if neos:
        import pandas as pd
        df = pd.DataFrame(neos)
        df.columns = ["Name", "Diameter (m)", "Velocity (km/h)", "Miss Distance (km)", "Hazardous"]
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.markdown("""
        <div class="metric-card" style="text-align:left; padding:28px;">
          <div style="font-family:'Orbitron',sans-serif; font-size:0.9rem; color:#00d4ff; margin-bottom:12px;">
            📡 NASA API – Sample Asteroid Data
          </div>
          <div style="font-family:'Exo 2',sans-serif; font-size:0.85rem; color:rgba(232,244,253,0.6); line-height:1.8;">
            • <b style="color:#fff;">2024 BX1</b> — Diameter: 1.2m | Velocity: 13,900 km/h | Miss: 360,000 km | 🟢 No<br>
            • <b style="color:#fff;">Apophis (99942)</b> — Diameter: 370m | Velocity: 30,700 km/h | Miss: 31,000 km | 🟢 No<br>
            • <b style="color:#fff;">2023 DZ2</b> — Diameter: 40m | Velocity: 28,200 km/h | Miss: 174,000 km | 🟢 No<br>
            • <b style="color:#fff;">Bennu (101955)</b> — Diameter: 490m | Velocity: 28,000 km/h | Miss: 7.5M km | 🟢 No
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Tab 2: ISS Tracker ──────────────────────────────────────
with tab2:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    iss = get_iss_location()

    iss_cols = st.columns(3)
    with iss_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-icon">🛰️</div>
          <div class="metric-value" style="font-size:1.4rem;">{iss['lat']:.2f}°</div>
          <div class="metric-label">Latitude</div>
        </div>""", unsafe_allow_html=True)
    with iss_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-icon">🌍</div>
          <div class="metric-value" style="font-size:1.4rem;">{iss['lon']:.2f}°</div>
          <div class="metric-label">Longitude</div>
        </div>""", unsafe_allow_html=True)
    with iss_cols[2]:
        st.markdown("""
        <div class="metric-card">
          <div class="metric-icon">⚡</div>
          <div class="metric-value" style="font-size:1.4rem;">28,000</div>
          <div class="metric-label">km/h Orbital Speed</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Simple SVG world map with ISS position
    x_pct = (iss["lon"] + 180) / 360 * 100
    y_pct = (90 - iss["lat"]) / 180 * 100

    st.markdown(f"""
    <div class="metric-card" style="padding:20px; position:relative;">
      <div style="font-family:'Orbitron',sans-serif; font-size:0.8rem; color:#00d4ff;
                  letter-spacing:0.12em; margin-bottom:14px;">🛰️ ISS CURRENT POSITION</div>
      <div style="position:relative; background:rgba(0,212,255,0.04);
                  border:1px solid rgba(0,212,255,0.12); border-radius:12px;
                  padding:0; overflow:hidden; height:220px;">
        <!-- Simple grid lines -->
        <svg width="100%" height="220" style="position:absolute; inset:0;"
             viewBox="0 0 800 220" preserveAspectRatio="none">
          <!-- Horizontal grid -->
          <line x1="0" y1="55"  x2="800" y2="55"  stroke="rgba(0,212,255,0.08)" stroke-width="1"/>
          <line x1="0" y1="110" x2="800" y2="110" stroke="rgba(0,212,255,0.12)" stroke-width="1"/>
          <line x1="0" y1="165" x2="800" y2="165" stroke="rgba(0,212,255,0.08)" stroke-width="1"/>
          <!-- Vertical grid -->
          <line x1="200" y1="0" x2="200" y2="220" stroke="rgba(0,212,255,0.08)" stroke-width="1"/>
          <line x1="400" y1="0" x2="400" y2="220" stroke="rgba(0,212,255,0.12)" stroke-width="1"/>
          <line x1="600" y1="0" x2="600" y2="220" stroke="rgba(0,212,255,0.08)" stroke-width="1"/>
          <!-- Orbit path (approximate) -->
          <ellipse cx="400" cy="110" rx="380" ry="55"
                   stroke="rgba(0,212,255,0.2)" stroke-width="1"
                   stroke-dasharray="6,4" fill="none"/>
          <!-- ISS position marker -->
          <circle cx="{x_pct * 8}" cy="{y_pct * 2.2}"
                  r="8" fill="#00d4ff" opacity="0.9">
            <animate attributeName="r" values="8;14;8" dur="2s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.9;0.4;0.9" dur="2s" repeatCount="indefinite"/>
          </circle>
          <!-- ISS label -->
          <text x="{min(x_pct * 8 + 14, 720)}" y="{y_pct * 2.2 + 5}"
                fill="#00d4ff" font-size="11" font-family="Orbitron,monospace">🛰️ ISS</text>
          <!-- Labels -->
          <text x="4" y="115" fill="rgba(232,244,253,0.3)" font-size="9">0°</text>
          <text x="4" y="62"  fill="rgba(232,244,253,0.3)" font-size="9">45°N</text>
          <text x="4" y="168" fill="rgba(232,244,253,0.3)" font-size="9">45°S</text>
        </svg>
      </div>
      <div style="margin-top:12px; font-family:'Exo 2',sans-serif; font-size:0.78rem;
                  color:rgba(232,244,253,0.4); text-align:center;">
        Source: Open Notify API · Updates every 2 minutes
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Tab 3: APOD ─────────────────────────────────────────────
with tab3:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    apod = get_apod()

    if apod:
        col_img, col_txt = st.columns([3, 2])
        with col_img:
            if apod.get("media_type") == "image":
                st.image(apod.get("url", ""), use_container_width=True)
            else:
                st.markdown(f"""
                <div class="metric-card" style="padding:24px;">
                  <p style="color:#00d4ff; font-family:'Orbitron',sans-serif; font-size:0.85rem;">
                    📹 Today's astronomy media is a video
                  </p>
                  <a href="{apod.get('url','#')}" target="_blank"
                     style="color:#bf5fff; font-family:'Exo 2',sans-serif;">
                    Watch on NASA ↗
                  </a>
                </div>""", unsafe_allow_html=True)
        with col_txt:
            st.markdown(f"""
            <div class="deep-card" style="height:100%;">
              <div class="deep-card-title" style="color:#00d4ff; font-size:1rem; line-height:1.4;">
                {apod.get('title', 'NASA Astronomy Picture of the Day')}
              </div>
              <div style="font-family:'Exo 2',sans-serif; font-size:0.75rem;
                          color:rgba(0,212,255,0.5); margin:8px 0 16px; letter-spacing:0.1em;">
                {apod.get('date', '')}
              </div>
              <div class="deep-card-desc" style="max-height:300px; overflow-y:auto;">
                {apod.get('explanation', '')}
              </div>
              <div style="margin-top:14px; font-size:0.73rem; color:rgba(232,244,253,0.3);
                          font-family:'Exo 2',sans-serif;">
                Credit: {apod.get('copyright', 'NASA / ESA')}
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card" style="padding:32px; text-align:center;">
          <div style="font-size:3rem; margin-bottom:16px;">🔭</div>
          <div style="font-family:'Orbitron',sans-serif; color:#00d4ff; font-size:0.9rem; margin-bottom:12px;">
            NASA Astronomy Picture of the Day
          </div>
          <div style="font-family:'Exo 2',sans-serif; color:rgba(232,244,253,0.5); font-size:0.85rem;">
            Each day NASA features a stunning image of the cosmos with an explanation written by astronomers.
            Connect to the internet to load today's picture.
          </div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  COSMIC JOURNEY SECTION
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="cosmic-section" id="journey">
  <h2 class="section-heading">🗺️ Journey Through Space</h2>
  <p class="section-subheading">Scroll from Earth orbit to the edge of the observable universe</p>
  <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

# Two-column zig-zag journey
left_col, right_col = st.columns([1, 1])
for i, (label, desc) in enumerate(JOURNEY):
    col = left_col if i % 2 == 0 else right_col
    with col:
        depth_pct = int((i / (len(JOURNEY) - 1)) * 100)
        # Monochrome colors: from white to dark gray
        gray_val = max(100, 255 - i * 15)
        color = f"rgb({gray_val},{gray_val},{gray_val})"
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:20px; text-align:left;
             border-left: 3px solid {color}; border-radius:4px 18px 18px 4px;">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
            <span style="font-size:0.7rem; font-family:'Orbitron',sans-serif;
                         color:rgba(232,244,253,0.3); letter-spacing:0.1em;">
              DEPTH {depth_pct}%
            </span>
          </div>
          <div style="font-family:'Orbitron',sans-serif; font-size:0.9rem;
                      color:{color}; margin-bottom:6px;">
            {label}
          </div>
          <div style="font-family:'Exo 2',sans-serif; font-size:0.8rem;
                      color:rgba(232,244,253,0.55); line-height:1.5;">
            {desc}
          </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div style="
  text-align: center;
  padding: 60px 20px 40px;
  border-top: 1px solid rgba(0,212,255,0.1);
  margin-top: 60px;
">
  <div style="font-family:'Orbitron',sans-serif; font-size:1.2rem;
              background: linear-gradient(90deg,#00d4ff,#bf5fff);
              -webkit-background-clip:text; -webkit-text-fill-color:transparent;
              background-clip:text; margin-bottom:12px; letter-spacing:0.1em;">
    🌌 CosmicAtlas
  </div>
  <div style="font-family:'Exo 2',sans-serif; font-size:0.8rem;
              color:rgba(232,244,253,0.3); letter-spacing:0.15em; margin-bottom:8px;">
    EXPLORE · DISCOVER · UNDERSTAND
  </div>
  <div style="font-family:'Exo 2',sans-serif; font-size:0.72rem;
              color:rgba(232,244,253,0.2);">
    Data: NASA APIs · Open Notify · n8n AI Workflow
  </div>
</div>
""", unsafe_allow_html=True)

# ── Auto-inject Canvas JS on every render ──────────────────
# (Canvas must be re-injected after Streamlit rerenders)
st.markdown(
    f"<script>{js}</script>",
    unsafe_allow_html=True,
)
