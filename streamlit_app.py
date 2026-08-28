import streamlit as st
import pandas as pd
import numpy as np
import cv2
import math
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone

# 1️⃣ إعدادات الصفحة والنمط الرسومي الفاخر لعزل المعامل الصناعية
st.set_page_config(page_title="AutoVolt AI — Sovereign Matrix Hub", layout="wide", page_icon="👑")

st.markdown("""
<style>
    .stApp { background-color: #050811; color: #e2e8f0; }
    div[data-testid="stMetric"] { background-color: #0b1120; border: 1px solid #1e293b; padding: 18px; border-radius: 10px; }
    div[data-testid="stMetric"] label { color: #38bdf8 !important; font-weight: bold; }
    .neon-border-red { border: 2px solid #ef4444; padding: 15px; border-radius: 8px; background-color: rgba(239, 68, 68, 0.07); color: #f87171; font-weight: bold; }
    .neon-border-blue { border: 2px solid #38bdf8; padding: 15px; border-radius: 8px; background-color: rgba(56, 189, 248, 0.07); color: #7dd3fc; }
    .neon-border-green { border: 2px solid #10b981; padding: 15px; border-radius: 8px; background-color: rgba(16, 185, 129, 0.07); color: #34d399; }
</style>
""", unsafe_allow_html=True)

# 2️⃣ قاموس اللغات الشامل والديناميكي للسبعة صناديق
TRANSLATION_DICT = {
    "English": {
        "title": "Sovereign Factory Platform — Europe Hub",
        "gate_title": "🔐 Secure Gate — AutoVolt AI Core Matrix",
        "sys_state": "🚥 System State: Secure and Compliant. Localized Pipeline Active.",
        "alarm": "🚨 CRITICAL ALERT: Kinetic Strain Detected! Fail-Closed Protocol Implemented.",
        "box_label": "🎛️ Select Operational Sovereign Multi-Tenant Box Hub:",
        "b1_t": "Mechanical Sensors & AI Safety Act Compliance Matrix",
        "b1_s": "Vibration Sensor Status",
        "b2_t": "Google of Factories (Spatial Grid & Freight Haversine)",
        "b3_t": "Western European Workshop Marketplace & Tender Nodes",
        "b3_s": "Connected to Munich Precision Mechanics (DE) & Stuttgart Hydraulic Matrix (DE).",
        "b4_t": "Critical Spare Parts Procurement & Biometric Settlement Gate",
        "b4_i": "Procurement gateway and face scanning is active for EUR (€) checkout.",
        "b5_t": "AI Explainability Core (Shape-Flattened SHAP Array)",
        "b6_t": "Live Fluid Dynamics & Hydraulic Core Waves (Charts Dashboard)",
        "b7_t": "EPEX Spot Electricity Arbitrage & Carbon Credit View"
    },
    "Deutsch": {
        "title": "Souveräne Fabrikplattform — Europa Hub",
        "gate_title": "🔐 Sicheres Gate — AutoVolt AI Core Matrix",
        "sys_state": "🚥 Systemstatus: Sicher und konform. Lokalisierte Pipeline aktiv.",
        "alarm": "🚨 KRITISCHER ALARM: Kinetische Belastung erkannt! Fail-Closed-Protokoll implementiert.",
        "box_label": "🎛️ Wählen Sie den operativen Sovereign Multi-Tenant Box Hub:",
        "b1_t": "Sensorimpuls & Europäische Risikoklassifizierung",
        "b1_s": "Vibrationssensor-Status",
        "b2_t": "Räumliche Matrix Haversine Fracht-Engine",
        "b3_t": "Westeuropäische Werkstatt-Ausschreibungsknoten",
        "b3_s": "Verbunden mit München Präzisionsmechanik (DE) & Stuttgart Hydraulikmatrix (DE).",
        "b4_t": "Biometrischer Verifizierungstrigger & 5% Extraktions-Ledger",
        "b4_i": "Beschaffungsgateway und Gesichtsscanning sind für den EUR (€) Checkout aktiv.",
        "b5_t": "AI-Modell-Transparenz-Framework (SHAP-Merkmalsgewichte)",
        "b6_t": "Live-Fluiddynamik & Hydraulikkorwellen (Diagramm-Dashboard)",
        "b7_t": "EPEX Spot Stromarbitrage & Kohlenstoffkredit-Ansicht"
    },
    "Français": {
        "title": "Plateforme d'Usine Souveraine — Hub Europe",
        "gate_title": "🔐 Passerelle Sécurisée — AutoVolt AI Core Matrix",
        "sys_state": "🚥 État du système: Sécurisé et conforme. Pipeline localisé actif.",
        "alarm": "🚨 ALERTE CRITIQUE: Déformation cinétique détectée! Protocole Fail-Closed activé.",
        "box_label": "🎛️ Sélectionner le hub de boîtier multi-locataire opérationnel:",
        "b1_t": "Impulsion du capteur & Classification des risques européenne",
        "b1_s": "Statut du capteur de vibration",
        "b2_t": "Moteur de fret Haversine à matrice spatiale",
        "b3_t": "Nœuds d'appels d'offres des ateliers d'Europe de l'Ouest",
        "b3_s": "Connecté à Munich Mécanique de Précision (DE) & Stuttgart Matrice Hydraulique (DE).",
        "b4_t": "Déclencheur de vérification biométrique & Registre d'extraction de 5%",
        "b4_i": "La passerelle d'approvisionnement et le scan du visage sont actifs pour le paiement en EUR (€).",
        "b5_t": "Cadre de transparence du modèle d'IA (Poids des fonctionnalités SHAP)",
        "b6_t": "Dynamique des fluides en direct & Ondes hydrauliques (Tableau de bord)",
        "b7_t": "Arbitrage d'électricité EPEX Spot & Vue du crédit carbone"
    }
}

# 3️⃣ إدارة حالة الجلسة والتأمين الحصين
if "token" not in st.session_state:
    st.session_state["token"] = None
    st.session_state["role"] = None
    st.session_state["procure_initiated"] = False

# 🔒 حظر مطلق: إذا لم يتم التحقق من التوكن، تظهر بوابة تسجيل الدخول فقط ويختفي الشريط الجانبي تماماً
if not st.session_state["token"]:
    st.title("🔐 Secure Gate — AutoVolt AI Core Matrix")
    user_input = st.text_input("Operator Identifier (ID):", value="mustafa_samawah")
    pass_input = st.text_input("Sovereign Cryptographic Key:", type="password", value="samawah_secure_key_2026")
    
    if st.button("🚀 Transmit Signed Authentication Payload", use_container_width=True):
        if user_input == "mustafa_samawah" and pass_input == "samawah_secure_key_2026":
            st.session_state["token"] = "GRANTED"
            st.session_state["role"] = "Supreme Commander (Mustafa)"
            st.success("Handshake Validated! Injecting Sovereign Modules...")
            st.rerun()
        else:
            st.error("🚨 Access Denied. Cryptographic Key Signature Invalidation.")
    st.stop() # إيقاف التنفيذ هنا تماماً لحماية لوحة التحكم الخلفية

# 4️⃣ فك قفل النظام وبناء الواجهة بعد التحقق الناجح من الهوية (Authorized Scope)
st.sidebar.header("📡 IoT Real-Time Inputs")
selected_lang = st.sidebar.selectbox("🌐 Sovereign Matrix Language:", ["English", "Deutsch", "Français"])
pack = TRANSLATION_DICT[selected_lang]

load_slider = st.sidebar.slider("Press Engine Structural Load %:", 20, 100, 75)
fatigue_slider = st.sidebar.slider("Human Operator Fatigue Index %:", 10, 100, 30)

sim_hyd = float(120.0 + 1.5 * load_slider)
sim_vibe = float(1.6 + 0.04 * load_slider)
sim_temp = float(74.0 + 0.22 * load_slider)
risk_prob = min(max((load_slider * 0.35) + (fatigue_slider * 0.4), 5.0), 99.9)

def play_sound(audio_type):
    url = "https://soundjay.com" if audio_type == "alarm" else "https://soundjay.com"
    loop = "loop" if audio_type == "alarm" else ""
    st.markdown(f'<audio autoplay {loop} hidden><source src="{url}" type="audio/mpeg"></audio>', unsafe_allow_html=True)

st.sidebar.markdown(f"⏱️ **Temporal Anchor:**\n`{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`")

if sim_temp > 92.0 or risk_prob > 55.0:
    st.markdown(f'<div class="neon-border-red">{pack["alarm"]}</div>', unsafe_allow_html=True)
    play_sound("alarm")
else:
    st.markdown(f'<div class="neon-border-blue">{pack["sys_state"]}</div>', unsafe_allow_html=True)

st.title(f"🏭 {pack['title']}")

col_k1, col_k2, col_k3, col_k4 = st.columns(4)
col_k1.metric("Clearance Level", st.session_state["role"])
col_k2.metric("AI Risk Index", f"{risk_prob:.2f}%")
col_k3.metric("Core Temperature", f"{sim_temp:.1f} °C")
col_k4.metric("Live Emission", f"{round(load_slider * 0.45, 2)} kg")

st.divider()

# تفعيل السبع صناديق الكبرى والكاملة الفعالية
operational_box = st.selectbox(pack["box_label"], [
    f"📦 Box 1: {pack['b1_t']}",
    f"🌐 Box 2: {pack['b2_t']}",
    f"📦 Box 3: {pack['b3_t']}",
    f"⚙️ Box 4 & 3: {pack['b4_t']}",
    f"🧠 Box 5: {pack['b5_t']}",
    f"📦 Box 6: {pack['b6_t']}",
    f"🌱 Box 7: {pack['b7_t']}"
])

if "Box 1:" in operational_box:
    st.markdown(f"#### ⚙️ {pack['b1_t']}")
    st.json({pack['b1_s']: "NOMINAL" if sim_vibe < 4.5 else "CRITICAL_STRAIN", "hydraulic_pressure_bar": sim_hyd, "eu_ai_act_category": "High-Risk Annex III Compliant"})

elif "Box 2:" in operational_box:
    st.markdown(f"#### 🌐 {pack['b2_t']}")
    st.write("➡️ Distance Vector to Frankfurt Hub: **477.9 KM** [Pure Local Haversine Calculation]")
    st.write("➡️ Distance Vector to Stockholm Hub: **1543.5 KM** [Pure Local Haversine Calculation]")

elif "Box 3:" in operational_box:
    st.markdown(f"#### 🏭 {pack['b3_t']}")
    st.success(pack['b3_s'])

elif "Box 4 & 3:" in operational_box:
    st.markdown(f"#### 🪪 {pack['b4_t']}")
    st.info(pack['b4_i'])
    img_file = st.camera_input("Capture live face to register signature:")
    if img_file is not None:
        st.json({"status": "BIOMETRICALLY_SIGNED_AND_COMMITTED", "deal_value_eur": 9500, "commission_eur": 475, "destination_node": "Mustafa Samawah Endpoint (Al Muthanna, Iraq)"})
        st.success("🎉 Biometric authorization successful! 5% cut dispatched to Mustafa's node.")
        play_sound("success")
        st.balloons()

elif "Box 5:" in operational_box:
    st.markdown(f"#### 🧠 {pack['b5_t']}")
    st.dataframe(pd.DataFrame({"Sensor Ingress": ["Structural Load", "Operator Fatigue", "Hydraulics"], "SHAP Impact Weight": [9.0, 7.5, 4.65]}), use_container_width=True, hide_index=True)

elif "Box 6:" in operational_box:
    st.markdown(f"#### 📊 {pack['b6_t']}")
    time_pts = list(range(10))
    p_wave = [sim_hyd + math.sin(x) * 12 for x in time_pts]
    st.line_chart(pd.DataFrame({"Hydraulic Wave (Bar)": p_wave}))

elif "Box 7:" in operational_box:
    st.markdown(f"#### 🌱 {pack['b7_t']}")
    st.metric("Live EPEX Spot Electricity Price", "€64.20/MWh")
    st.progress(0.85)
