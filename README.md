# 🌍 Terra-BIM (Extreme Biome Information Modeling)

**Hackathon:** MSS2026 SpaceApps (Track 1B Capstone)  
**SDGs Addressed:** SDG 11 (Sustainable Cities and Communities) & SDG 13 (Climate Action)  
**Live Demo:** [Streamlit Deployment](https://extraterrestrialbim.streamlit.app)  

---

## 📌 Project Vision
Climate change is creating extreme environments across the globe. From Tornado Alleys in the US to flood-prone regions in Southeast Asia, communities need rapid, data-driven structural designs for resilient housing and disaster-relief shelters. **Terra-BIM** is a generative design dashboard that translates Earth Observation data into actionable architectural specifications.

## 🎯 Stakeholders & Human-Centered Design (HCD)
Our primary users are **Disaster Response Coordinators, NGO Leads, and Urban Planners**. 
Instead of forcing users to manually calculate wind loads or flood elevations, the user simply inputs the hazard environment and its intensity. Terra-BIM acts as an "Earth-based Resilient Structural Engineer," hiding the complex cloud-based calculations behind a beautiful, intuitive, and tactile "Neumorphic" interface.

## 🧪 The Solution & Dynamic Data Integration
Terra-BIM replaces generic construction planning with real-time adaptation:
1. **Hazard Profiles:** Users select extreme weather risks (Hurricanes, Tornadoes, Floods, Wildfires, Earthquakes) and input Hazard Intensity.
2. **Local Materials:** The app factors in sustainable, localized resources (Bamboo, Rammed Earth, Recycled Ocean Plastics).
3. **Generative Analysis:** Powered by the Google Gemini API, the app generates a comprehensive MBSE (Model-Based Systems Engineering) structural specification, including aerodynamic profiles, foundation types, and thermal requirements.

## 🎨 UI/UX & Immersive Deployment
The application features a modern, tactile **Skeuomorphic/Neumorphic design**, creating a physical "instrument" feel that grounds the user experience. 
Going beyond 2D data, Terra-BIM bridges the gap between analysis and visualization by exporting a **Procedural Python Script** that automatically generates the aerodynamic shelter geometry (e.g., monolithic domes for wind deflection) directly into **Unreal Engine 5** for 1:1 scale Virtual Reality walkthroughs.

---

## 🛠️ Installation & Usage

1. **Clone the repository**
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
   streamlit run app.py
   ```
5. **VR Export:**
   Click "Download UE5 Python Script", open any Unreal Engine 5 project, and navigate to **Tools → Execute Python Script** to spawn the generated resilient shelter geometry.
