# 🌍 MANTIS: Procedural Resilience System

**Hackathon:** MSS2026 SpaceApps (Track 1B Capstone)  
**SDGs Addressed:** SDG 11 (Sustainable Cities and Communities) & SDG 13 (Climate Action)  
**Live Demo:** [https://mantis.streamlit.app/](https://mantis.streamlit.app/)  

---

## 📌 Project Vision
Climate change is creating extreme environments across the globe. From Tornado Alleys in the US to flood-prone regions in Southeast Asia, communities need rapid, data-driven structural designs for resilient housing and disaster-relief shelters. **MANTIS** is an intelligent generative design dashboard that translates Earth Observation data into actionable architectural specifications.

## 🎯 Stakeholders & Human-Centered Design (HCD)
Our primary users are **Disaster Response Coordinators, NGO Leads, and Urban Planners**. 
Instead of forcing users to manually calculate wind loads or flood elevations, the user simply inputs the spatial coordinates. MANTIS acts as an "Earth-based Resilient Structural Engineer," hiding complex cloud-based hazard calculations behind a cinematic, intuitive, and tactile dark-mode engineering interface.

## 🧪 The Solution & Dynamic Data Integration
MANTIS replaces generic construction planning with real-time procedural adaptation:
1. **Spatial Intelligence:** Users select a geographic target. The system extracts historical natural disaster risks (Hurricanes, Tornadoes, Floods, Seismic activity).
2. **Local Materials:** The app factors in sustainable, localized in-situ resources (Bamboo, Rammed Earth, Recycled Ocean Plastics).
3. **Generative Analysis:** Powered by the Google Gemini 1.5 API, the app mathematically maps hazard inputs to structural schemas, generating comprehensive MBSE (Model-Based Systems Engineering) structural specifications.

## 🎨 UI/UX & Immersive Deployment
The application features a modern, cinematic entry sequence inspired by high-end industrial design (LoveFrom-style minimalism), transitioning into a robust data dashboard. 
Going beyond 2D data, MANTIS bridges the gap between analysis and visualization by exporting a **Procedural Python Script** that automatically generates the aerodynamic shelter geometry directly into **Unreal Engine 5** for 1:1 scale Virtual Reality walkthroughs.

---

## 🛠️ Installation & Deployment Instructions

### Local Development
1. **Clone the repository:**
   ```bash
   git clone https://github.com/arhimatrix/X-BIM.git
   cd X-BIM
   ```
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your Gemini API Key:**
   Create a `.streamlit/secrets.toml` file and add:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
4. **Run the App:**
   ```bash
   streamlit run app_earth.py
   ```

### Unreal Engine 5 VR Export
Click the **"Download UE5 Python Script"** button in the MANTIS dashboard. Open any Unreal Engine 5 project, and navigate to **Tools → Execute Python Script** to procedural spawn the generated resilient shelter modules.
