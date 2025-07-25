import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# ==================== CONFIGURACIÓN DE PÁGINA Y CSS MEJORADO ====================
st.set_page_config(
    page_title="MUPAI - Evaluación Fitness Personalizada",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
:root {
    --mupai-yellow: #F4C430;
    --mupai-dark-yellow: #DAA520;
    --mupai-black: #181A1B;
    --mupai-gray: #232425;
    --mupai-light-gray: #EDEDED;
    --mupai-white: #FFFFFF;
    --mupai-success: #27AE60;
    --mupai-warning: #F39C12;
    --mupai-danger: #E74C3C;
}
/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #1E1E1E 0%, #232425 100%);
}
.main-header {
    background: linear-gradient(135deg, var(--mupai-yellow) 0%, var(--mupai-dark-yellow) 100%);
    color: #181A1B;
    padding: 2rem 1rem;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(244, 196, 48, 0.20);
    animation: fadeIn 0.5s ease-out;
}
.content-card {
    background: #1E1E1E;
    padding: 2rem 1.3rem;
    border-radius: 16px;
    box-shadow: 0 5px 22px 0px rgba(244,196,48,0.07), 0 1.5px 8px rgba(0,0,0,0.11);
    margin-bottom: 1.7rem;
    border-left: 5px solid var(--mupai-yellow);
    animation: slideIn 0.5s;
}
.card-psmf {
    border-left-color: var(--mupai-warning)!important;
}
.card-success {
    border-left-color: var(--mupai-success)!important;
}
.content-card, .content-card * {
    color: #FFF !important;
    font-weight: 500;
    letter-spacing: 0.02em;
}
.stButton > button {
    background: linear-gradient(135deg, var(--mupai-yellow) 0%, var(--mupai-dark-yellow) 100%);
    color: #232425;
    border: none;
    padding: 0.85rem 2.3rem;
    font-weight: bold;
    border-radius: 28px;
    transition: all 0.3s;
    box-shadow: 0 4px 16px rgba(244, 196, 48, 0.18);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-size: 1.15rem;
}
.stButton > button:hover {
    filter: brightness(1.04);
    box-shadow: 0 7px 22px rgba(244, 196, 48, 0.24);
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > select {
    border: 2px solid var(--mupai-yellow)!important;
    border-radius: 11px!important;
    padding: 0.7rem 0.9rem!important;
    background: #232425!important;
    color: #fff!important;
    font-size: 1.13rem!important;
    font-weight: 600!important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label,
.stRadio label, .stCheckbox label, .stDateInput label, .stMarkdown,
.stExpander .streamlit-expanderHeader, .stExpander label, .stExpander p, .stExpander div {
    color: #fff !important;
    opacity: 1 !important;
    font-weight: 700 !important;
    font-size: 1.04rem !important;
}
.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: #e0e0e0 !important;
    opacity: 1 !important;
}
.stAlert > div {
    border-radius: 11px;
    padding: 1.1rem;
    border-left: 5px solid;
    background: #222326 !important;
    color: #FFF !important;
}
[data-testid="metric-container"] {
    background: linear-gradient(125deg, #252525 0%, #303030 100%);
    padding: 1.1rem 1rem;
    border-radius: 12px;
    border-left: 4px solid var(--mupai-yellow);
    box-shadow: 0 2.5px 11px rgba(0,0,0,0.11);
    color: #fff !important;
}
.streamlit-expanderHeader {
    background: linear-gradient(135deg, var(--mupai-gray) 70%, #242424 100%);
    border-radius: 12px;
    font-weight: bold;
    color: #FFF !important;
    border: 2px solid var(--mupai-yellow);
    font-size: 1.16rem;
}
.stRadio > div {
    background: #181A1B !important;
    padding: 1.1rem 0.5rem;
    border-radius: 10px;
    border: 2px solid transparent;
    transition: all 0.3s;
    color: #FFF !important;
}
.stRadio > div:hover {
    border-color: var(--mupai-yellow);
}
.stCheckbox > label, .stCheckbox > span {
    color: #FFF !important;
    opacity: 1 !important;
    font-size: 1.05rem;
}
.stProgress > div > div > div {
    background: linear-gradient(135deg, var(--mupai-yellow) 0%, var(--mupai-dark-yellow) 100%)!important;
    border-radius: 10px;
    animation: pulse 1.2s infinite;
}
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.92; }
    100% { opacity: 1; }
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px);} to { opacity: 1; transform: translateY(0);} }
@keyframes slideIn { from { opacity: 0; transform: translateX(-18px);} to { opacity: 1; transform: translateX(0);} }
.badge {
    display: inline-block;
    padding: 0.32rem 0.98rem;
    border-radius: 18px;
    font-size: 0.97rem;
    font-weight: 800;
    margin: 0.27rem;
    color: #FFF;
    background: #313131;
    border: 1px solid #555;
}
.badge-success { background: var(--mupai-success); }
.badge-warning { background: var(--mupai-warning); color: #222; border: 1px solid #b78a09;}
.badge-danger { background: var(--mupai-danger); }
.badge-info { background: var(--mupai-yellow); color: #1E1E1E;}
.dataframe {
    border-radius: 10px !important;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    background: #2A2A2A!important;
    color: #FFF!important;
}
hr {
    border: none;
    height: 2.5px;
    background: linear-gradient(to right, transparent, var(--mupai-yellow), transparent);
    margin: 2.1rem 0;
}
@media (max-width: 768px) {
    .main-header { padding: 1.2rem;}
    .content-card { padding: 1.1rem;}
    .stButton > button { padding: 0.5rem 1.1rem; font-size: 0.96rem;}
}
.content-card:hover {
    transform: translateY(-1.5px);
    box-shadow: 0 8px 27px rgba(0,0,0,0.17);
    transition: all 0.25s;
}
.gradient-text {
    background: linear-gradient(135deg, var(--mupai-yellow) 0%, var(--mupai-dark-yellow) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
    font-size: 1.11rem;
}
.footer-mupai {
    text-align: center;
    padding: 2.2rem 0.3rem 2.2rem 0.3rem;
    background: linear-gradient(135deg, #202021 0%, #232425 100%);
    border-radius: 15px;
    color: #FFF;
    margin-top: 2.2rem;
}
.footer-mupai h4 { color: var(--mupai-yellow); margin-bottom: 1.1rem;}
.footer-mupai a {
    color: var(--mupai-yellow);
    text-decoration: none;
    margin: 0 1.2rem;
    font-weight: 600;
    font-size: 1.01rem;
}
</style>
""", unsafe_allow_html=True)
# Header principal visual
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem; margin: 0; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
        🏋️ MUPAI
    </h1>
    <p style="font-size: 1.2rem; margin: 0.5rem 0; opacity: 0.9;">
        Muscle Up Performance Assessment Intelligence
    </p>
    <p style="font-size: 1rem; margin: 0; opacity: 0.8;">
        Tu evaluación fitness personalizada basada en ciencia
    </p>
</div>
""", unsafe_allow_html=True)

# --- Inicialización de estado de sesión robusta (solo una vez)
defaults = {
    "datos_completos": False,
    "correo_enviado": False,
    "datos_ejercicios": {},
    "niveles_ejercicios": {},
    "nombre": "",
    "telefono": "",
    "email_cliente": "",
    "edad": "",
    "sexo": "Hombre",
    "fecha_llenado": datetime.now().strftime("%Y-%m-%d"),
    "acepto_terminos": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Tarjetas visuales robustas
def crear_tarjeta(titulo, contenido, tipo="info"):
    colores = {
        "info": "var(--mupai-yellow)",
        "success": "var(--mupai-success)",
        "warning": "var(--mupai-warning)",
        "danger": "var(--mupai-danger)"
    }
    color = colores.get(tipo, "var(--mupai-yellow)")
    return f"""
    <div class="content-card" style="border-left-color: {color};">
        <h3 style="margin-bottom: 1rem;">{titulo}</h3>
        <div>{contenido}</div>
    </div>
    """

# Referencias funcionales mejoradas (CORREGIDO PARA MUJERES)
referencias_funcionales = {
    "Hombre": {
        "Flexiones": {"tipo": "reps", "niveles": [("Bajo", 10), ("Promedio", 20), ("Bueno", 35), ("Avanzado", 50)]},
        "Fondos": {"tipo": "reps", "niveles": [("Bajo", 5), ("Promedio", 12), ("Bueno", 20), ("Avanzado", 30)]},
        "Press banca": {"tipo": "reps_peso", "niveles": [("Bajo", (5, 40)), ("Promedio", (8, 60)), ("Bueno", (10, 80)), ("Avanzado", (10, 100))]},
        "Dominadas": {"tipo": "reps", "niveles": [("Bajo", 2), ("Promedio", 5), ("Bueno", 10), ("Avanzado", 15)]},
        "Remo invertido": {"tipo": "reps", "niveles": [("Bajo", 5), ("Promedio", 10), ("Bueno", 15), ("Avanzado", 20)]},
        "Sentadilla": {"tipo": "reps_peso", "niveles": [("Bajo", (5, 60)), ("Promedio", (8, 80)), ("Bueno", (10, 110)), ("Avanzado", (10, 140))]},
        "Peso muerto": {"tipo": "reps_peso", "niveles": [("Bajo", (5, 70)), ("Promedio", (8, 100)), ("Bueno", (10, 130)), ("Avanzado", (10, 180))]},
        "Hip thrust": {"tipo": "reps_peso", "niveles": [("Bajo", (5, 60)), ("Promedio", (8, 90)), ("Bueno", (10, 120)), ("Avanzado", (10, 150))]},
        "Plancha": {"tipo": "tiempo", "niveles": [("Bajo", 20), ("Promedio", 40), ("Bueno", 60), ("Avanzado", 90)]},
        "Ab wheel": {"tipo": "reps", "niveles": [("Bajo", 1), ("Promedio", 5), ("Bueno", 10), ("Avanzado", 15)]},
        "L-sit": {"tipo": "tiempo", "niveles": [("Bajo", 5), ("Promedio", 10), ("Bueno", 20), ("Avanzado", 30)]}
    },
    "Mujer": {
        "Flexiones": {"tipo": "reps", "niveles": [("Bajo", 2), ("Promedio", 8), ("Bueno", 15), ("Avanzado", 25)]},
        "Fondos": {"tipo": "reps", "niveles": [("Bajo", 1), ("Promedio", 4), ("Bueno", 10), ("Avanzado", 18)]},
        "Press banca": {"tipo": "reps_peso", "niveles": [("Bajo", (5, 20)), ("Promedio", (8, 30)), ("Bueno", (10, 40)), ("Avanzado", (10, 50))]},  # CORREGIDO
        "Dominadas": {"tipo": "reps", "niveles": [("Bajo", 0), ("Promedio", 1), ("Bueno", 3), ("Avanzado", 5)]},
        "Remo invertido": {"tipo": "reps", "niveles": [("Bajo", 2), ("Promedio", 5), ("Bueno", 10), ("Avanzado", 15)]},
        "Sentadilla": {"tipo": "reps_peso", "niveles": [("Bajo", (5, 30)), ("Promedio", (8, 50)), ("Bueno", (10, 70)), ("Avanzado", (10, 90))]},
        "Peso muerto": {"tipo": "reps_peso", "niveles": [("Bajo", (5, 30)), ("Promedio", (8, 50)), ("Bueno", (10, 70)), ("Avanzado", (10, 95))]},
        "Hip thrust": {"tipo": "reps_peso", "niveles": [("Bajo", (5, 30)), ("Promedio", (8, 60)), ("Bueno", (10, 90)), ("Avanzado", (10, 120))]},
        "Plancha": {"tipo": "tiempo", "niveles": [("Bajo", 15), ("Promedio", 30), ("Bueno", 50), ("Avanzado", 70)]},
        "Ab wheel": {"tipo": "reps", "niveles": [("Bajo", 0), ("Promedio", 3), ("Bueno", 7), ("Avanzado", 12)]},
        "L-sit": {"tipo": "tiempo", "niveles": [("Bajo", 3), ("Promedio", 8), ("Bueno", 15), ("Avanzado", 25)]}
    }
}

# === Funciones auxiliares para cálculos ===

def calcular_tmb_cunningham(mlg):
    """Calcula el TMB usando la fórmula de Cunningham."""
    try:
        mlg = float(mlg)
    except (TypeError, ValueError):
        mlg = 0.0
    return 370 + (21.6 * mlg)

def calcular_mlg(peso, porcentaje_grasa):
    """Calcula la Masa Libre de Grasa."""
    try:
        peso = float(peso)
        porcentaje_grasa = float(porcentaje_grasa)
    except (TypeError, ValueError):
        peso = 0.0
        porcentaje_grasa = 0.0
    return peso * (1 - porcentaje_grasa / 100)

def corregir_porcentaje_grasa(medido, metodo, sexo):
    """
    Corrige el porcentaje de grasa según el método de medición.
    Si el método es Omron, ajusta con tabla.
    Si InBody, aplica factor.
    Si BodPod, aplica factor por sexo.
    Si DEXA, devuelve el valor medido.
    """
    try:
        medido = float(medido)
    except (TypeError, ValueError):
        medido = 0.0

    if metodo == "Omron HBF-516 (BIA)":
        tabla = {
            5: 2.5, 6: 3.5, 7: 4.5, 8: 5.5, 9: 6.5,
            10: 7.5, 11: 8.5, 12: 9.5, 13: 10.5, 14: 11.5,
            15: 13.5, 16: 14.5, 17: 15.5, 18: 16.5, 19: 17.5,
            20: 20.5, 21: 21.5, 22: 22.5, 23: 23.5, 24: 24.5,
            25: 27.0, 26: 28.0, 27: 29.0, 28: 30.0, 29: 31.0,
            30: 33.5, 31: 34.5, 32: 35.5, 33: 36.5, 34: 37.5,
            35: 40.0, 36: 41.0, 37: 42.0, 38: 43.0, 39: 44.0,
            40: 45.0
        }
        grasa_redondeada = int(round(medido))
        grasa_redondeada = min(max(grasa_redondeada, 5), 40)
        return tabla.get(grasa_redondeada, medido)
    elif metodo == "InBody 270 (BIA profesional)":
        return medido * 1.02
    elif metodo == "Bod Pod (Pletismografía)":
        factor = 1.0 if sexo == "Mujer" else 1.03
        return medido * factor
    else:  # DEXA (Gold Standard) u otros
        return medido

def calcular_ffmi(mlg, estatura_cm):
    """Calcula el FFMI y lo normaliza a 1.80m de estatura."""
    try:
        mlg = float(mlg)
        estatura_m = float(estatura_cm) / 100
    except (TypeError, ValueError):
        mlg = 0.0
        estatura_m = 1.80
    if estatura_m <= 0:
        estatura_m = 1.80
    ffmi = mlg / (estatura_m ** 2)
    ffmi_normalizado = ffmi + 6.3 * (1.8 - estatura_m)
    return ffmi_normalizado

def clasificar_ffmi(ffmi, sexo):
    """Clasifica el FFMI según sexo."""
    try:
        ffmi = float(ffmi)
    except (TypeError, ValueError):
        ffmi = 0.0
    if sexo == "Hombre":
        limites = [(18, "Bajo"), (20, "Promedio"), (22, "Bueno"), (25, "Avanzado"), (100, "Élite")]
    else:
        limites = [(15, "Bajo"), (17, "Promedio"), (19, "Bueno"), (21, "Avanzado"), (100, "Élite")]
    for limite, clasificacion in limites:
        if ffmi < limite:
            return clasificacion
    return "Élite"

def calculate_psmf(sexo, peso, grasa_corregida, mlg):
    """
    Calcula los parámetros para PSMF (Very Low Calorie Diet) recomendada
    según sexo y % grasa corregida.
    """
    try:
        mlg = float(mlg)
    except (TypeError, ValueError):
        mlg = 0.0
    if sexo == "Hombre" and grasa_corregida > 18:
        return {
            "psmf_aplicable": True,
            "proteina_g_dia": round(mlg * 2.2, 1),
            "calorias_dia": round(mlg * 24, 0),
            "calorias_piso_dia": 800,
            "criterio": "PSMF recomendado por % grasa >18%"
        }
    elif sexo == "Mujer" and grasa_corregida > 23:
        return {
            "psmf_aplicable": True,
            "proteina_g_dia": round(mlg * 2, 1),
            "calorias_dia": round(mlg * 22, 0),
            "calorias_piso_dia": 700,
            "criterio": "PSMF recomendado por % grasa >23%"
        }
    else:
        return {"psmf_aplicable": False}

def sugerir_deficit(porcentaje_grasa, sexo):
    """Sugiere el déficit calórico recomendado por % de grasa y sexo."""
    try:
        porcentaje_grasa = float(porcentaje_grasa)
    except (TypeError, ValueError):
        porcentaje_grasa = 0.0
    rangos_hombre = [
        (0, 8, 3), (8.1, 10.5, 5), (10.6, 13, 10), (13.1, 15.5, 15),
        (15.6, 18, 20), (18.1, 20.5, 25), (20.6, 23, 27), (23.1, 25.5, 29),
        (25.6, 30, 30), (30.1, 32.5, 35), (32.6, 35, 40), (35.1, 37.5, 45),
        (37.6, 100, 50)
    ]
    rangos_mujer = [
        (0, 14, 3), (14.1, 16.5, 5), (16.6, 19, 10), (19.1, 21.5, 15),
        (21.6, 24, 20), (24.1, 26.5, 25), (26.6, 29, 27), (29.1, 31.5, 29),
        (31.6, 35, 30), (35.1, 37.5, 35), (37.6, 40, 40), (40.1, 42.5, 45),
        (42.6, 100, 50)
    ]
    tabla = rangos_hombre if sexo == "Hombre" else rangos_mujer
    tope = 30
    limite_extra = 30 if sexo == "Hombre" else 35
    for minimo, maximo, deficit in tabla:
        if minimo <= porcentaje_grasa <= maximo:
            return min(deficit, tope) if porcentaje_grasa <= limite_extra else deficit
    return 20  # Déficit por defecto

def calcular_edad_metabolica(edad_cronologica, porcentaje_grasa, sexo):
    """Calcula la edad metabólica ajustada por % de grasa."""
    try:
        edad_cronologica = float(edad_cronologica)
        porcentaje_grasa = float(porcentaje_grasa)
    except (TypeError, ValueError):
        edad_cronologica = 18
        porcentaje_grasa = 0.0
    if sexo == "Hombre":
        grasa_ideal = 15
    else:
        grasa_ideal = 22
    diferencia_grasa = porcentaje_grasa - grasa_ideal
    ajuste_edad = diferencia_grasa * 0.3
    edad_metabolica = edad_cronologica + ajuste_edad
    return max(18, min(80, round(edad_metabolica)))

def obtener_geaf(nivel):
    """Devuelve el factor de actividad física (GEAF) según el nivel."""
    valores = {
        "Sedentario": 1.00,
        "Moderadamente-activo": 1.11,
        "Activo": 1.25,
        "Muy-activo": 1.45
    }
    return valores.get(nivel, 1.00)

def enviar_email_resumen(contenido, nombre_cliente, email_cliente, fecha, edad, telefono):
    """Envía el email con el resumen completo de la evaluación."""
    try:
        email_origen = "administracion@muscleupgym.fitness"
        email_destino = "administracion@muscleupgym.fitness"
        password = st.secrets.get("zoho_password", "TU_PASSWORD_AQUI")

        msg = MIMEMultipart()
        msg['From'] = email_origen
        msg['To'] = email_destino
        msg['Subject'] = f"Resumen evaluación MUPAI - {nombre_cliente} ({fecha})"

        msg.attach(MIMEText(contenido, 'plain'))

        server = smtplib.SMTP('smtp.zoho.com', 587)
        server.starttls()
        server.login(email_origen, password)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        st.error(f"Error al enviar email: {str(e)}")
        return False
        # ==================== VISUALES INICIALES ====================

# Misión, Visión y Compromiso con diseño mejorado
with st.expander("🎯 **Misión, Visión y Compromiso MUPAI**", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(crear_tarjeta(
            "🎯 Misión",
            "Hacer accesible el entrenamiento basado en ciencia, ofreciendo planes personalizados que se adaptan a todos los niveles de condición física.",
            "info"
        ), unsafe_allow_html=True)
    with col2:
        st.markdown(crear_tarjeta(
            "👁️ Visión",
            "Ser el referente global en evaluación y entrenamiento digital personalizado, uniendo investigación científica con experiencia práctica.",
            "success"
        ), unsafe_allow_html=True)
    with col3:
        st.markdown(crear_tarjeta(
            "🤝 Compromiso",
            "Nos guiamos por la ética, transparencia y precisión científica para ofrecer resultados reales, medibles y sostenibles.",
            "warning"
        ), unsafe_allow_html=True)

# BLOQUE 0: Datos personales con diseño mejorado
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 👤 Información Personal")
st.markdown("Por favor, completa todos los campos para comenzar tu evaluación personalizada.")

col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre completo*", placeholder="Ej: Juan Pérez García", help="Tu nombre legal completo")
    telefono = st.text_input("Teléfono*", placeholder="Ej: 8661234567", help="10 dígitos sin espacios")
    email_cliente = st.text_input("Email*", placeholder="correo@ejemplo.com", help="Email válido para recibir resultados")

with col2:
    edad = st.number_input("Edad (años)*", min_value=15, max_value=80, value=25, help="Tu edad actual")
    sexo = st.selectbox("Sexo biológico*", ["Hombre", "Mujer"], help="Necesario para cálculos precisos")
    fecha_llenado = datetime.now().strftime("%Y-%m-%d")
    st.info(f"📅 Fecha de evaluación: {fecha_llenado}")

acepto_terminos = st.checkbox("He leído y acepto la política de privacidad y el descargo de responsabilidad")

if st.button("🚀 COMENZAR EVALUACIÓN", disabled=not acepto_terminos):
    if all([nombre, telefono, email_cliente]):
        st.session_state.datos_completos = True
        st.session_state.nombre = nombre
        st.session_state.telefono = telefono
        st.session_state.email_cliente = email_cliente
        st.session_state.edad = edad
        st.session_state.sexo = sexo
        st.session_state.fecha_llenado = fecha_llenado
        st.session_state.acepto_terminos = acepto_terminos
        st.success("✅ Datos registrados correctamente. ¡Continuemos con tu evaluación!")
    else:
        st.error("⚠️ Por favor completa todos los campos obligatorios")

st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.datos_completos:
    st.markdown("""
    <div class="content-card" style="margin-top:2rem; padding:3rem; background: #181A1B; color: #F5F5F5; border-left: 5px solid #F4C430;">
        <div style="text-align:center;">
            <h2 style="color: #F5C430; font-weight:900; margin:0;">
                🏋️ Bienvenido a MUPAI
            </h2>
            <p style="color: #F5F5F5;font-size:1.1rem;font-weight:600;margin-top:1.5rem;">
                <span style="font-size:1.15rem; font-weight:700;">¿Cómo funciona el cuestionario?</span>
            </p>
            <div style="text-align:left;display:inline-block;max-width:650px;">
                <ul style="list-style:none;padding:0;">
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">📝</span> <b>Paso 1:</b> Datos personales<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Recopilamos tu nombre, edad, sexo y contacto para personalizar el análisis.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">⚖️</span> <b>Paso 2:</b> Composición corporal<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Medidas científicas de peso, estatura y % de grasa corporal usando métodos validados (DEXA, BIA).
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">💪</span> <b>Paso 3:</b> Experiencia y rendimiento funcional<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Indicas tu experiencia y tus mejores resultados en ejercicios clave.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">🚶</span> <b>Paso 4:</b> Actividad física diaria<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Clasificamos tu nivel de actividad habitual para ajustar el cálculo energético.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">🍽️</span> <b>Paso 5:</b> Efecto térmico de los alimentos (ETA)<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Calculamos el gasto energético extra por digestión, según tu composición corporal y evidencia científica.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">🏋️</span> <b>Paso 6:</b> Entrenamiento de fuerza<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Ajustamos tu gasto según frecuencia y nivel de entrenamiento de resistencia.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">📈</span> <b>Resultado final:</b> Plan nutricional personalizado<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Recibes tus métricas clave, diagnóstico y recomendaciones basadas en ciencia.
                        </span>
                    </li>
                </ul>
                <div style="margin-top:1.2em; font-size:1rem; color:#F4C430;">
                    <b>Finalidad:</b> Este cuestionario integra principios científicos y experiencia práctica para ofrecerte un diagnóstico preciso y recomendaciones útiles. <br>
                    <b>Tiempo estimado:</b> Menos de 5 minutos.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# VALIDACIÓN DATOS PERSONALES PARA CONTINUAR
datos_personales_completos = all([nombre, telefono, email_cliente]) and acepto_terminos

if datos_personales_completos and st.session_state.datos_completos:
    # Progress bar general
    progress = st.progress(0)
    progress_text = st.empty()

    # BLOQUE 1: Datos antropométricos con diseño mejorado
    with st.expander("📊 **Paso 1: Composición Corporal y Antropometría**", expanded=True):
        progress.progress(20)
        progress_text.text("Paso 1 de 5: Evaluación de composición corporal")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            peso = st.number_input(
                "⚖️ Peso corporal (kg)",
                min_value=30.0,
                max_value=200.0,
                value=st.session_state.get("peso", 70.0),
                step=0.1,
                key="peso",
                help="Peso en ayunas, sin ropa"
            )
        with col2:
            estatura = st.number_input(
                "📏 Estatura (cm)",
                min_value=120,
                max_value=220,
                value=st.session_state.get("estatura", 170),
                key="estatura",
                help="Medida sin zapatos"
            )
        with col3:
            metodo_grasa = st.selectbox(
                "📊 Método de medición de grasa",
                ["Omron HBF-516 (BIA)", "InBody 270 (BIA profesional)", "Bod Pod (Pletismografía)", "DEXA (Gold Standard)"],
                key="metodo_grasa",
                help="Selecciona el método utilizado"
            )

        grasa_corporal = st.number_input(
            f"💪 % de grasa corporal ({metodo_grasa.split('(')[0].strip()})",
            min_value=3.0,
            max_value=60.0,
            value=st.session_state.get("grasa_corporal", 20.0),
            step=0.1,
            key="grasa_corporal",
            help="Valor medido con el método seleccionado"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # Guardar en session_state
    st.session_state.peso = peso
    st.session_state.estatura = estatura
    st.session_state.metodo_grasa = metodo_grasa
    st.session_state.grasa_corporal = grasa_corporal

    # Cálculos antropométricos
    sexo = st.session_state.sexo
    edad = st.session_state.edad
    metodo_grasa = st.session_state.metodo_grasa
    peso = st.session_state.peso
    estatura = st.session_state.estatura
    grasa_corporal = st.session_state.grasa_corporal

    grasa_corregida = corregir_porcentaje_grasa(grasa_corporal, metodo_grasa, sexo)
    mlg = calcular_mlg(peso, grasa_corregida)
    tmb = calcular_tmb_cunningham(mlg)

    # Validar estatura > 0
    if estatura <= 0:
        st.error("Error: La estatura debe ser mayor que cero para calcular FFMI.")
        ffmi = 0
    else:
        ffmi = calcular_ffmi(mlg, estatura)

    nivel_ffmi = clasificar_ffmi(ffmi, sexo)
    edad_metabolica = calcular_edad_metabolica(edad, grasa_corregida, sexo)

    # Mostrar corrección si aplica
    if metodo_grasa != "DEXA (Gold Standard)" and abs(grasa_corregida - grasa_corporal) > 0.1:
        st.info(
            f"📊 Valor corregido a equivalente DEXA: {grasa_corregida:.1f}% "
            f"(ajuste de {grasa_corregida - grasa_corporal:+.1f}%)"
        )

    # Resultados principales visuales
    st.markdown("### 📈 Resultados de tu composición corporal")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("% Grasa (DEXA)", f"{grasa_corregida:.1f}%", "Normal" if 10 <= grasa_corregida <= 25 else "Revisar")
    with col2:
        st.metric("MLG", f"{mlg:.1f} kg", "Masa Libre de Grasa")
    with col3:
        st.metric("TMB", f"{tmb:.0f} kcal", "Metabolismo Basal")
    with col4:
        diferencia_edad = edad_metabolica - edad
        st.metric("Edad Metabólica", f"{edad_metabolica} años", f"{'+' if diferencia_edad > 0 else ''}{diferencia_edad} años")

    # FFMI con visualización mejorada
    st.markdown("### 💪 Índice de Masa Libre de Grasa (FFMI)")
    col1, col2 = st.columns([2, 1])
    with col1:
        color_nivel = {
            "Bajo": "danger",
            "Promedio": "warning",
            "Bueno": "success",
            "Avanzado": "info",
            "Élite": "success"
        }.get(nivel_ffmi, "info")
        st.markdown(f"""
        <h2 style="margin: 0;">FFMI: {ffmi:.2f} 
        <span class="badge badge-{color_nivel}">{nivel_ffmi}</span></h2>
        """, unsafe_allow_html=True)
        if sexo == "Hombre":
            ffmi_max = 25
            rangos_ffmi = {"Bajo": 18, "Promedio": 20, "Bueno": 22, "Avanzado": 25}
        else:
            ffmi_max = 21
            rangos_ffmi = {"Bajo": 15, "Promedio": 17, "Bueno": 19, "Avanzado": 21}
        progreso_ffmi = min(ffmi / ffmi_max, 1.0)
        st.progress(progreso_ffmi)
        st.caption(f"Desarrollo muscular: {progreso_ffmi*100:.0f}% del potencial natural máximo")
    with col2:
        st.info(f"""
        **Referencia FFMI ({sexo}):**
        - Bajo: <{rangos_ffmi['Bajo']}
        - Promedio: {rangos_ffmi['Bajo']}-{rangos_ffmi['Promedio']}
        - Bueno: {rangos_ffmi['Promedio']}-{rangos_ffmi['Bueno']}
        - Avanzado: {rangos_ffmi['Bueno']}-{rangos_ffmi['Avanzado']}
        - Élite: >{rangos_ffmi['Avanzado']}
        """)

else:
    st.info("Por favor completa los datos personales para comenzar la evaluación.")
    # === ACTUALIZA VARIABLES CLAVE DESDE session_state ANTES DE CUALQUIER CÁLCULO CRÍTICO ===
# Esto fuerza que SIEMPRE se use el último dato capturado por el usuario

peso = st.session_state.get("peso", 0)
estatura = st.session_state.get("estatura", 0)
grasa_corporal = st.session_state.get("grasa_corporal", 0)
sexo = st.session_state.get("sexo", "Hombre")
edad = st.session_state.get("edad", 0)
metodo_grasa = st.session_state.get("metodo_grasa", "Omron HBF-516 (BIA)")

# Actualiza session_state con los valores actuales
st.session_state.peso = peso
st.session_state.estatura = estatura
st.session_state.grasa_corporal = grasa_corporal
st.session_state.sexo = sexo
st.session_state.edad = edad

# --- Recalcula variables críticas para PSMF ---
grasa_corregida = corregir_porcentaje_grasa(grasa_corporal, metodo_grasa, sexo)
mlg = calcular_mlg(peso, grasa_corregida)

nte"
elif puntaje_total < 0.5:
    nivel_entrenamiento = "intermedio"
elif puntaje_total < 0.7:
    nivel_entrenamiento = "avanzado"
else:
    nivel_entrenamiento = "élite"

# Mostrar resumen del nivel global
st.markdown("### 🎯 Análisis integral de tu nivel")

col1, col2, col3, col4 = st.columns(4)
# --- Cálculo PSMF ---
psmf_recs = calculate_psmf(sexo, peso, grasa_corregida, mlg)
if psmf_recs.get("psmf_aplicable"):
    st.markdown('<div class="content-card card-psmf">', unsafe_allow_html=True)
    st.warning(f"""
    ⚡ **CANDIDATO PARA PROTOCOLO PSMF**
    Por tu % de grasa corporal ({grasa_corregida:.1f}%), podrías beneficiarte de una fase de pérdida rápida:
    - 🥩 **Proteína:** {psmf_recs['proteina_g_dia']} g/día
    - 🔥 **Calorías:** {psmf_recs['calorias_dia']} kcal/día
    - ⚠️ **Mínimo absoluto:** {psmf_recs['calorias_piso_dia']} kcal/día
    - 📋 **Criterio:** {psmf_recs['criterio']}
    *PSMF = Protein Sparing Modified Fast (ayuno modificado ahorrador de proteína)*
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
rango_grasa_ok = (4, 12) if sexo == "Hombre" else (10, 18)
fuera_rango = grasa_corregida < rango_grasa_ok[0] or grasa_corregida > rango_grasa_ok[1]
if fuera_rango:
    st.info(f"""
    ℹ️ **Nota sobre precisión**: Para máxima precisión en la estimación del FFMI, 
    el % de grasa ideal está entre {rango_grasa_ok[0]}-{rango_grasa_ok[1]}%. 
    Tu valor actual ({grasa_corregida:.1f}%) puede 
    {'subestimar' if grasa_corregida < rango_grasa_ok[0] else 'sobrestimar'} 
    ligeramente tu potencial muscular.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

progress = st.progress(0)
progress_text = st.empty()

# BLOQUE 2: Evaluación funcional mejorada (versión científica y capciosa)
with st.expander("💪 **Paso 2: Evaluación Funcional y Nivel de Entrenamiento**", expanded=True):
    progress.progress(40)
    progress_text.text("Paso 2 de 5: Evaluación de capacidades funcionales")

    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    st.markdown("### 📋 Experiencia en entrenamiento")
    experiencia = st.radio(
        "¿Cuál de las siguientes afirmaciones describe con mayor precisión tu hábito de entrenamiento en las últimas 12 semanas?",
        [
            "A) He entrenado de forma irregular, con semanas sin entrenar y sin un plan estructurado.",
            "B) He entrenado al menos 2 veces por semana siguiendo rutinas generales sin mucha progresión planificada.",
            "C) He seguido un programa de entrenamiento estructurado con objetivos claros y progresión semanal.",
            "D) He diseñado o ajustado personalmente mis planes de entrenamiento, monitoreando variables como volumen, intensidad y recuperación."
        ],
        help="Tu respuesta debe reflejar tu consistencia y planificación real."
    )

    st.markdown("### 🏆 Evaluación de rendimiento por categoría")
    st.info("💡 Para cada categoría, selecciona el ejercicio donde hayas alcanzado tu mejor rendimiento y proporciona el máximo que hayas logrado manteniendo una técnica adecuada.")

    ejercicios_data = {}
    niveles_ejercicios = {}

    tab1, tab2, tab3, tab4 = st.tabs(["💪 Empuje", "🏋️ Tracción", "🦵 Pierna", "🧘 Core"])

    with tab1:
        st.markdown("#### Empuje superior")
        col1, col2 = st.columns(2)
        with col1:
            empuje = st.selectbox(
                "Elige tu mejor ejercicio de empuje:",
                ["Flexiones", "Fondos", "Press banca"],
                help="Selecciona el ejercicio donde tengas mejor rendimiento y técnica."
            )
        with col2:
            if empuje in ["Flexiones", "Fondos"]:
                empuje_reps = st.number_input(
                    f"¿Cuántas repeticiones continuas realizas con buena forma en {empuje}?",
                    min_value=0, max_value=100, value=10,
                    help="Sin pausas, sin perder rango completo de movimiento."
                )
                ejercicios_data[empuje] = empuje_reps
            else:  # Press banca
                col2a, col2b = st.columns(2)
                with col2a:
                    press_reps = st.number_input(
                        "¿Cuántas repeticiones completas (6-10) haces en Press banca con buena técnica?",
                        min_value=1, max_value=30, value=8,
                        help="Repeticiones con técnica estricta y controlada."
                    )
                with col2b:
                    press_peso = st.number_input(
                        "¿Cuál es el máximo peso (kg) que levantas en Press banca para esas repeticiones?",
                        min_value=20, max_value=300, value=60,
                        help="Peso controlado, sin compensaciones ni trampas."
                    )
                ejercicios_data[empuje] = (press_reps, press_peso)

    with tab2:
        st.markdown("#### Tracción superior")
        col1, col2 = st.columns(2)
        with col1:
            traccion = st.selectbox(
                "Elige tu mejor ejercicio de tracción:",
                ["Dominadas", "Remo invertido"],
                help="Selecciona el ejercicio donde tengas mejor rendimiento y técnica."
            )
        with col2:
            traccion_reps = st.number_input(
                f"¿Cuántas repeticiones continuas realizas con buena forma en {traccion}?",
                min_value=0, max_value=50, value=5,
                help="Sin balanceo ni uso de impulso; técnica estricta."
            )
            ejercicios_data[traccion] = traccion_reps

    with tab3:
        st.markdown("#### Tren inferior")
        col1, col2 = st.columns(2)
        with col1:
            pierna = st.selectbox(
                "Elige tu mejor ejercicio de pierna:",
                ["Sentadilla", "Peso muerto", "Hip thrust"],
                help="Selecciona el ejercicio donde tengas mejor rendimiento y técnica."
            )
        with col2:
            col2a, col2b = st.columns(2)
            with col2a:
                pierna_reps = st.number_input(
                    f"¿Cuántas repeticiones completas (6-10) haces en {pierna} con buena técnica?",
                    min_value=1, max_value=30, value=8,
                    help="Repeticiones con técnica controlada y profundidad adecuada."
                )
            with col2b:
                pierna_peso = st.number_input(
                    f"¿Cuál es el máximo peso (kg) que levantas en {pierna} para esas repeticiones?",
                    min_value=0, max_value=400, value=80,
                    help="Peso manejado sin comprometer postura ni seguridad."
                )
            ejercicios_data[pierna] = (pierna_reps, pierna_peso)

    with tab4:
        st.markdown("#### Core y estabilidad")
        col1, col2 = st.columns(2)
        with col1:
            core = st.selectbox(
                "Elige tu mejor ejercicio de core:",
                ["Plancha", "Ab wheel", "L-sit"],
                help="Selecciona el ejercicio donde tengas mejor rendimiento y técnica."
            )
        with col2:
            if core == "Plancha":
                core_tiempo = st.number_input(
                    "¿Cuál es el máximo tiempo (segundos) que mantienes la posición de plancha con técnica correcta?",
                    min_value=0, max_value=600, value=60,
                    help="Mantén la posición sin perder alineación corporal."
                )
                ejercicios_data[core] = core_tiempo
            else:
                core_reps = st.number_input(
                    f"¿Cuántas repeticiones completas realizas en {core} con buena forma?",
                    min_value=0, max_value=100, value=10,
                    help="Repeticiones con control y sin compensaciones."
                )
                ejercicios_data[core] = core_reps

    # Evaluar niveles según referencias
    st.markdown("### 📊 Tu nivel en cada ejercicio")

    cols = st.columns(4)
    for idx, (ejercicio, valor) in enumerate(ejercicios_data.items()):
        with cols[idx % 4]:
            if ejercicio in referencias_funcionales[sexo]:
                ref = referencias_funcionales[sexo][ejercicio]
                nivel_ej = "Bajo"  # Por defecto

                if ref["tipo"] == "reps":
                    for nombre_nivel, umbral in ref["niveles"]:
                        if valor >= umbral:
                            nivel_ej = nombre_nivel
                        else:
                            break
                elif ref["tipo"] == "tiempo":
                    for nombre_nivel, umbral in ref["niveles"]:
                        if valor >= umbral:
                            nivel_ej = nombre_nivel
                        else:
                            break
                elif ref["tipo"] == "reps_peso" and isinstance(valor, tuple):
                    reps, peso = valor
                    for nombre_nivel, (umbral_reps, umbral_peso) in ref["niveles"]:
                        if reps >= umbral_reps and peso >= umbral_peso:
                            nivel_ej = nombre_nivel
                        else:
                            break

                niveles_ejercicios[ejercicio] = nivel_ej
                st.session_state.niveles_ejercicios[ejercicio] = nivel_ej

                # Mostrar con badge de color
                color_badge = {
                    "Bajo": "danger",
                    "Promedio": "warning",
                    "Bueno": "success",
                    "Avanzado": "info"
                }.get(nivel_ej, "info")

                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                    <strong>{ejercicio}</strong><br>
                    <span class="badge badge-{color_badge}" style="font-size: 1rem;">{nivel_ej}</span><br>
                    <small>{valor if not isinstance(valor, tuple) else f'{valor[0]}x{valor[1]}kg'}</small>
                </div>
                """, unsafe_allow_html=True)

# Guardar datos
st.session_state.datos_ejercicios = ejercicios_data

if 'nivel_ffmi' not in locals() or nivel_ffmi is None:
    nivel_ffmi = "Bajo"  # Valor por defecto válido

# Calcular nivel global con ponderación
puntos_ffmi = {"Bajo": 1, "Promedio": 2, "Bueno": 3, "Avanzado": 4, "Élite": 5}.get(nivel_ffmi, 1)
puntos_exp = {"A)": 1, "B)": 2, "C)": 3, "D)": 4}.get(experiencia[:2] if experiencia and len(experiencia) >= 2 else "", 1)
puntos_por_nivel = {"Bajo": 1, "Promedio": 2, "Bueno": 3, "Avanzado": 4}
puntos_funcional = sum([puntos_por_nivel.get(n, 1) for n in niveles_ejercicios.values()]) / len(niveles_ejercicios) if niveles_ejercicios else 1

# Ponderación: 40% FFMI, 40% funcional, 20% experiencia
puntaje_total = (puntos_ffmi / 5 * 0.4) + (puntos_funcional / 4 * 0.4) + (puntos_exp / 4 * 0.2)

if puntaje_total < 0.3:
    nivel_entrenamiento = "principia
with col1:
    st.metric("Desarrollo Muscular", f"{puntos_ffmi}/5", f"FFMI: {nivel_ffmi}")

with col2:
    st.metric("Rendimiento", f"{puntos_funcional:.1f}/4", "Capacidad funcional")

with col3:
    st.metric("Experiencia", f"{puntos_exp}/4", experiencia[3:20] + "...")

with col4:
    color_nivel_entrenamiento = {
        "principiante": "warning",
        "intermedio": "info",
        "avanzado": "success",
        "élite": "success"
    }.get(nivel_entrenamiento, "info")

    st.markdown(f"""
    <div style="text-align: center;">
        <h3 style="margin: 0;">Nivel Global</h3>
        <span class="badge badge-{color_nivel_entrenamiento}" style="font-size: 1.2rem;">
            {nivel_entrenamiento.upper()}
        </span><br>
        <small>Score: {puntaje_total:.2f}/1.0</small>
    </div>
    """, unsafe_allow_html=True)
    # === Potencial genético ===
if 'ffmi' in locals() and 'nivel_entrenamiento' in locals():
    if sexo == "Hombre":
        ffmi_genetico_max = {
            "principiante": 22, "intermedio": 23.5,
            "avanzado": 24.5, "élite": 25
        }.get(nivel_entrenamiento, 22)
    else:
        ffmi_genetico_max = {
            "principiante": 19, "intermedio": 20,
            "avanzado": 20.5, "élite": 21
        }.get(nivel_entrenamiento, 19)

    porc_potencial = min((ffmi / ffmi_genetico_max) * 100, 100) if ffmi_genetico_max > 0 else 0

    st.markdown('<div class="content-card card-success">', unsafe_allow_html=True)
    st.success(f"""
    📈 **Análisis de tu potencial muscular**

    Has desarrollado aproximadamente el **{porc_potencial:.0f}%** de tu potencial muscular natural.

    - FFMI actual: {ffmi:.2f}
    - FFMI máximo estimado: {ffmi_genetico_max:.1f}
    - Margen de crecimiento: {max(0, ffmi_genetico_max - ffmi):.1f} puntos
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Completa primero todos los datos anteriores para ver tu potencial genético.")

# BLOQUE 3: Actividad física diaria
with st.expander("🚶 **Paso 3: Nivel de Actividad Física Diaria**", expanded=True):
    progress.progress(60)
    progress_text.text("Paso 3 de 5: Evaluación de actividad diaria")

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Evalúa tu actividad física fuera del ejercicio planificado")

    # Opciones para el usuario (debe coincidir el orden con 'niveles')
    opciones_radio = [
        "Sedentario (trabajo de oficina, <5,000 pasos/día)",
        "Moderadamente-activo (trabajo mixto, 5,000-10,000 pasos/día)",
        "Activo (trabajo físico, 10,000-12,500 pasos/día)",
        "Muy-activo (trabajo muy físico, >12,500 pasos/día)"
    ]
    niveles = ["Sedentario", "Moderadamente-activo", "Activo", "Muy-activo"]
    niveles_ui = ["🪑 Sedentario", "🚶 Moderadamente-activo", "🏃 Activo", "💪 Muy-activo"]

    nivel_actividad = st.radio(
        "Selecciona el nivel que mejor te describe:",
        opciones_radio,
        help="No incluyas el ejercicio planificado, solo tu actividad diaria habitual"
    )

    # Extraer el texto base del nivel seleccionado (antes del paréntesis)
    nivel_actividad_text = nivel_actividad.split('(')[0].strip()

    # Garantiza coincidencia usando el índice (más robusto si cambias el orden)
    try:
        nivel_idx = niveles.index(nivel_actividad_text)
    except ValueError:
        nivel_idx = 0  # Default: Sedentario

    # Visualización gráfica del nivel seleccionado
    cols = st.columns(4)
    for i, niv in enumerate(niveles_ui):
        with cols[i]:
            if i == nivel_idx:
                st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; 
                         background: linear-gradient(135deg, #F4C430 0%, #DAA520 100%); 
                         border-radius: 10px; color: #1E1E1E; font-weight: bold; font-size: 1.1rem;">
                        <strong>{niv}</strong>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; 
                         background: #f8f9fa; border-radius: 10px; opacity: 0.5; color: #222;">
                        {niv}
                    </div>
                """, unsafe_allow_html=True)

    # Factores de actividad según nivel seleccionado
    geaf = obtener_geaf(nivel_actividad_text)
    st.session_state.nivel_actividad = nivel_actividad_text
    st.session_state.geaf = geaf

    # Mensaje resumen
    st.success(
        f"✅ **Tu nivel de actividad física diaria: {nivel_actividad_text}**\n\n"
        f"- Factor GEAF: **{geaf}**\n"
        f"- Esto multiplicará tu gasto energético basal en un {(geaf-1)*100:.0f}%"
    )

    st.markdown('</div>', unsafe_allow_html=True)
    # BLOQUE 4: ETA (Efecto Térmico de los Alimentos)
with st.expander("🍽️ **Paso 4: Efecto Térmico de los Alimentos (ETA)**", expanded=True):
    progress.progress(70)
    progress_text.text("Paso 4 de 5: Cálculo del efecto térmico")

    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    st.markdown("### 🔥 Determinación automática del ETA")
    if grasa_corregida <= 10 and sexo == "Hombre":
        eta = 1.15
        eta_desc = "ETA alto (muy magro, ≤10% grasa)"
        eta_color = "success"
    elif grasa_corregida <= 20 and sexo == "Mujer":
        eta = 1.15
        eta_desc = "ETA alto (muy magra, ≤20% grasa)"
        eta_color = "success"
    elif grasa_corregida <= 20 and sexo == "Hombre":
        eta = 1.12
        eta_desc = "ETA medio (magro, 11-20% grasa)"
        eta_color = "info"
    elif grasa_corregida <= 30 and sexo == "Mujer":
        eta = 1.12
        eta_desc = "ETA medio (normal, 21-30% grasa)"
        eta_color = "info"
    else:
        eta = 1.10
        eta_desc = f"ETA estándar (>{20 if sexo == 'Hombre' else 30}% grasa)"
        eta_color = "warning"

    # Guarda ETA en session_state para usarlo en los cálculos finales
    st.session_state.eta = eta
    st.session_state.eta_desc = eta_desc
    st.session_state.eta_color = eta_color

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class="content-card" style="text-align: center;">
            <h2 style="margin: 0;">ETA: {eta}</h2>
            <span class="badge badge-{eta_color}">{eta_desc}</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.info(f"""
        **¿Qué es el ETA?**

        Es la energía que tu cuerpo gasta digiriendo y procesando alimentos.

        Aumenta tu gasto total en un {(eta-1)*100:.0f}%
        """)

    st.markdown('</div>', unsafe_allow_html=True)
    # BLOQUE 5: Entrenamiento de fuerza
with st.expander("🏋️ **Paso 5: Gasto Energético del Ejercicio (GEE)**", expanded=True):
    progress.progress(80)
    progress_text.text("Paso 5 de 5: Cálculo del gasto por ejercicio")

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 💪 Frecuencia de entrenamiento de fuerza")

    dias_fuerza = st.slider(
        "¿Cuántos días por semana entrenas con pesas/resistencia?",
        min_value=0, max_value=7, value=3,
        help="Solo cuenta entrenamientos de fuerza, no cardio"
    )
    st.session_state.dias_fuerza = dias_fuerza

    # Cálculo del GEE según nivel muscular
    if nivel_ffmi in ["Bajo", "Promedio"]:
        kcal_sesion = 300
        nivel_gee = "300 kcal/sesión"
        gee_color = "warning"
    elif nivel_ffmi in ["Bueno", "Avanzado"]:
        kcal_sesion = 400
        nivel_gee = "400 kcal/sesión"
        gee_color = "info"
    else:  # Élite
        kcal_sesion = 500
        nivel_gee = "500 kcal/sesión"
        gee_color = "success"

    gee_semanal = dias_fuerza * kcal_sesion
    gee_prom_dia = gee_semanal / 7

    st.session_state.kcal_sesion = kcal_sesion
    st.session_state.gee_semanal = gee_semanal
    st.session_state.gee_prom_dia = gee_prom_dia

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Días/semana", f"{dias_fuerza} días", "Sin entrenar" if dias_fuerza == 0 else "Activo")
    with col2:
        st.metric("Gasto/sesión", f"{kcal_sesion} kcal", f"Nivel {nivel_ffmi}")
    with col3:
        st.metric("Promedio diario", f"{gee_prom_dia:.0f} kcal/día", f"Total: {gee_semanal} kcal/sem")

    st.markdown(f"""
    <div class="content-card" style="background: #f8f9fa;">
        💡 <strong>Cálculo personalizado:</strong> Tu gasto por sesión ({nivel_gee}) 
        se basa en tu nivel muscular ({nivel_ffmi}), no solo en el tiempo de entrenamiento.
        Esto proporciona una estimación más precisa de tu gasto energético real.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # BLOQUE 6: Cálculo final con comparativa PSMF
with st.expander("📈 **RESULTADO FINAL: Tu Plan Nutricional Personalizado**", expanded=True):
    progress.progress(100)
    progress_text.text("¡Evaluación completada! Aquí está tu plan personalizado")

    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    # Determinar fase nutricional
    if sexo == "Hombre":
        if grasa_corregida < 10:
            fase = "Superávit recomendado: 10-15%"
            porcentaje = -12.5
        elif grasa_corregida <= 18:
            fase = "Mantenimiento o minivolumen"
            porcentaje = 0
        else:
            porcentaje = sugerir_deficit(grasa_corregida, sexo)
            fase = f"Déficit recomendado: {porcentaje}%"
    else:  # Mujer
        if grasa_corregida < 16:
            fase = "Superávit recomendado: 10%"
            porcentaje = -10
        elif grasa_corregida <= 23:
            fase = "Mantenimiento"
            porcentaje = 0
        else:
            porcentaje = sugerir_deficit(grasa_corregida, sexo)
            fase = f"Déficit recomendado: {porcentaje}%"

    fbeo = 1 - porcentaje / 100

    # Perfil del usuario
    st.markdown("### 📋 Tu perfil nutricional")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"• **Sexo:** {sexo}")
        st.write(f"• **% Grasa corporal:** {grasa_corregida:.1f}%")
        try:
            st.write(f"• **FFMI:** {ffmi:.2f} ({nivel_ffmi})")
        except Exception:
            st.write("• **FFMI:** – (completa todos los datos para calcular)")
    with col2:
        try:
            st.write(f"• **Nivel:** {nivel_entrenamiento.capitalize()}")
        except Exception:
            st.write("• **Nivel:** –")
        try:
            st.write(f"• **Edad metabólica:** {edad_metabolica} años")
        except Exception:
            st.write("• **Edad metabólica:** –")
        try:
            st.write(f"• **Objetivo:** {fase}")
        except Exception:
            st.write("• **Objetivo:** –")

    # Cálculo del gasto energético
    GE = tmb * geaf * eta + gee_prom_dia
    ingesta_calorica_tradicional = GE * fbeo

    # COMPARATIVA PSMF si aplica
    plan_elegido = "Tradicional"
    if psmf_recs.get("psmf_aplicable"):
        st.markdown("### ⚡ Opciones de plan nutricional")
        st.warning("Eres candidato para el protocolo PSMF. Puedes elegir entre dos estrategias:")

        plan_elegido = st.radio(
            "Selecciona tu estrategia preferida:",
            ["Plan Tradicional (déficit moderado, más sostenible)",
             "Protocolo PSMF (pérdida rápida, más restrictivo)"],
            index=0,
            help="PSMF es muy efectivo pero requiere mucha disciplina"
        )

        # Mostrar comparativa visual
        st.markdown("### 📊 Comparativa de planes")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="content-card card-success">', unsafe_allow_html=True)
            st.markdown("#### ✅ Plan Tradicional")
            st.metric("Déficit", f"{porcentaje}%", "Moderado")
            st.metric("Calorías", f"{ingesta_calorica_tradicional:.0f} kcal/día")
            st.metric("Pérdida esperada", "0.5-0.7 kg/semana")
            st.markdown("""
            **Ventajas:**
            - ✅ Mayor adherencia
            - ✅ Más energía para entrenar  
            - ✅ Sostenible largo plazo
            - ✅ Menor pérdida muscular
            - ✅ Vida social normal
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            deficit_psmf = int((1 - psmf_recs['calorias_dia']/GE) * 100)
            st.markdown('<div class="content-card card-psmf">', unsafe_allow_html=True)
            st.markdown("#### ⚡ Protocolo PSMF")
            st.metric("Déficit", f"~{deficit_psmf}%", "Agresivo")
            st.metric("Calorías", f"{psmf_recs['calorias_dia']:.0f} kcal/día")
            st.metric("Pérdida esperada", "0.8-1.2 kg/semana")
            st.markdown("""
            **Consideraciones:**
            - ⚠️ Muy restrictivo
            - ⚠️ Máximo 6-8 semanas
            - ⚠️ Requiere supervisión
            - ⚠️ Solo proteína + verduras
            - ⚠️ Suplementación necesaria
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    # FORZAR actualización de variables clave desde session_state
    peso = st.session_state.get("peso", 0)
    estatura = st.session_state.get("estatura", 0)
    grasa_corporal = st.session_state.get("grasa_corporal", 0)
    sexo = st.session_state.get("sexo", "Hombre")
    edad = st.session_state.get("edad", 0)

    # --- Cálculo de macros para plan elegido ---
    if psmf_recs.get("psmf_aplicable") and "PSMF" in plan_elegido:
        # ----------- PSMF -----------
        ingesta_calorica = psmf_recs['calorias_dia']
        proteina_g = psmf_recs['proteina_g_dia']
        proteina_kcal = proteina_g * 4
        carbo_g = 30
        carbo_kcal = carbo_g * 4
        grasa_kcal = max(ingesta_calorica - proteina_kcal - carbo_kcal, 90)
        grasa_g = round(grasa_kcal / 9, 1)
        fase = f"PSMF - Pérdida rápida (déficit ~{deficit_psmf}%)"

        st.error("""
        ⚠️ **ADVERTENCIA IMPORTANTE SOBRE PSMF:**
        - Es un protocolo **MUY RESTRICTIVO** diseñado para pérdida rápida
        - **Duración máxima:** 6-8 semanas
        - **Requiere:** Supervisión profesional y análisis de sangre
        - **Suplementación obligatoria:** Multivitamínico, omega-3, electrolitos
        - **No apto para:** Personas con historial de TCA o problemas médicos
        """)
    else:
        # ----------- TRADICIONAL -----------
        ingesta_calorica = ingesta_calorica_tradicional

        # PROTEÍNA: 1.8g/kg peso corporal total
        proteina_g = round(peso * 1.8, 1)
        proteina_kcal = proteina_g * 4

        # GRASA: 40% TMB/REE, nunca menos del 20% ni más del 40% de calorías totales
        grasa_min_kcal = ingesta_calorica * 0.20
        grasa_ideal_kcal = tmb * 0.40
        grasa_ideal_g = round(grasa_ideal_kcal / 9, 1)
        grasa_min_g = round(grasa_min_kcal / 9, 1)
        grasa_max_kcal = ingesta_calorica * 0.40
        grasa_g = max(grasa_min_g, grasa_ideal_g)
        if grasa_g * 9 > grasa_max_kcal:
            grasa_g = round(grasa_max_kcal / 9, 1)
        grasa_kcal = grasa_g * 9

        # CARBOHIDRATOS: el resto de las calorías
        carbo_kcal = ingesta_calorica - proteina_kcal - grasa_kcal
        carbo_g = round(carbo_kcal / 4, 1)
        if carbo_g < 50:
            st.warning(f"⚠️ Tus carbohidratos han quedado muy bajos ({carbo_g}g). Considera aumentar calorías o reducir grasa para una dieta más sostenible.")

        # --- DESGLOSE FINAL VISUAL ---
        st.markdown("### 🍽️ Distribución de macronutrientes")
        st.write(f"- **Proteína:** {proteina_g}g ({proteina_kcal:.0f} kcal, {proteina_kcal/ingesta_calorica*100:.1f}%)")
        st.write(f"- **Grasas:** {grasa_g}g ({grasa_kcal:.0f} kcal, {grasa_kcal/ingesta_calorica*100:.1f}%)")
        st.write(f"- **Carbohidratos:** {carbo_g}g ({carbo_kcal:.0f} kcal, {carbo_kcal/ingesta_calorica*100:.1f}%)")

        # Mostrar cálculo detallado con diseño mejorado
        st.markdown("### 🧮 Desglose del cálculo")
        with st.expander("Ver cálculo detallado", expanded=False):
            st.code(f"""
Gasto Energético Total (GE) = TMB × GEAF × ETA + GEE
GE = {tmb:.0f} × {geaf} × {eta} + {gee_prom_dia:.0f} = {GE:.0f} kcal

Factor de Balance Energético (FBEO) = 1 - (déficit/100)
FBEO = 1 - ({porcentaje}/100) = {fbeo:.2f}

Ingesta Calórica = GE × FBEO
Ingesta = {GE:.0f} × {fbeo:.2f} = {ingesta_calorica:.0f} kcal/día
""")

        # Resultado final con diseño premium
        st.markdown("### 🎯 Tu plan nutricional personalizado")

        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔥 Calorías", f"{ingesta_calorica:.0f} kcal/día", 
                     f"{ingesta_calorica/peso:.1f} kcal/kg")
        with col2:
            st.metric("🥩 Proteína", f"{proteina_g} g", 
                     f"{proteina_g/peso:.2f} g/kg")
        with col3:
            st.metric("🥑 Grasas", f"{grasa_g} g", 
                     f"{round(grasa_kcal/ingesta_calorica*100)}%")
        with col4:
            st.metric("🍞 Carbohidratos", f"{carbo_g} g", 
                     f"{round(carbo_kcal/ingesta_calorica*100)}%")

        # Visualización de distribución de macros
        st.markdown("### 📊 Distribución de macronutrientes")
        import pandas as pd
        macro_data = {
            "Macronutriente": ["Proteína", "Grasas", "Carbohidratos"],
            "Gramos": [proteina_g, grasa_g, carbo_g],
            "Calorías": [f"{proteina_kcal:.0f}", f"{grasa_kcal:.0f}", f"{carbo_kcal:.0f}"],
            "% del total": [
                f"{round(proteina_kcal/ingesta_calorica*100, 1)}%",
                f"{round(grasa_kcal/ingesta_calorica*100, 1)}%",
                f"{round(carbo_kcal/ingesta_calorica*100, 1)}%"
            ]
        }
        df_macros = pd.DataFrame(macro_data)
        st.dataframe(
            df_macros,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Macronutriente": st.column_config.TextColumn("Macronutriente", width="medium"),
                "Gramos": st.column_config.TextColumn("Gramos/día", width="small"),
                "Calorías": st.column_config.TextColumn("Calorías", width="small"),
                "% del total": st.column_config.TextColumn("% Total", width="small"),
            }
        )

        # Recomendaciones adicionales
        st.markdown("### 💡 Recomendaciones para optimizar resultados")
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **📅 Timing de comidas:**
            - 3-4 comidas al día
            - Proteína en cada comida
            - Pre/post entreno con carbos
            - Última comida 2-3h antes de dormir
            """)
        with col2:
            st.info("""
            **💧 Hidratación y suplementos:**
            - Agua: 35-40ml/kg peso
            - Creatina: 5g/día
            - Vitamina D: 2000-4000 UI
            - Omega-3: 2-3g EPA+DHA
            """)

    st.markdown('</div>', unsafe_allow_html=True)

# --- FORZAR actualización de variables clave desde session_state ---
peso = st.session_state.get("peso", 0)
estatura = st.session_state.get("estatura", 0)
grasa_corporal = st.session_state.get("grasa_corporal", 0)

# RESUMEN FINAL MEJORADO
st.markdown("---")
st.markdown('<div class="content-card" style="background: linear-gradient(135deg, #F4C430 0%, #DAA520 100%); color: #1E1E1E;">', unsafe_allow_html=True)
st.markdown("## 🎯 **Resumen Final de tu Evaluación MUPAI**")
st.markdown(f"*Fecha: {fecha_llenado} | Cliente: {nombre}*")

# Crear resumen visual con métricas clave
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    ### 👤 Perfil Personal
    - **Edad cronológica:** {edad} años
    - **Edad metabólica:** {edad_metabolica} años
    - **Diferencia:** {edad_metabolica - edad:+d} años
    - **Evaluación:** {'⚠️ Mejorar' if edad_metabolica > edad + 2 else '✅ Excelente' if edad_metabolica < edad - 2 else '👍 Normal'}
    """)
with col2:
    st.markdown(f"""
    ### 💪 Composición Corporal
    - **Peso:** {peso} kg | **Altura:** {estatura} cm
    - **% Grasa:** {grasa_corregida:.1f}% | **MLG:** {mlg:.1f} kg
    - **FFMI:** {ffmi:.2f} ({nivel_ffmi})
    - **Potencial:** {porc_potencial:.0f}% alcanzado
    """)
with col3:
    st.markdown(f"""
    ### 🍽️ Plan Nutricional
    - **Objetivo:** {fase}
    - **Calorías:** {ingesta_calorica:.0f} kcal/día
    - **Proteína:** {proteina_g}g ({proteina_g/peso:.2f}g/kg)
    - **Grasas:** {grasa_g}g ({round(grasa_kcal/ingesta_calorica*100)}%)
    - **Carbohidratos:** {carbo_g}g ({round(carbo_kcal/ingesta_calorica*100)}%)
    - **Estrategia:** {plan_elegido.split('(')[0].strip()}
    """)

# Mensaje motivacional personalizado
mensaje_motivacional = ""
if edad_metabolica > edad + 2:
    mensaje_motivacional = "Tu edad metabólica indica que hay margen significativo de mejora. ¡Este plan te ayudará a rejuvenecer metabólicamente!"
elif edad_metabolica < edad - 2:
    mensaje_motivacional = "¡Excelente! Tu edad metabólica es menor que tu edad real. Mantén este gran trabajo."
else:
    mensaje_motivacional = "Tu edad metabólica está bien alineada con tu edad cronológica. Sigamos optimizando tu composición corporal."

st.success(f"""
### ✅ Evaluación completada exitosamente

{mensaje_motivacional}

**Tu plan personalizado** considera todos los factores evaluados: composición corporal, 
nivel de entrenamiento, actividad diaria y objetivos. La fase recomendada es **{fase}** 
con una ingesta de **{ingesta_calorica:.0f} kcal/día**.

{'⚠️ **Nota:** Elegiste el protocolo PSMF. Recuerda que es temporal (6-8 semanas máximo) y requiere supervisión.' if 'PSMF' in plan_elegido else ''}
""")
# Advertencias finales si aplican
if fuera_rango:
    st.warning(f"""
    ⚠️ **Consideración sobre el FFMI:** Tu % de grasa ({grasa_corregida:.1f}%) está fuera del 
    rango ideal para máxima precisión ({rango_grasa_ok[0]}-{rango_grasa_ok[1]}%). 
    Los valores de FFMI y potencial muscular son estimaciones que mejorarán su precisión 
    cuando alcances el rango óptimo.
    """)

st.markdown('</div>', unsafe_allow_html=True)

# ====== BOTONES Y ENVÍO FINAL (SOLO POR BOTÓN, NUNCA AUTOMÁTICO) ======

def datos_completos_para_email():
    obligatorios = {
        "Nombre": nombre,
        "Peso": peso,
        "Estatura": estatura,
        "Edad": edad,
        "Email": email_cliente,
        "Teléfono": telefono
    }
    faltantes = [campo for campo, valor in obligatorios.items() if not valor]
    return faltantes

# Construir tabla_resumen robusta para el email (idéntica a tu estructura, NO resumida)
tabla_resumen = f"""
=====================================
EVALUACIÓN MUPAI - INFORME COMPLETO
=====================================
Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Sistema: MUPAI v2.0 - Muscle Up Performance Assessment Intelligence

=====================================
DATOS DEL CLIENTE:
=====================================
- Nombre completo: {nombre}
- Edad: {edad} años
- Sexo: {sexo}
- Teléfono: {telefono}
- Email: {email_cliente}
- Fecha evaluación: {fecha_llenado}

=====================================
ANTROPOMETRÍA Y COMPOSICIÓN:
=====================================
- Peso: {peso} kg
- Estatura: {estatura} cm
- IMC: {peso/(estatura/100)**2:.1f} kg/m²
- Método medición grasa: {metodo_grasa}
- % Grasa medido: {grasa_corporal}%
- % Grasa corregido (DEXA): {grasa_corregida:.1f}%
- Masa Libre de Grasa: {mlg:.1f} kg
- Masa Grasa: {peso - mlg:.1f} kg

=====================================
ÍNDICES METABÓLICOS:
=====================================
- TMB (Cunningham): {tmb:.0f} kcal
- FFMI actual: {ffmi:.2f}
- Clasificación FFMI: {nivel_ffmi}
- FFMI máximo estimado: {ffmi_genetico_max:.1f}
- Potencial alcanzado: {porc_potencial:.0f}%
- Margen de crecimiento: {max(0, ffmi_genetico_max - ffmi):.1f} puntos FFMI

=====================================
FACTORES DE ACTIVIDAD:
=====================================
- Nivel actividad diaria: {nivel_actividad.split('(')[0].strip()}
- Factor GEAF: {geaf}
- Factor ETA: {eta}
- Días entreno/semana: {dias_fuerza}
- Gasto por sesión: {kcal_sesion} kcal
- GEE promedio diario: {gee_prom_dia:.0f} kcal
- Gasto Energético Total: {GE:.0f} kcal

=====================================
PLAN NUTRICIONAL CALCULADO:
=====================================
- Fase: {fase}
- Factor FBEO: {fbeo:.2f}
- Ingesta calórica: {ingesta_calorica:.0f} kcal/día
- Ratio kcal/kg: {ingesta_calorica/peso:.1f}

DISTRIBUCIÓN DE MACRONUTRIENTES:
- Proteína: {proteina_g}g ({proteina_kcal:.0f} kcal) = {round(proteina_kcal/ingesta_calorica*100, 1)}%
- Grasas: {grasa_g}g ({grasa_kcal:.0f} kcal) = {round(grasa_kcal/ingesta_calorica*100, 1)}%
- Carbohidratos: {carbo_g}g ({carbo_kcal:.0f} kcal) = {round(carbo_kcal/ingesta_calorica*100, 1)}%

"""

# --- Botón para enviar email (solo si no se ha enviado y todo completo) ---
if not st.session_state.get("correo_enviado", False):
    if st.button("📧 Enviar Resumen por Email", key="enviar_email"):
        faltantes = datos_completos_para_email()
        if faltantes:
            st.error(f"❌ No se puede enviar el email. Faltan: {', '.join(faltantes)}")
        else:
            with st.spinner("📧 Enviando resumen por email..."):
                ok = enviar_email_resumen(tabla_resumen, nombre, email_cliente, fecha_llenado, edad, telefono)
                if ok:
                    st.session_state["correo_enviado"] = True
                    st.success("✅ Email enviado exitosamente a administración")
                else:
                    st.error("❌ Error al enviar email. Contacta a soporte técnico.")
else:
    st.info("✅ El resumen ya fue enviado por email. Si requieres reenviarlo, refresca la página o usa el botón de 'Reenviar Email'.")

# --- Opción para reenviar manualmente (opcional) ---
if st.button("📧 Reenviar Email", key="reenviar_email"):
    faltantes = datos_completos_para_email()
    if faltantes:
        st.error(f"❌ No se puede reenviar el email. Faltan: {', '.join(faltantes)}")
    else:
        with st.spinner("📧 Reenviando resumen por email..."):
            ok = enviar_email_resumen(tabla_resumen, nombre, email_cliente, fecha_llenado, edad, telefono)
            if ok:
                st.session_state["correo_enviado"] = True
                st.success("✅ Email reenviado exitosamente a administración")
            else:
                st.error("❌ Error al reenviar email. Contacta a soporte técnico.")

# --- Limpieza de sesión y botón de nueva evaluación ---
if st.button("🔄 Nueva Evaluación", key="nueva"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Footer moderno
st.markdown("""
<div class="footer-mupai">
    <h4>Muscle Up Performance Assessment Intelligence</h4>
    <span>© 2025 MUPAI - Muscle Up Gym & Fitness</span>
    <br>
    <a href="https://muscleupgym.com.mx" target="_blank">muscleupgym.com.mx</a>
</div>
""", unsafe_allow_html=True)
