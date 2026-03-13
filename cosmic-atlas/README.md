# 🌌 CosmicAtlas

> **Explore the Universe Beyond Earth** — a cinematic, interactive space exploration web app built with Streamlit + n8n AI.

---

## ✨ Features

| Section | Description |
|---|---|
| 🌌 **Hero** | Animated galaxy background, parallax starfield, shooting stars |
| 🪐 **Solar System** | All 8 planets with stats, rotating orbs, glowing cards |
| 🕳️ **Deep Space** | Galaxies, nebulae, black holes, neutron stars |
| 🤖 **Space AI** | Chat interface powered by your n8n webhook |
| 📡 **Dashboard** | Live NASA asteroid data, ISS tracker, Astronomy Picture of the Day |
| 🗺️ **Journey** | Scroll from Earth orbit to the edge of the universe |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
cd cosmic-atlas
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

Opens at → **http://localhost:8501**

---

## 🤖 Space AI (n8n Integration)

### Step 1 — Start n8n
```bash
# With Docker
docker run -it --rm -p 5678:5678 n8nio/n8n

# Or npm
npx n8n
```

### Step 2 — Import the workflow
1. Open **http://localhost:5678**
2. Go to **Workflows → Import**
3. Upload `n8n_workflow.json`
4. Add your **OpenAI API key** to the credentials
5. **Activate** the workflow

### Step 3 — Test the webhook
```bash
curl -X POST http://localhost:5678/webhook/space-ai \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a black hole?"}'
```

Expected response:
```json
{ "response": "A black hole is..." }
```

---

## 📁 Project Structure

```
cosmic-atlas/
├── app.py                    ← Main Streamlit application
├── space_ui.css              ← Cinematic space theme
├── requirements.txt
├── n8n_workflow.json         ← Import into n8n
├── .streamlit/
│   └── config.toml           ← Dark theme config
└── animations/
    └── starfield.js          ← Star field, nebula, shooting stars
```

---

## 🌐 Live APIs Used

| API | Data |
|---|---|
| [NASA NeoWs](https://api.nasa.gov/) | Near-Earth asteroids |
| [NASA APOD](https://api.nasa.gov/) | Astronomy Picture of the Day |
| [Open Notify](http://api.open-notify.org/) | ISS live position |
| n8n webhook | AI answers about space |

---

## 🎨 Design

- **Deep space gradient** background: `#020111` → `#000000`  
- **Animated starfield** with 3-layer parallax (mouse + scroll)
- **Nebula clouds** drifting with radial gradients  
- **Shooting stars** spawned randomly  
- **Typography**: Orbitron (headings) + Space Grotesk + Exo 2  
- **Colors**: Neon blue `#00d4ff` · Neon purple `#bf5fff` · Neon cyan `#00ffea`
