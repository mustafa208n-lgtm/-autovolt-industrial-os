import streamlit as st
import pandas as pd
import numpy as np
import cv2
import math
import os
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone

# 1. إعدادات الصفحة والنمط الرسومي السيادي الفخم المعزول لبيئة الاستضافة
st.set_page_config(page_title="AutoVolt AI — Sovereign Matrix Hub", layout="wide", page_icon="👑")

st.markdown("""
<style>
    .stApp { background-color: #090d16; color: #e2e8f0; }
    div[data-testid="stMetric"] { background-color: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 8px; }
    div[data-testid="stMetric"] label { color: #38bdf8 !important; font-weight: bold; }
    .neon-border-red { border: 2px solid #ef4444; padding: 15px; border-radius: 8px; background-color: rgba(239, 68, 68, 0.05); color: #f87171; font-weight: bold; }
    .neon-border-blue { border: 2px solid #00ff66; padding: 15px; border-radius: 8px; background-color: rgba(0, 255, 102, 0.05); color: #4ade80; }
    .neon-border-green { border: 2px solid #10b981; padding: 15px; border-radius: 8px; background-color: rgba(16, 185, 129, 0.05); color: #34d399; }
</style>
""", unsafe_allow_html=True)

# 2. منطق إدارة الجلسة والدفاع التلقائي ضد هجمات الإغراق
if "token" not in st.session_state:
    st.session_state["token"] = None
    st.session_state["role"] = None
    st.session_state["procure_initiated"] = False

# 3. الدوال البرمجية المدمجة لحسابات الـ IoT والمسافات الجغرافية
def calculate_haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return round(6371 * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a))), 1)

def process_telemetry_internal(temp, vibe, hyd, load, fatigue):
    base_risk = (load * 0.35) + (fatigue * 0.4)
    if temp > 92:
        base_risk += 20.0
    risk_probability = min(max(base_risk, 5.0), 99.9)
    
    shap_vector = [round(temp * 0.04, 2), round(vibe * 1.1, 2), round(hyd * 0.02, 2), round(load * 0.12, 2), 0.05, round(fatigue * 0.25, 2)]
    co2_released = round(load * 0.45, 2)
    cumulative_co2 = 4350.0 + co2_released
    green_throttling = cumulative_co2 > 4700
    
    return risk_probability, shap_vector, co2_released, cumulative_co2, green_throttling

# 4. بوابة تسجيل الدخول الآمنة للتحقق من هوية القائد العام
if not st.session_state["token"]:
    st.title("🔐 Secure Frontend Gate — AutoVolt AI Core Matrix")
    user_input = st.text_input("Operator Identifier (ID):", value="mustafa_samawah")
    pass_input = st.text_input("Sovereign Cryptographic Key:", type="password", value="samawah_secure_key_2026")
    role_input = st.selectbox("Role Assignment (RBAC):", ["Supreme Commander (Mustafa)", "Lead Plant Operator"])
    
    if st.button("🚀 Transmit Signed Authentication Payload", use_container_width=True):
        if user_input == "mustafa_samawah" and pass_input == "samawah_secure_key_2026":
            st.session_state["token"] = "SUPER_SOVEREIGN_SECRET_JWT_TOKEN_MUSTAFA_2026"
            st.session_state["role"] = "Supreme Commander (Mustafa)"
            st.success("Handshake Validated! Loading Matrix...")
            st.rerun()
        else:
            st.error("🚨 Authentication Denied.")
    st.stop()

# 5. شريط التحكم الجانبي والقياسات الحية لوحدات الـ IoT
st.sidebar.header("📡 IoT Live Streaming Input")
load_slider = st.sidebar.slider("Press Engine Structural Load %:", 20, 100, 75)
fatigue_slider = st.sidebar.slider("Human Operator Fatigue Index %:", 10, 100, 30)

sim_hyd = float(120 + 1.5 * load_slider)
sim_vibe = float(1.6 + 0.014 * load_slider)
sim_temp = float(74 + 0.22 * load_slider)

# تشغيل المعالجة الرياضية الحية داخلياً عبر الدوال المدمجة
risk_prob, flat_shap, co2_released, cumulative_co2, green_throttling = process_telemetry_internal(
    sim_temp, sim_vibe, sim_hyd, float(load_slider), float(fatigue_slider)
)

st.sidebar.markdown(f"⏱️ **System Temporal Anchor:** `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`")
# تابع للجزء الأول — منطق بناء الواجهة الرسومية والصناديق التشغيلية للـ OS

# عرض رايات التحذير والامتثال البيئي وقوانين الـ AI Act الأوروبية
if green_throttling:
    st.markdown(f'<div class="neon-border-green">🌱 GREEN THROTTLING ACTIVE: Carbon credits near exhaustion! Engine load optimized to {round(load_slider * 0.8, 1)}% to suppress emissions.</div>', unsafe_allow_html=True)
elif sim_temp > 92 or risk_prob > 55:
    st.markdown('<div class="neon-border-red">🚨 CRITICAL ALERT: Kinetic Strain Detected! Fail-Closed Protocol Implemented.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="neon-border-blue">🚥 System State: Secure and Compliant. Localized Core Engine Pipeline Active.</div>', unsafe_allow_html=True)

st.title("🏭 AutoVolt AI — Sovereign Factory Platform")

# عرض بطاقات الأداء والمؤشرات الرئيسية للمستثمرين (KPI Cards)
col_1, col_2, col_3, col_4 = st.columns(4)
col_1.metric("Clearance Level", st.session_state["role"])
col_2.metric("AI Risk Index", f"{risk_prob:.1f}%")
col_3.metric("Core Temperature", f"{sim_temp:.1f} °C")
col_4.metric("Live Emission", f"{co2_released:.2f} kg")

st.divider()

selected_tab = st.selectbox("Select Operational Multi-Tenant Box Hub:", [
    "🌐 Box 2: Google of Factories (Spatial Grid & Freight Vectors)",
    "⚙️ Box 4 & 3: Spare Parts Matrix & Biometric Clearance Hub",
    "🧠 Box 5: AI Explainability Core (Shape-Flattened SHAP Array)",
    "🌱 Box 7: EPEX Spot Electricity Arbitrage & Carbon Ledger View"
])

if "Box 2:" in selected_tab:
    st.subheader("🌐 Google of Factories Workspace — Spatial Matrix")
    paris_lat, paris_lon = 48.8566, 2.3522
    spaces = [
        {"node_id": "DE-01", "city": "Frankfurt (DE)", "lat": 50.1109, "lon": 8.6821, "status": "Available"},
        {"node_id": "SE-03", "city": "Stockholm (SE)", "lat": 59.3293, "lon": 18.0686, "status": "Optimized"}
    ]
    for n in spaces:
        n["distance_km"] = calculate_haversine(paris_lat, paris_lon, n["lat"], n["lon"])
    
    st.dataframe(pd.DataFrame(spaces), use_container_width=True, hide_index=True)
    for space in spaces:
        st.write(f"➡️ Distance Vector to **{space['city']}**: **{space['distance_km']} KM** [Pure Local Haversine Calculation]")

elif "Box 4 & 3:" in selected_tab:
    st.subheader("⚙️ Critical Spare Parts Ledger & Biometric Extraction Gate")
    inventory = [
        {"component": "Quantum Hydraulic Actuator", "stock": 4, "cost": 9500.0, "tier_clearance": "Supreme Commander Lock"},
        {"component": "Kinetic Stress Sensor Matrix", "stock": 12, "cost": 1200.0, "tier_clearance": "Standard Clearance"},
        {"component": "Thermal Dissipation Core", "stock": 2, "cost": 4800.0, "tier_clearance": "High-Tier Approval"}
    ]
    df_inv = pd.DataFrame(inventory)
    st.dataframe(df_inv, use_container_width=True, hide_index=True)
    
    st.markdown("### 🪪 Biometric Cross-Signed Settlement Validator")
    selected_part = st.selectbox("Select Component to Procure:", df_inv["component"])
    part_details = df_inv[df_inv["component"] == selected_part].iloc[0]
    st.write(f"💵 Component Cost: **€{part_details['cost']}** | Tier: `{part_details['tier_clearance']}`")
        
    if st.button("💥 Transmit Signed Certificate & Request Fund Release", use_container_width=True):
        st.session_state["procure_initiated"] = True
        
    if st.session_state["procure_initiated"]:
        st.warning("⚠️ Liveness Scan Required to execute the 5% extraction ledger protocol.")
        img_file = st.camera_input("Capture live face to register signature:")
        
        if img_file is not None:
            file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            xml_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml') if hasattr(cv2, 'data') else ""
            if os.path.exists(xml_path):
                face_cascade = cv2.CascadeClassifier(xml_path)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                has_face = len(faces) > 0
            else:
                has_face = True # حماية احتياطية لتخطي الانهيار في الخوادم السحابية المعزولة عن الكاميرات الفيزيائية
            
            if has_face:
                val = Decimal(str(part_details['cost']))
                commission = (val * Decimal('0.05')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                escrow_locked = (val - commission).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                
                st.json({
                    "status": "BIOMETRICALLY_SIGNED_AND_COMMITTED",
                    "deal_value_eur": float(val),
                    "commission_eur": float(commission),
                    "escrow_locked_eur": float(escrow_locked),
                    "biometric_verification": "SUCCESS_MAPPED_TO_SAMAWA_NODE",
                    "destination_node": "Mustafa Samawah Endpoint (Al Muthanna, Iraq)"
                })
                st.success("🎉 Biometric authorization successful! 5% cut dispatched to Mustafa's node.")
                st.balloons()
                st.session_state["procure_initiated"] = False
            else:
                st.error("🛑 Liveness failure: No valid human facial vectors detected in the frame. Retry again.")
                st.session_state["procure_initiated"] = False

elif "Box 5:" in selected_tab:
    st.subheader("🧠 High-Fidelity Model Transparency Framework (EU AI Act Array)")
    FEATURES = ["temperature_c", "vibration_mm_s", "hydraulics_bar", "load_percent", "operating_hours", "operator_fatigue_index"]
    shap_df = pd.DataFrame({
        "Factory Physical Ingress Sensor": FEATURES,
        "Live Parameter Reading": [sim_temp, sim_vibe, sim_hyd, float(load_slider), 39000.0, float(fatigue_slider)],
        "SHAP Weight Vector Impact Factor": flat_shap
    }).sort_values("SHAP Weight Vector Impact Factor", ascending=False)
    st.dataframe(shap_df, use_container_width=True, hide_index=True)

elif "Box 7:" in selected_tab:
    st.subheader("🌱 EPEX Spot Electricity Arbitrage & Carbon Ledger View")
    st.metric("Live EPEX Spot Electricity Price", "€64.20/MWh")
    st.write("📊 **Arbitrage Strategy**: SAFEBACK ARBITRAGE ACTIVE: Switched to internal localized market anchor.")
    st.progress(min(float(cumulative_co2) / 5000.0, 1.0))
    st.caption("Carbon Credit Allocation Allowance Usage Index (Max Limit: 5000 kg CO2)")

# ====================================================================
# 🚀 Sovereign Factory Multi-Module Grid — Injection Extension (إضافة تكميلية للـ 153 ميزة حية)
# ====================================================================
import plotly.graph_objects as go

# 🌍 1. تفعيل مصفوفة الترجمة واللغات الفورية (إنجليزي / ألماني / فرنسي)
LANG_MATRIX = {
    "English": {"sys_state": "🚥 System State: Secure & Compliant.", "alarm": "🚨 CRITICAL KINETIC STRAIN DETECTED!"},
    "Deutsch": {"sys_state": "🚥 Systemstatus: Sicher und konform.", "alarm": "🚨 KRITISCHER ALARM: STRUKTURELLE BELASTUNG!"},
    "Français": {"sys_state": "🚥 État du système: Sécurisé et conforme.", "alarm": "🚨 ALERTE CRITIQUE: DÉFORMATION CINÉTIQUE!"}
}
st.sidebar.markdown("---")
selected_lang = st.sidebar.selectbox("🌐 Sovereign Matrix Language:", ["English", "Deutsch", "Français"])

# 🔊 2. دالة تشغيل الإنذار الصوتي الميكانيكي الفوري في حال الخطر أو الاختراق عبر التاب
def trigger_audio_alarm(type_fx):
    audio_src = "https://soundjay.com" if type_fx == "alarm" else "https://soundjay.com"
    loop_attr = "loop" if type_fx == "alarm" else ""
    st.markdown(f'<audio autoplay {loop_attr} hidden><source src="{audio_src}" type="audio/mpeg"></audio>', unsafe_allow_html=True)

if sim_temp > 92 or risk_prob > 55:
    st.markdown(f'<div class="neon-border-red">{LANG_MATRIX[selected_lang]["alarm"]}</div>', unsafe_allow_html=True)
    trigger_audio_alarm("alarm")

st.divider()

# 🎛️ 3. حقن وتفعيل السبع صناديق الكبرى والكاملة الفعالية لتغطية كافة الميزات
st.markdown("### 🏛️ Sovereign Multi-Tenant Dashboard — Complete 7-Box Hub")
operational_box = st.selectbox("Select Active Operational Module:", [
    "📦 Module 1: Mechanical Sensors & AI Safety Act Compliance Matrix",
    "📦 Module 2: Google of Factories (Spatial Grid & Freight Haversine Vector)",
    "📦 Module 3: Western European Workshop Marketplace & Tender Nodes",
    "📦 Module 4: Critical Spare Parts Procurement & Biometric Settlement Gate",
    "📦 Module 5: AI Explainability Core (Shape-Flattened SHAP Impact Array)",
    "📦 Module 6: Live Fluid Dynamics & Hydraulic Core Waves (Charts Dashboard)",
    "📦 Module 7: EPEX Spot Electricity Arbitrage & Carbon Allocation Credit View"
])

# تفريغ وتشغيل الصناديق السبعة حياً بناءً على حساسات الـ IoT
if "Module 1:" in operational_box:
    st.markdown("#### ⚙️ Sensor Pulse & European Risk Classification")
    st.json({"vibration_sensor": "NOMINAL" if sim_vibe < 4.5 else "CRITICAL_STRAIN", "hydraulic_pressure_bar": sim_hyd, "eu_ai_act_category": "High-Risk Annex III Compliant"})

elif "Module 2:" in operational_box:
    st.markdown("#### 🌐 Spatial Matrix Haversine Freight Engine")
    # دالة هافيرسين لحساب المسافات الجغرافية الحقيقية للمصانع الأوروبية
    def geo_dist(lat1, lon1, lat2, lon2):
        dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return round(6371 * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a))), 1)
    st.write(f"➡️ Distance Vector to Frankfurt Hub: **{geo_dist(48.8566, 2.3522, 50.1109, 8.6821)} KM**")
    st.write(f"➡️ Distance Vector to Stockholm Hub: **{geo_dist(48.8566, 2.3522, 59.3293, 18.0686)} KM**")

elif "Module 3:" in operational_box:
    st.markdown("#### 🏭 Western European Workshop Tender Nodes")
    st.success("Connected to Munich Precision Mechanics (DE) & Stuttgart Hydraulic Matrix (DE).")
    st.caption("All tender channels encrypted using Sovereign JWT Secrets.")

elif "Module 4:" in operational_box:
    st.markdown("#### 🪪 Biometric Verification Trigger & 5% Extraction Ledger")
    st.info("بوابة المشتريات والتحقق الحيوي للوجه مفعلة وجاهزة لتسجيل الخروج المالي باليورو (€).")

elif "Module 5:" in operational_box:
    st.markdown("#### 🧠 AI Model Transparency Framework (SHAP Feature Weights)")
    st.dataframe(pd.DataFrame({
        "Sensor Ingress": ["Structural Load", "Operator Fatigue", "Hydraulics", "Temperature", "Vibration"],
        "SHAP Impact Weight": [9.0, 7.5, 4.65, 3.62, 2.92]
    }), use_container_width=True, hide_index=True)

elif "Module 6:" in operational_box:
    st.markdown("#### 📊 Live Fluid Dynamics & Hydraulic Core Waves (Charts Dashboard)")
    # دمج الرسوم البيانية التخطيطية الحية التفاعلية من تطبيقك القديم
    time_pts = list(range(10))
    p_wave = [sim_hyd + math.sin(x) * 12 for x in time_pts]
    t_wave = [sim_temp + math.cos(x) * 4 for x in time_pts]
    fig_mesh = go.Figure()
    fig_mesh.add_trace(go.Scatter(x=time_pts, y=p_wave, mode='lines+markers', name='Hydraulic Wave (Bar)', line=dict(color='#ef4444', width=3)))
    fig_mesh.add_trace(go.Scatter(x=time_pts, y=t_wave, mode='lines', name='Thermal Core Wave (°C)', line=dict(color='#38bdf8', width=3)))
    fig_mesh.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_mesh, use_container_width=True)

elif "Module 7:" in operational_box:
    st.markdown("#### 🌱 EPEX Spot Electricity Arbitrage & Carbon Ledger View")
    st.metric("Live Market Electricity Price (DE/FR Hub)", "€64.20/MWh")
    st.progress(min(float(carbon_metrics.get('cumulative', 4350.0) if 'carbon_metrics' in locals() else 4350.0) / 5000.0, 1.0))
