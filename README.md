# 🌌 CosmicAtlas

> **Explore the Universe Beyond Earth** — a cinematic, interactive space exploration web app built with Streamlit + n8n AI.

---

## 🔭 Vision

**CosmicAtlas** aims to democratize space exploration by blending immersive, cinematic web design with cutting-edge artificial intelligence and real-time astronomical data. Our vision is to create a digital observatory where anyone—from curious students to amateur astronomers—can journey from Earth's orbit to the edges of the observable universe, interacting with a vast repository of cosmic knowledge guided by an intelligent, context-aware AI.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🌌 **Cinematic Hero** | Animated galaxy background, parallax starfield, and deep-space scroll effects. |
| 🪐 **Interactive Solar System** | Detailed, glowing planetary cards with real-time stats (distance, moons, temp). |
| 🕳️ **Deep Space Explorer** | Educational profiles on galaxies, nebulae, black holes, and neutron stars. |
| 🤖 **Space Explorer AI** | A conversational, neon-styled AI chatbot acting as your personal astrophysicist. |
| 📡 **Live Cosmic Dashboard** | Real-time integrations displaying Near-Earth Asteroids, ISS tracking, and NASA's APOD. |
| 🗺️ **Cosmic Journey** | A scrolling visual timeline traveling from Earth orbit to the edge of the universe. |

---

## 🛠️ Technical Stack

CosmicAtlas is built using a modern, lightweight, and highly interactive Python stack:

*   **Frontend / UI Framework:** [Streamlit](https://streamlit.io/) (Python)
*   **Custom Styling:** Vanilla CSS (`space_ui.css`) with glassmorphism, glowing neons, and monochrome aesthetics.
*   **Animations:** Custom JavaScript (`starfield.js`) HTML5 Canvas for dense parallax starfields.
*   **Backend Automation:** [n8n](https://n8n.io/) (Node-based workflow automation tool).
*   **Data Processing:** Python (`pandas`, `requests`, `python-dotenv`).

---

## 🧠 AI & Language Models Used

The **Space Explorer AI** within CosmicAtlas is driven by state-of-the-art Large Language Models (LLMs) orchestrated through n8n:

*   **Primary Language Model:** OpenAI's `gpt-4o-mini`.
*   **Role:** The model is strictly prompted via a System Message to act as *"CosmicAtlas AI — an expert astrophysics assistant with deep knowledge of the universe."*
*   **Capabilities:** It processes user queries, formats responses with structural clarity and emojis, and delivers scientifically accurate, poetic insights into astrophysics, cosmology, and space missions.

---

## 🤖 n8n Workflow Integration

The AI chat is completely decoupled from the frontend code, executing remotely via an **n8n Workflow**.

### How it works:
1.  **Trigger:** Streamlit sends a `POST` request to the n8n Webhook URL.
2.  **Processing (LangChain Agent):** n8n receives the message, passes it to the OpenAI LangChain node (`gpt-4o-mini`), applying the CosmicAtlas system prompt.
3.  **Response:** n8n formats the AI's output into JSON and responds to the Streamlit webhook.

### How to set it up:
1.  Start your n8n instance (`npx n8n` or Docker).
2.  Go to **Workflows → Import** and upload the included `n8n_workflow.json`.
3.  Add your **OpenAI API Key** to the n8n credentials.
4.  **Activate** the workflow.
*Ensure your `.env` file points `N8N_WEBHOOK_URL` to your active n8n webhook route.*

---

## 🌍 Real-World Use Cases

1.  **Educational Institutions:** Teachers can use CosmicAtlas as an interactive white-board aide to visually explain the solar system, while students can interrogate the AI about complex topics like black hole thermodynamics.
2.  **Amateur Astronomers:** Users can quickly check the **Cosmic Dashboard** before a night of stargazing to see the Astronomy Picture of the Day or track if the ISS will be visible passing overhead.
3.  **Science Communicators & Museums:** A beautiful, kiosk-ready interface that can be deployed on touchscreens to engage the public with real-time NASA data and near-earth asteroid tracking.
4.  **Hackathon Basecamp:** A perfect template for developers wanting to learn how to integrate Python frontend frameworks (Streamlit) with external, no-code AI automation pipelines (n8n).

---

## 🚀 Quick Start

### 1. Install Dependencies
Ensure you have Python 3.9+ installed.
```bash
cd cosmic-atlas
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root directory (or rename a template if you have one):
```env
NASA_API_KEY=your_nasa_api_key_here
N8N_WEBHOOK_URL=http://localhost:5678/webhook/space-ai
```

### 3. Run the App
```bash
python -m streamlit run app.py
```
Opens at → **http://localhost:8501**

---

## 🌐 Live APIs Used

| API | Data |
|---|---|
| [NASA NeoWs](https://api.nasa.gov/) | Near-Earth asteroids |
| [NASA APOD](https://api.nasa.gov/) | Astronomy Picture of the Day |
| [Open Notify](http://api.open-notify.org/) | ISS live position |
| Local n8n Webhook | AI answers about space |

---

## 📁 Project Structure

```
cosmic-atlas/
├── app.py                    ← Main Streamlit application
├── space_ui.css              ← Cinematic monochrome space theme
├── requirements.txt          ← Python dependencies
├── n8n_workflow.json         ← Importable n8n AI workflow
├── .env                      ← Secret keys & URLs (Ignored by git)
├── .gitignore                ← Repo configuration
├── .streamlit/
│   └── config.toml           ← Streamlit dark theme config
└── animations/
    └── starfield.js          ← HTML5 Canvas dense starfield engine
```
