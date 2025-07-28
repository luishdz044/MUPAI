import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import re

# ==================== FUNCIONES DE VALIDACIÓN ESTRICTA ====================
def validate_name(name):
    """
    Valida que el nombre tenga al menos dos palabras.
    Retorna (es_válido, mensaje_error)
    """
    if not name or not name.strip():
        return False, "El nombre es obligatorio"
    
    # Limpiar espacios extra y dividir en palabras
    words = name.strip().split()
    
    if len(words) < 2:
        return False, "El nombre debe contener al menos dos palabras (nombre y apellido)"
    
    # Verificar que cada palabra tenga al menos 2 caracteres y solo contenga letras y espacios
    for word in words:
        if len(word) < 2:
            return False, "Cada palabra del nombre debe tener al menos 2 caracteres"
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$', word):
            return False, "El nombre solo puede contener letras y espacios"
    
    return True, ""

def validate_phone(phone):
    """
    Valida que el teléfono tenga exactamente 10 dígitos.
    Retorna (es_válido, mensaje_error)
    """
    if not phone or not phone.strip():
        return False, "El teléfono es obligatorio"
    
    # Limpiar espacios y caracteres especiales
    clean_phone = re.sub(r'[^0-9]', '', phone.strip())
    
    if len(clean_phone) != 10:
        return False, "El teléfono debe tener exactamente 10 dígitos"
    
    # Verificar que todos sean dígitos
    if not clean_phone.isdigit():
        return False, "El teléfono solo puede contener números"
    
    return True, ""

def validate_email(email):
    """
    Valida que el email tenga formato estándar.
    Retorna (es_válido, mensaje_error)
    """
    if not email or not email.strip():
        return False, "El email es obligatorio"
    
    # Patrón regex para email estándar
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email.strip()):
        return False, "El email debe tener un formato válido (ejemplo: usuario@dominio.com)"
    
    return True, ""

# ==================== CONFIGURACIÓN DE PÁGINA Y CSS MEJORADO ====================
st.set_page_config(
    page_title="MUPAI - Cuestionario de Selección Alimentaria Personalizada",
    page_icon="🍽️",
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
/* Special styling for selectboxes */
.stSelectbox[data-testid="stSelectbox"] > div > div > select {
    background: #F8F9FA!important;
    color: #1E1E1E!important;
    border: 2px solid #DAA520!important;
    font-weight: bold!important;
}
.stSelectbox[data-testid="stSelectbox"] option {
    background: #FFFFFF!important;
    color: #1E1E1E!important;
    font-weight: bold!important;
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

# Header principal visual con logos
import base64

# Cargar y codificar los logos desde la raíz del repo
try:
    with open('LOGO MUPAI.png', 'rb') as f:
        logo_mupai_b64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    logo_mupai_b64 = ""

try:
    with open('LOGO MUP.png', 'rb') as f:
        logo_gym_b64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    logo_gym_b64 = ""

st.markdown(f"""
<style>
.header-container {{
    background: #000000;
    padding: 2rem 1rem;
    border-radius: 18px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: fadeIn 0.5s ease-out;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
}}

.logo-left, .logo-right {{
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    max-width: 150px;
}}

.logo-left img, .logo-right img {{
    max-height: 80px;
    max-width: 100%;
    height: auto;
    width: auto;
    object-fit: contain;
}}

.header-center {{
    flex: 1;
    text-align: center;
    padding: 0 2rem;
}}

.header-title {{
    color: #FFB300;
    font-size: 2.2rem;
    font-weight: 900;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    line-height: 1.2;
}}

.header-subtitle {{
    color: #FFFFFF;
    font-size: 1rem;
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
}}

@media (max-width: 768px) {{
    .header-container {{
        flex-direction: column;
        text-align: center;
    }}
    
    .logo-left, .logo-right {{
        margin-bottom: 1rem;
    }}
    
    .header-center {{
        padding: 0;
    }}
    
    .header-title {{
        font-size: 1.8rem;
    }}
}}
</style>

<div class="header-container">
    <div class="logo-left">
        <img src="data:image/png;base64,{logo_mupai_b64}" alt="LOGO MUPAI" />
    </div>
    <div class="header-center">
        <h1 class="header-title">MUPAI: CUESTIONARIO DE SELECCIÓN ALIMENTARIA PERSONALIZADA</h1>
        <p class="header-subtitle">Tu evaluación personalizada de preferencias alimentarias basada en ciencia</p>
    </div>
    <div class="logo-right">
        <img src="data:image/png;base64,{logo_gym_b64}" alt="LOGO MUSCLE UP GYM" />
    </div>
</div>
""", unsafe_allow_html=True)

# --- Inicialización de estado de sesión robusta (solo una vez)
defaults = {
    "datos_completos": False,
    "correo_enviado": False,
    "preferencias_alimentarias": {},
    "restricciones_dieteticas": {},
    "nombre": "",
    "telefono": "",
    "email_cliente": "",
    "edad": "",
    "sexo": "Hombre",
    "fecha_llenado": datetime.now().strftime("%Y-%m-%d"),
    "acepto_terminos": False,
    "authenticated": False  # Nueva variable para controlar el login
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==================== SISTEMA DE AUTENTICACIÓN ====================
ADMIN_PASSWORD = "MUPAI2025"  # Contraseña predefinida

# Si no está autenticado, mostrar login
if not st.session_state.authenticated:
    st.markdown("""
    <div class="content-card" style="max-width: 500px; margin: 2rem auto; text-align: center;">
        <h2 style="color: var(--mupai-yellow); margin-bottom: 1.5rem;">
            🔐 Acceso Exclusivo
        </h2>
        <p style="margin-bottom: 2rem; color: #CCCCCC;">
            Ingresa la contraseña para acceder al sistema de cuestionario de selección alimentaria personalizada MUPAI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container centrado para el formulario de login
    login_container = st.container()
    with login_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password_input = st.text_input(
                "Contraseña", 
                type="password", 
                placeholder="Ingresa la contraseña de acceso",
                key="password_input"
            )
            
            if st.button("🚀 Acceder al Sistema", use_container_width=True):
                if password_input == ADMIN_PASSWORD:
                    st.session_state.authenticated = True
                    st.success("✅ Acceso autorizado. Bienvenido al sistema MUPAI de selección alimentaria personalizada.")
                    st.rerun()
                else:
                    st.error("❌ Contraseña incorrecta. Acceso denegado.")
    
    # Mostrar información mientras no esté autenticado
    st.markdown("""
    <div class="content-card" style="margin-top: 3rem; text-align: center; background: #1A1A1A;">
        <h3 style="color: var(--mupai-yellow);">Sistema de Cuestionario de Selección Alimentaria Personalizada</h3>
        <p style="color: #CCCCCC;">
            MUPAI utiliza metodologías científicas avanzadas para evaluar preferencias alimentarias 
            específicas, tolerancias individuales y crear perfiles nutricionales adaptativos.
        </p>
        <p style="color: #999999; font-size: 0.9rem; margin-top: 1.5rem;">
            © 2025 MUPAI - Muscle up GYM 
            Digital Nutrition Science
            Personalized Food Selection Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()  # Detener la ejecución hasta que se autentique

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

def enviar_email_resumen(contenido, nombre_cliente, email_cliente, fecha, edad, telefono):
    """Envía el email con el resumen completo de la evaluación de patrones alimentarios."""
    try:
        email_origen = "administracion@muscleupgym.fitness"
        email_destino = "administracion@muscleupgym.fitness"
        password = st.secrets.get("zoho_password", "TU_PASSWORD_AQUI")

        msg = MIMEMultipart()
        msg['From'] = email_origen
        msg['To'] = email_destino
        msg['Subject'] = f"Cuestionario de Selección Alimentaria Personalizada MUPAI - {nombre_cliente} ({fecha})"

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
            "Hacer accesible la evaluación nutricional basada en ciencia, ofreciendo análisis de patrones alimentarios personalizados que se adaptan a todos los estilos de vida.",
            "info"
        ), unsafe_allow_html=True)
    with col2:
        st.markdown(crear_tarjeta(
            "👁️ Visión",
            "Ser el referente global en evaluación de patrones alimentarios digitales, uniendo investigación nutricional con experiencia práctica personalizada.",
            "success"
        ), unsafe_allow_html=True)
    with col3:
        st.markdown(crear_tarjeta(
            "🤝 Compromiso",
            "Nos guiamos por la ética, transparencia y precisión científica para ofrecer recomendaciones nutricionales reales, medibles y sostenibles.",
            "warning"
        ), unsafe_allow_html=True)

# BLOQUE 0: Datos personales con diseño mejorado
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 👤 Información Personal")
st.markdown("Por favor, completa todos los campos para comenzar tu evaluación de patrones alimentarios personalizada.")

col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre completo*", placeholder="Ej: Juan Pérez García", help="Tu nombre legal completo")
    telefono = st.text_input("Teléfono*", placeholder="Ej: 8661234567", help="10 dígitos sin espacios")
    email_cliente = st.text_input("Email*", placeholder="correo@ejemplo.com", help="Email válido para recibir resultados")

with col2:
    edad = st.number_input("Edad (años)*", min_value=15, max_value=80, value=25, help="Tu edad actual")
    sexo = st.selectbox("Sexo biológico*", ["Hombre", "Mujer"], help="Necesario para análisis nutricionales precisos")
    fecha_llenado = datetime.now().strftime("%Y-%m-%d")
    st.info(f"📅 Fecha de evaluación: {fecha_llenado}")

acepto_terminos = st.checkbox("He leído y acepto la política de privacidad y el descargo de responsabilidad")

if st.button("🚀 COMENZAR EVALUACIÓN", disabled=not acepto_terminos):
    # Validación estricta de cada campo
    name_valid, name_error = validate_name(nombre)
    phone_valid, phone_error = validate_phone(telefono)
    email_valid, email_error = validate_email(email_cliente)
    
    # Mostrar errores específicos para cada campo que falle
    validation_errors = []
    if not name_valid:
        validation_errors.append(f"**Nombre:** {name_error}")
    if not phone_valid:
        validation_errors.append(f"**Teléfono:** {phone_error}")
    if not email_valid:
        validation_errors.append(f"**Email:** {email_error}")
    
    # Solo proceder si todas las validaciones pasan
    if name_valid and phone_valid and email_valid:
        st.session_state.datos_completos = True
        st.session_state.nombre = nombre
        st.session_state.telefono = telefono
        st.session_state.email_cliente = email_cliente
        st.session_state.edad = edad
        st.session_state.sexo = sexo
        st.session_state.fecha_llenado = fecha_llenado
        st.session_state.acepto_terminos = acepto_terminos
        st.success("✅ Datos registrados correctamente. ¡Continuemos con tu evaluación de patrones alimentarios!")
    else:
        # Mostrar todos los errores de validación
        error_message = "⚠️ **Por favor corrige los siguientes errores:**\n\n" + "\n\n".join(validation_errors)
        st.error(error_message)

st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.datos_completos:
    st.markdown("""
    <div class="content-card" style="margin-top:2rem; padding:3rem; background: #181A1B; color: #F5F5F5; border-left: 5px solid #F4C430;">
        <div style="text-align:center;">
            <h2 style="color: #F5C430; font-weight:900; margin:0;">
                🍽️ Bienvenido a MUPAI Patrones Alimentarios
            </h2>
            <p style="color: #F5F5F5;font-size:1.1rem;font-weight:600;margin-top:1.5rem;">
                <span style="font-size:1.15rem; font-weight:700;">¿Cómo funciona la evaluación?</span>
            </p>
            <div style="text-align:left;display:inline-block;max-width:650px;">
                <ul style="list-style:none;padding:0;">
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">📝</span> <b>Paso 1:</b> Datos personales<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Recopilamos tu información básica para personalizar la evaluación nutricional.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">🥗</span> <b>Paso 2:</b> Preferencias alimentarias<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Identificamos tus gustos, aversiones y preferencias de sabores y texturas.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">🚫</span> <b>Paso 3:</b> Restricciones y alergias<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Evaluamos restricciones dietéticas, alergias e intolerancias alimentarias.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">⏰</span> <b>Paso 4:</b> Patrones de comida y horarios<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Analizamos frecuencia de comidas, horarios y hábitos de alimentación.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">👨‍🍳</span> <b>Paso 5:</b> Habilidades culinarias y preparación<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Evaluamos nivel de cocina, tiempo disponible y métodos de preparación preferidos.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">🏛️</span> <b>Paso 6:</b> Contexto cultural y social<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Consideramos tradiciones culturales, contexto social y situaciones especiales.
                        </span>
                    </li>
                    <li style="margin-bottom:1.1em;">
                        <span style="font-size:1.3rem;">📈</span> <b>Resultado final:</b> Plan alimentario personalizado<br>
                        <span style="color:#F5F5F5;font-size:1rem;">
                            Recibes recomendaciones nutricionales adaptadas a tus preferencias y necesidades.
                        </span>
                    </li>
                </ul>
                <div style="margin-top:1.2em; font-size:1rem; color:#F4C430;">
                    <b>Finalidad:</b> Esta evaluación integra principios de nutrición personalizada para ofrecerte recomendaciones alimentarias que se ajusten a tu estilo de vida. <br>
                    <b>Tiempo estimado:</b> Menos de 10 minutos.
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

    st.markdown("""
    <div class="content-card" style="text-align: center; background: linear-gradient(135deg, #F4C430 0%, #DAA520 100%); color: #1E1E1E; margin-bottom: 2rem;">
        <h2 style="margin: 0; color: #1E1E1E; font-weight: 900;">🧾 CUESTIONARIO DE SELECCIÓN ALIMENTARIA PERSONALIZADA</h2>
        <p style="margin: 0.5rem 0 0 0; color: #333; font-weight: 600;">
            Marca (✓) todos los alimentos y bebidas que consumes con facilidad o disfrutas. 
            Esto permitirá diseñar un plan de alimentación ajustado a tus gustos, tolerancias y necesidades personales.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # GRUPO 1: PROTEÍNA ANIMAL CON MÁS CONTENIDO GRASO
    with st.expander("🥩 **GRUPO 1: PROTEÍNA ANIMAL CON MÁS CONTENIDO GRASO**", expanded=True):
        progress.progress(10)
        progress_text.text("Grupo 1 de 10: Proteína animal con más contenido graso")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### (elige todas las que puedas consumir con facilidad)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🍳 Huevos y embutidos")
            grupo1_huevos_embutidos = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Huevo entero", "Chorizo", "Salchicha (Viena, alemana, parrillera)", 
                 "Longaniza", "Tocino", "Jamón serrano"],
                key="g1_huevos_embutidos"
            )
            
            st.markdown("#### 🥩 Carnes y cortes grasos")
            grupo1_carnes_grasas = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Costilla de res", "Costilla de cerdo", "Ribeye", "T-bone", "New York",
                 "Arrachera marinada", "Molida 80/20 (regular)", "Molida 85/15", "Cecina con grasa"],
                key="g1_carnes_grasas"
            )
            
            st.markdown("#### 🧀 Quesos altos en grasa")
            grupo1_quesos_altos = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Queso manchego", "Queso doble crema", "Queso oaxaca", 
                 "Queso gouda", "Queso crema", "Queso cheddar"],
                key="g1_quesos_altos"
            )
        
        with col2:
            st.markdown("#### 🥛 Lácteos enteros")
            grupo1_lacteos_enteros = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Leche entera", "Yogur entero azucarado", "Yogur tipo griego entero",
                 "Yogur de frutas azucarado", "Yogur bebible regular", "Crema",
                 "Queso para untar (tipo Philadelphia original)"],
                key="g1_lacteos_enteros"
            )
            
            st.markdown("#### 🐟 Pescados grasos")
            grupo1_pescados_grasos = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Atún en aceite", "Salmón", "Sardinas", "Macarela", "Trucha"],
                key="g1_pescados_grasos"
            )

        # Guardar en session state
        st.session_state.grupo1_huevos_embutidos = grupo1_huevos_embutidos
        st.session_state.grupo1_carnes_grasas = grupo1_carnes_grasas
        st.session_state.grupo1_quesos_altos = grupo1_quesos_altos
        st.session_state.grupo1_lacteos_enteros = grupo1_lacteos_enteros
        st.session_state.grupo1_pescados_grasos = grupo1_pescados_grasos
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 2: PROTEÍNA ANIMAL MAGRA
    with st.expander("🍗 **GRUPO 2: PROTEÍNA ANIMAL MAGRA**", expanded=True):
        progress.progress(20)
        progress_text.text("Grupo 2 de 10: Proteína animal magra")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### (elige todas las que te sean fáciles de consumir)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🍗 Carnes y cortes magros")
            grupo2_carnes_magras = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Pechuga de pollo sin piel", "Filete de res magro (aguayón, bola, sirloin sin grasa visible)",
                 "Lomo de cerdo", "Bistec de res sin grasa visible", "Cecina magra",
                 "Molida 90/10", "Molida 95/5", "Molida 97/3", "Carne para deshebrar sin grasa (falda limpia)"],
                key="g2_carnes_magras"
            )
            
            st.markdown("#### 🐟 Pescados blancos y bajos en grasa")
            grupo2_pescados_blancos = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Tilapia", "Basa", "Huachinango", "Merluza", "Robalo", "Atún en agua"],
                key="g2_pescados_blancos"
            )
            
            st.markdown("#### 🧀 Quesos bajos en grasa o magros")
            grupo2_quesos_magros = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Queso panela", "Queso cottage", "Queso ricotta light", "Queso oaxaca reducido en grasa",
                 "Queso mozzarella light", "Queso fresco bajo en grasa"],
                key="g2_quesos_magros"
            )
        
        with col2:
            st.markdown("#### 🥛 Lácteos light o reducidos")
            grupo2_lacteos_light = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Leche descremada", "Leche deslactosada light", "Leche de almendra sin azúcar",
                 "Leche de coco sin azúcar", "Leche de soya sin azúcar", "Yogur griego natural sin azúcar",
                 "Yogur griego light", "Yogur bebible bajo en grasa", "Yogur sin azúcar añadida",
                 "Yogur de frutas bajo en grasa y sin azúcar añadida", "Queso crema light"],
                key="g2_lacteos_light"
            )
            
            st.markdown("#### 🥚 Otros")
            grupo2_otros = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Clara de huevo", "Jamón de pechuga de pavo", "Jamón de pierna bajo en grasa",
                 "Salchicha de pechuga de pavo (light)"],
                key="g2_otros"
            )

        # Guardar en session state
        st.session_state.grupo2_carnes_magras = grupo2_carnes_magras
        st.session_state.grupo2_pescados_blancos = grupo2_pescados_blancos
        st.session_state.grupo2_quesos_magros = grupo2_quesos_magros
        st.session_state.grupo2_lacteos_light = grupo2_lacteos_light
        st.session_state.grupo2_otros = grupo2_otros
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 3: FUENTES DE GRASA SALUDABLE
    with st.expander("🥑 **GRUPO 3: FUENTES DE GRASA SALUDABLE**", expanded=True):
        progress.progress(30)
        progress_text.text("Grupo 3 de 10: Fuentes de grasa saludable")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### (elige todas las que puedas o suelas consumir)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🥑 Grasas naturales de alimentos")
            grupo3_grasas_naturales = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Aguacate", "Yema de huevo", "Aceitunas (negras, verdes)", 
                 "Coco rallado natural", "Coco fresco", "Leche de coco sin azúcar"],
                key="g3_grasas_naturales"
            )
            
            st.markdown("#### 🌰 Frutos secos y semillas")
            grupo3_frutos_secos = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Almendras", "Nueces", "Nuez de la India", "Pistaches", "Cacahuates naturales (sin sal)",
                 "Semillas de chía", "Semillas de linaza", "Semillas de girasol", "Semillas de calabaza (pepitas)"],
                key="g3_frutos_secos"
            )
        
        with col2:
            st.markdown("#### 🧈 Mantequillas y pastas vegetales")
            grupo3_mantequillas = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Mantequilla de maní natural", "Mantequilla de almendra", 
                 "Tahini (pasta de ajonjolí)", "Mantequilla de nuez de la India"],
                key="g3_mantequillas"
            )

        # Guardar en session state
        st.session_state.grupo3_grasas_naturales = grupo3_grasas_naturales
        st.session_state.grupo3_frutos_secos = grupo3_frutos_secos
        st.session_state.grupo3_mantequillas = grupo3_mantequillas
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 4: CARBOHIDRATOS COMPLEJOS Y CEREALES
    with st.expander("🍞 **GRUPO 4: CARBOHIDRATOS COMPLEJOS Y CEREALES**", expanded=True):
        progress.progress(40)
        progress_text.text("Grupo 4 de 10: Carbohidratos complejos y cereales")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### (elige todos los que consumas con facilidad)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌾 Cereales y granos integrales")
            grupo4_cereales = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Avena tradicional", "Avena instantánea sin azúcar", "Arroz integral", "Arroz blanco",
                 "Arroz jazmín", "Arroz basmati", "Trigo bulgur", "Cuscús", "Quinoa", "Amaranto",
                 "Trigo inflado natural", "Cereal de maíz sin azúcar", "Cereal integral bajo en azúcar"],
                key="g4_cereales"
            )
            
            st.markdown("#### 🌽 Tortillas y panes")
            grupo4_tortillas_panes = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Tortilla de maíz", "Tortilla de nopal", "Tortilla integral", "Tortilla de harina",
                 "Pan integral", "Pan multigrano", "Pan de centeno", "Pan de caja sin azúcar añadida",
                 "Pan pita integral", "Pan tipo Ezekiel (germinado)"],
                key="g4_tortillas_panes"
            )
        
        with col2:
            st.markdown("#### 🥔 Raíces, tubérculos y derivados")
            grupo4_tuberculos = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Papa cocida o al horno", "Camote cocido o al horno", "Yuca", "Plátano macho",
                 "Puré de papa", "Papas horneadas", "Papas en air fryer"],
                key="g4_tuberculos"
            )
            
            st.markdown("#### 🫘 Leguminosas")
            grupo4_leguminosas = st.multiselect(
                "Selecciona todos los que puedas consumir:",
                ["Frijoles negros", "Frijoles bayos", "Frijoles pintos", "Lentejas", "Garbanzos",
                 "Habas cocidas", "Soya texturizada", "Edamames (vainas de soya)", "Hummus (puré de garbanzo)"],
                key="g4_leguminosas"
            )

        # Guardar en session state
        st.session_state.grupo4_cereales = grupo4_cereales
        st.session_state.grupo4_tortillas_panes = grupo4_tortillas_panes
        st.session_state.grupo4_tuberculos = grupo4_tuberculos
        st.session_state.grupo4_leguminosas = grupo4_leguminosas
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 5: VEGETALES
    with st.expander("🥬 **GRUPO 5: VEGETALES**", expanded=True):
        progress.progress(50)
        progress_text.text("Grupo 5 de 10: Vegetales")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### (elige todos los que consumes o toleras fácilmente)")
        
        grupo5_vegetales = st.multiselect(
            "Selecciona todos los vegetales que puedas consumir:",
            ["Espinaca", "Acelga", "Kale", "Lechuga (romana, italiana, orejona, iceberg)",
             "Col morada", "Col verde", "Repollo", "Brócoli", "Coliflor", "Ejote", "Chayote",
             "Calabacita", "Nopal", "Betabel", "Zanahoria", "Jitomate saladet", "Jitomate bola",
             "Tomate verde", "Cebolla blanca", "Cebolla morada", "Pimiento morrón (rojo, verde, amarillo, naranja)",
             "Pepino", "Apio", "Rábano", "Ajo", "Berenjena", "Champiñones", "Guisantes (chícharos)",
             "Verdolaga", "Habas tiernas", "Germen de alfalfa", "Germen de soya", "Flor de calabaza"],
            key="g5_vegetales"
        )

        # Guardar en session state
        st.session_state.grupo5_vegetales = grupo5_vegetales
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 6: FRUTAS
    with st.expander("🍎 **GRUPO 6: FRUTAS**", expanded=True):
        progress.progress(60)
        progress_text.text("Grupo 6 de 10: Frutas")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### (elige todas las que disfrutes o toleres bien)")
        
        grupo6_frutas = st.multiselect(
            "Selecciona todas las frutas que puedas consumir:",
            ["Manzana (roja, verde, gala, fuji)", "Naranja", "Mandarina", "Mango (petacón, ataulfo)",
             "Papaya", "Sandía", "Melón", "Piña", "Plátano (tabasco, dominico, macho)", "Uvas",
             "Fresas", "Arándanos", "Zarzamoras", "Frambuesas", "Higo", "Kiwi", "Pera", "Durazno",
             "Ciruela", "Granada", "Cereza", "Chabacano", "Lima", "Limón", "Guayaba", "Tuna",
             "Níspero", "Mamey", "Pitahaya (dragon fruit)", "Tamarindo", "Coco (carne, rallado)",
             "Caqui (persimón)", "Maracuyá", "Manzana en puré sin azúcar", "Fruta en almíbar light"],
            key="g6_frutas"
        )

        # Guardar en session state
        st.session_state.grupo6_frutas = grupo6_frutas
        
        st.markdown('</div>', unsafe_allow_html=True)

    # APARTADO EXTRA: GRASA/ACEITE DE COCCIÓN FAVORITA
    with st.expander("🍳 **APARTADO EXTRA: GRASA/ACEITE DE COCCIÓN FAVORITA**", expanded=True):
        progress.progress(70)
        progress_text.text("Apartado Extra: Grasa/aceite de cocción favorita")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### (elige todas las opciones que suelas usar para cocinar, freír, hornear o saltear tus alimentos)")
        
        aceites_coccion = st.multiselect(
            "Selecciona todos los aceites o grasas que uses para cocinar:",
            ["🫒 Aceite de oliva extra virgen", "🥑 Aceite de aguacate", "🥥 Aceite de coco virgen",
             "🧈 Mantequilla con sal", "🧈 Mantequilla sin sal", "🧈 Mantequilla clarificada (ghee)",
             "🐷 Manteca de cerdo (casera o artesanal)",
             "🧴 Spray antiadherente sin calorías (aceite de oliva o aguacate)",
             "❌ Prefiero cocinar sin aceite o con agua"],
            key="aceites_coccion"
        )

        # Guardar en session state
        st.session_state.aceites_coccion = aceites_coccion
        
        st.markdown('</div>', unsafe_allow_html=True)

    # BEBIDAS SIN CALORÍAS
    with st.expander("🥤 **¿Qué bebidas sin calorías sueles consumir regularmente para hidratarte?**", expanded=True):
        progress.progress(75)
        progress_text.text("Bebidas sin calorías para hidratación")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### (Marca todas las que acostumbres)")
        
        bebidas_sin_calorias = st.multiselect(
            "Selecciona todas las bebidas sin calorías que consumas:",
            ["💧 Agua natural", "💦 Agua mineral",
             "⚡ Bebidas con electrolitos sin azúcar (Electrolit Zero, SueroX, LMNT, etc.)",
             "🍋 Agua infusionada con frutas naturales (limón, pepino, menta, etc.)",
             "🍵 Té de hierbas sin azúcar (manzanilla, menta, jengibre, etc.)",
             "🍃 Té verde o té negro sin azúcar", "☕ Café negro sin azúcar",
             "🥤 Refrescos sin calorías (Coca Cola Zero, Pepsi Light, etc.)"],
            key="bebidas_sin_calorias"
        )

        # Guardar en session state
        st.session_state.bebidas_sin_calorias = bebidas_sin_calorias
        
        st.markdown('</div>', unsafe_allow_html=True)

    # SECCIÓN FINAL: ALERGIAS, INTOLERANCIAS Y PREFERENCIAS
    with st.expander("🚨 **SECCIÓN FINAL: ALERGIAS, INTOLERANCIAS Y PREFERENCIAS**", expanded=True):
        progress.progress(85)
        progress_text.text("Sección Final: Alergias, intolerancias y preferencias")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        st.markdown("### ❗ 1. ¿Tienes alguna alergia alimentaria? (Marca todas las que apliquen)")
        alergias_alimentarias = st.multiselect(
            "Selecciona todas las alergias que tengas:",
            ["Lácteos", "Huevo", "Frutos secos", "Mariscos", "Pescado", "Gluten", "Soya", "Semillas"],
            key="alergias_alimentarias"
        )
        
        otra_alergia = st.text_input(
            "Otra alergia (especificar):",
            placeholder="Especifica si tienes otra alergia no listada...",
            key="otra_alergia"
        )
        
        st.markdown("### ⚠️ 2. ¿Tienes alguna intolerancia o malestar digestivo?")
        intolerancias = st.multiselect(
            "Selecciona todas las intolerancias que tengas:",
            ["Lácteos con lactosa", "Leguminosas", "FODMAPs", "Gluten", "Crucíferas", "Endulzantes artificiales"],
            key="intolerancias"
        )
        
        otra_intolerancia = st.text_input(
            "Otra intolerancia (especificar):",
            placeholder="Especifica si tienes otra intolerancia no listada...",
            key="otra_intolerancia"
        )
        
        st.markdown("### ➕ 3. ¿Hay algún alimento o bebida que desees incluir, aunque no aparezca en las listas anteriores?")
        alimentos_adicionales = st.text_area(
            "Escribe aquí los alimentos o bebidas adicionales:",
            placeholder="Especifica alimentos o bebidas que consumes y no aparecen en las listas...",
            key="alimentos_adicionales"
        )

        # Guardar en session state
        st.session_state.alergias_alimentarias = alergias_alimentarias
        st.session_state.otra_alergia = otra_alergia
        st.session_state.intolerancias = intolerancias
        st.session_state.otra_intolerancia = otra_intolerancia
        st.session_state.alimentos_adicionales = alimentos_adicionales
        
        st.markdown('</div>', unsafe_allow_html=True)

    # SECCIÓN DE ANTOJOS ALIMENTARIOS
    with st.expander("😋 **SECCIÓN DE ANTOJOS ALIMENTARIOS**", expanded=True):
        progress.progress(95)
        progress_text.text("Sección de Antojos Alimentarios")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Instrucciones: Marca los alimentos que frecuentemente se te antojan o deseas con intensidad, aunque no necesariamente los consumas con regularidad. Puedes marcar tantos como necesites.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🍫 Alimentos dulces / postres")
            antojos_dulces = st.multiselect(
                "Selecciona todos los alimentos dulces que se te antojen:",
                ["Chocolate con leche", "Chocolate amargo", "Pan dulce (conchas, donas, cuernitos)",
                 "Pastel (tres leches, chocolate, etc.)", "Galletas (Marías, Emperador, Chokis, etc.)",
                 "Helado / Nieve", "Flan / Gelatina", "Dulces tradicionales (cajeta, obleas, jamoncillo, glorias)",
                 "Cereal azucarado", "Leche condensada", "Churros"],
                key="antojos_dulces"
            )
            
            st.markdown("#### 🧂 Alimentos salados / snacks")
            antojos_salados = st.multiselect(
                "Selecciona todos los alimentos salados que se te antojen:",
                ["Papas fritas (Sabritas, Ruffles, etc.)", "Cacahuates enchilados",
                 "Frituras (Doritos, Cheetos, Takis, etc.)", "Totopos con salsa", "Galletas saladas",
                 "Cacahuates japoneses", "Chicharrón (de cerdo o harina)", "Nachos con queso",
                 "Queso derretido o gratinado"],
                key="antojos_salados"
            )
            
            st.markdown("#### 🌮 Comidas rápidas / callejeras")
            antojos_comida_rapida = st.multiselect(
                "Selecciona todas las comidas rápidas que se te antojen:",
                ["Tacos (pastor, asada, birria, etc.)", "Tortas (cubana, ahogada, etc.)",
                 "Hamburguesas", "Hot dogs", "Pizza", "Quesadillas fritas", "Tamales",
                 "Pambazos", "Sopes / gorditas", "Elotes / esquites", "Burritos",
                 "Enchiladas", "Empanadas"],
                key="antojos_comida_rapida"
            )
        
        with col2:
            st.markdown("#### 🍹 Bebidas y postres líquidos")
            antojos_bebidas = st.multiselect(
                "Selecciona todas las bebidas que se te antojen:",
                ["Refrescos regulares (Coca-Cola, Fanta, etc.)", "Jugos industrializados (Boing, Jumex, etc.)",
                 "Malteadas / Frappés", "Agua de sabor con azúcar (jamaica, horchata, tamarindo)",
                 "Café con azúcar y leche", "Champurrado / atole", "Licuado de plátano con azúcar",
                 "Bebidas alcohólicas (cerveza, tequila, vino, etc.)"],
                key="antojos_bebidas"
            )
            
            st.markdown("#### 🔥 Alimentos con condimentos estimulantes")
            antojos_condimentos = st.multiselect(
                "Selecciona todos los que se te antojen:",
                ["Chiles en escabeche", "Salsas picantes", "Salsa Valentina, Tajín o Chamoy",
                 "Pepinos con chile y limón", "Mangos verdes con chile", "Gomitas enchiladas",
                 "Fruta con Miguelito o chile en polvo"],
                key="antojos_condimentos"
            )
        
        st.markdown("#### ❓ Pregunta final:")
        otros_antojos = st.text_area(
            "¿Qué otros alimentos o preparaciones se te antojan mucho y no aparecen en esta lista?",
            placeholder="Escríbelos aquí...",
            key="otros_antojos"
        )

        # Guardar en session state
        st.session_state.antojos_dulces = antojos_dulces
        st.session_state.antojos_salados = antojos_salados
        st.session_state.antojos_comida_rapida = antojos_comida_rapida
        st.session_state.antojos_bebidas = antojos_bebidas
        st.session_state.antojos_condimentos = antojos_condimentos
        st.session_state.otros_antojos = otros_antojos
        
        st.markdown('</div>', unsafe_allow_html=True)

    # RESULTADO FINAL: Análisis de selección alimentaria personalizada
    with st.expander("📈 **RESULTADO FINAL: Tu Perfil de Selección Alimentaria Personalizada**", expanded=True):
        progress.progress(100)
        progress_text.text("Análisis completo: Generando tu perfil de selección alimentaria personalizada")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Tu Perfil de Selección Alimentaria Personalizada")
        
        # Crear resumen del perfil
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Perfil Personal")
            st.write(f"• **Nombre:** {nombre}")
            st.write(f"• **Edad:** {edad} años")
            st.write(f"• **Sexo:** {sexo}")
            
            st.markdown("#### 🥩 Proteínas Seleccionadas")
            total_proteinas_grasas = len(st.session_state.get('grupo1_huevos_embutidos', [])) + len(st.session_state.get('grupo1_carnes_grasas', [])) + len(st.session_state.get('grupo1_quesos_altos', [])) + len(st.session_state.get('grupo1_lacteos_enteros', [])) + len(st.session_state.get('grupo1_pescados_grasos', []))
            total_proteinas_magras = len(st.session_state.get('grupo2_carnes_magras', [])) + len(st.session_state.get('grupo2_pescados_blancos', [])) + len(st.session_state.get('grupo2_quesos_magros', [])) + len(st.session_state.get('grupo2_lacteos_light', [])) + len(st.session_state.get('grupo2_otros', []))
            
            st.write(f"• **Proteínas con grasa:** {total_proteinas_grasas} opciones")
            st.write(f"• **Proteínas magras:** {total_proteinas_magras} opciones")
            
            st.markdown("#### 🥑 Grasas y Carbohidratos")
            total_grasas = len(st.session_state.get('grupo3_grasas_naturales', [])) + len(st.session_state.get('grupo3_frutos_secos', [])) + len(st.session_state.get('grupo3_mantequillas', []))
            total_carbohidratos = len(st.session_state.get('grupo4_cereales', [])) + len(st.session_state.get('grupo4_tortillas_panes', [])) + len(st.session_state.get('grupo4_tuberculos', [])) + len(st.session_state.get('grupo4_leguminosas', []))
            
            st.write(f"• **Grasas saludables:** {total_grasas} opciones")
            st.write(f"• **Carbohidratos complejos:** {total_carbohidratos} opciones")
        
        with col2:
            st.markdown("#### 🥬 Vegetales y Frutas")
            total_vegetales = len(st.session_state.get('grupo5_vegetales', []))
            total_frutas = len(st.session_state.get('grupo6_frutas', []))
            
            st.write(f"• **Vegetales:** {total_vegetales} opciones")
            st.write(f"• **Frutas:** {total_frutas} opciones")
            
            st.markdown("#### 🍳 Preferencias Adicionales")
            total_aceites = len(st.session_state.get('aceites_coccion', []))
            total_bebidas = len(st.session_state.get('bebidas_sin_calorias', []))
            
            st.write(f"• **Aceites de cocción:** {total_aceites} opciones")
            st.write(f"• **Bebidas sin calorías:** {total_bebidas} opciones")
            
            st.markdown("#### 😋 Antojos Identificados")
            total_antojos = len(st.session_state.get('antojos_dulces', [])) + len(st.session_state.get('antojos_salados', [])) + len(st.session_state.get('antojos_comida_rapida', [])) + len(st.session_state.get('antojos_bebidas', [])) + len(st.session_state.get('antojos_condimentos', []))
            st.write(f"• **Total antojos:** {total_antojos} opciones")

        # Análisis de restricciones
        if st.session_state.get('alergias_alimentarias') or st.session_state.get('intolerancias'):
            st.markdown("#### ⚠️ Restricciones Importantes")
            if st.session_state.get('alergias_alimentarias'):
                st.warning(f"**Alergias:** {', '.join(st.session_state.get('alergias_alimentarias', []))}")
            if st.session_state.get('intolerancias'):
                st.warning(f"**Intolerancias:** {', '.join(st.session_state.get('intolerancias', []))}")
            if st.session_state.get('otra_alergia'):
                st.warning(f"**Otra alergia:** {st.session_state.get('otra_alergia')}")
            if st.session_state.get('otra_intolerancia'):
                st.warning(f"**Otra intolerancia:** {st.session_state.get('otra_intolerancia')}")

        # Recomendaciones personalizadas basadas en las selecciones
        st.markdown("### 💡 Análisis de tu Selección Alimentaria")
        
        # Calcular variedad total de alimentos seleccionados
        total_alimentos = total_proteinas_grasas + total_proteinas_magras + total_grasas + total_carbohidratos + total_vegetales + total_frutas
        
        col1, col2 = st.columns(2)
        with col1:
            if total_alimentos > 50:
                variedad_nivel = "ALTA"
                variedad_color = "success"
                recomendacion_variedad = "Excelente variedad alimentaria. Tienes una amplia gama de opciones para crear planes nutricionales diversos y balanceados."
            elif total_alimentos > 30:
                variedad_nivel = "MODERADA"
                variedad_color = "warning"
                recomendacion_variedad = "Buena variedad alimentaria. Puedes ampliar gradualmente tu selección para mayor flexibilidad nutricional."
            else:
                variedad_nivel = "BÁSICA"
                variedad_color = "danger"
                recomendacion_variedad = "Variedad limitada. Se recomienda explorar gradualmente nuevos alimentos para mejorar la diversidad nutricional."
            
            if variedad_color == "success":
                st.success(f"""
                **🌟 Variedad alimentaria: {variedad_nivel}**
                
                {recomendacion_variedad}
                
                **Total de alimentos seleccionados:** {total_alimentos}
                """)
            elif variedad_color == "warning":
                st.warning(f"""
                **⚡ Variedad alimentaria: {variedad_nivel}**
                
                {recomendacion_variedad}
                
                **Total de alimentos seleccionados:** {total_alimentos}
                """)
            else:
                st.error(f"""
                **⚠️ Variedad alimentaria: {variedad_nivel}**
                
                {recomendacion_variedad}
                
                **Total de alimentos seleccionados:** {total_alimentos}
                """)
        
        with col2:
            # Análisis de balance nutricional
            if total_proteinas_grasas + total_proteinas_magras > 10 and total_carbohidratos > 8 and total_vegetales > 10:
                balance_nivel = "BALANCEADO"
                balance_color = "success"
                recomendacion_balance = "Tu selección muestra un buen balance entre macronutrientes y micronutrientes."
            elif total_proteinas_grasas + total_proteinas_magras > 5 and total_carbohidratos > 5 and total_vegetales > 5:
                balance_nivel = "MODERADO"
                balance_color = "warning"
                recomendacion_balance = "Balance nutricional aceptable. Considera ampliar las categorías con menos selecciones."
            else:
                balance_nivel = "MEJORABLE"
                balance_color = "danger"
                recomendacion_balance = "Se recomienda incluir más opciones de diferentes grupos alimentarios para mejor balance."
            
            if balance_color == "success":
                st.success(f"""
                **⚖️ Balance nutricional: {balance_nivel}**
                
                {recomendacion_balance}
                """)
            elif balance_color == "warning":
                st.warning(f"""
                **⚖️ Balance nutricional: {balance_nivel}**
                
                {recomendacion_balance}
                """)
            else:
                st.error(f"""
                **⚖️ Balance nutricional: {balance_nivel}**
                
                {recomendacion_balance}
                """)

        st.markdown("### 🎯 Próximos Pasos Recomendados")
        
        st.success(f"""
        ### ✅ Cuestionario de Selección Alimentaria Personalizada completado exitosamente
        
        **Tu perfil alimentario personalizado está listo** con {total_alimentos} alimentos seleccionados 
        distribuidos en 6 grupos principales más aceites de cocción y bebidas sin calorías.
        
        **Esta información permite diseñar planes de alimentación específicos** que se ajusten 
        exactamente a tus gustos, tolerancias y preferencias personales.
        
        Se recomienda consulta con nutricionista especializado para desarrollar plan alimentario 
        personalizado basado en estas selecciones específicas.
        """)

        st.markdown('</div>', unsafe_allow_html=True)

# Construir resumen completo para email
def crear_resumen_email():
    resumen = f"""
=====================================
CUESTIONARIO DE SELECCIÓN ALIMENTARIA PERSONALIZADA - MUPAI
=====================================
Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Sistema: MUPAI v2.0 - Muscle Up Performance Assessment Intelligence

=====================================
DATOS DEL CLIENTE:
=====================================
- Nombre completo: {st.session_state.get('nombre', 'No especificado')}
- Edad: {st.session_state.get('edad', 'No especificado')} años
- Sexo: {st.session_state.get('sexo', 'No especificado')}
- Teléfono: {st.session_state.get('telefono', 'No especificado')}
- Email: {st.session_state.get('email_cliente', 'No especificado')}
- Fecha evaluación: {st.session_state.get('fecha_llenado', 'No especificado')}

=====================================
GRUPO 1: PROTEÍNA ANIMAL CON MÁS CONTENIDO GRASO
=====================================
🍳 Huevos y embutidos:
{', '.join(st.session_state.get('grupo1_huevos_embutidos', [])) if st.session_state.get('grupo1_huevos_embutidos') else 'Ninguno seleccionado'}

🥩 Carnes y cortes grasos:
{', '.join(st.session_state.get('grupo1_carnes_grasas', [])) if st.session_state.get('grupo1_carnes_grasas') else 'Ninguno seleccionado'}

🧀 Quesos altos en grasa:
{', '.join(st.session_state.get('grupo1_quesos_altos', [])) if st.session_state.get('grupo1_quesos_altos') else 'Ninguno seleccionado'}

🥛 Lácteos enteros:
{', '.join(st.session_state.get('grupo1_lacteos_enteros', [])) if st.session_state.get('grupo1_lacteos_enteros') else 'Ninguno seleccionado'}

🐟 Pescados grasos:
{', '.join(st.session_state.get('grupo1_pescados_grasos', [])) if st.session_state.get('grupo1_pescados_grasos') else 'Ninguno seleccionado'}

=====================================
GRUPO 2: PROTEÍNA ANIMAL MAGRA
=====================================
🍗 Carnes y cortes magros:
{', '.join(st.session_state.get('grupo2_carnes_magras', [])) if st.session_state.get('grupo2_carnes_magras') else 'Ninguno seleccionado'}

🐟 Pescados blancos y bajos en grasa:
{', '.join(st.session_state.get('grupo2_pescados_blancos', [])) if st.session_state.get('grupo2_pescados_blancos') else 'Ninguno seleccionado'}

🧀 Quesos bajos en grasa o magros:
{', '.join(st.session_state.get('grupo2_quesos_magros', [])) if st.session_state.get('grupo2_quesos_magros') else 'Ninguno seleccionado'}

🥛 Lácteos light o reducidos:
{', '.join(st.session_state.get('grupo2_lacteos_light', [])) if st.session_state.get('grupo2_lacteos_light') else 'Ninguno seleccionado'}

🥚 Otros:
{', '.join(st.session_state.get('grupo2_otros', [])) if st.session_state.get('grupo2_otros') else 'Ninguno seleccionado'}

=====================================
GRUPO 3: FUENTES DE GRASA SALUDABLE
=====================================
🥑 Grasas naturales de alimentos:
{', '.join(st.session_state.get('grupo3_grasas_naturales', [])) if st.session_state.get('grupo3_grasas_naturales') else 'Ninguno seleccionado'}

🌰 Frutos secos y semillas:
{', '.join(st.session_state.get('grupo3_frutos_secos', [])) if st.session_state.get('grupo3_frutos_secos') else 'Ninguno seleccionado'}

🧈 Mantequillas y pastas vegetales:
{', '.join(st.session_state.get('grupo3_mantequillas', [])) if st.session_state.get('grupo3_mantequillas') else 'Ninguno seleccionado'}

=====================================
GRUPO 4: CARBOHIDRATOS COMPLEJOS Y CEREALES
=====================================
🌾 Cereales y granos integrales:
{', '.join(st.session_state.get('grupo4_cereales', [])) if st.session_state.get('grupo4_cereales') else 'Ninguno seleccionado'}

🌽 Tortillas y panes:
{', '.join(st.session_state.get('grupo4_tortillas_panes', [])) if st.session_state.get('grupo4_tortillas_panes') else 'Ninguno seleccionado'}

🥔 Raíces, tubérculos y derivados:
{', '.join(st.session_state.get('grupo4_tuberculos', [])) if st.session_state.get('grupo4_tuberculos') else 'Ninguno seleccionado'}

🫘 Leguminosas:
{', '.join(st.session_state.get('grupo4_leguminosas', [])) if st.session_state.get('grupo4_leguminosas') else 'Ninguno seleccionado'}

=====================================
GRUPO 5: VEGETALES
=====================================
{', '.join(st.session_state.get('grupo5_vegetales', [])) if st.session_state.get('grupo5_vegetales') else 'Ninguno seleccionado'}

=====================================
GRUPO 6: FRUTAS
=====================================
{', '.join(st.session_state.get('grupo6_frutas', [])) if st.session_state.get('grupo6_frutas') else 'Ninguna seleccionada'}

=====================================
APARTADO EXTRA: GRASA/ACEITE DE COCCIÓN FAVORITA
=====================================
{', '.join(st.session_state.get('aceites_coccion', [])) if st.session_state.get('aceites_coccion') else 'Ninguno seleccionado'}

=====================================
BEBIDAS SIN CALORÍAS PARA HIDRATACIÓN
=====================================
{', '.join(st.session_state.get('bebidas_sin_calorias', [])) if st.session_state.get('bebidas_sin_calorias') else 'Ninguna seleccionada'}

=====================================
SECCIÓN FINAL: ALERGIAS, INTOLERANCIAS Y PREFERENCIAS
=====================================
❗ Alergias alimentarias:
{', '.join(st.session_state.get('alergias_alimentarias', [])) if st.session_state.get('alergias_alimentarias') else 'Ninguna'}
Otra alergia especificada: {st.session_state.get('otra_alergia', 'No especificado')}

⚠️ Intolerancias o malestar digestivo:
{', '.join(st.session_state.get('intolerancias', [])) if st.session_state.get('intolerancias') else 'Ninguna'}
Otra intolerancia especificada: {st.session_state.get('otra_intolerancia', 'No especificado')}

➕ Alimentos adicionales deseados:
{st.session_state.get('alimentos_adicionales', 'No especificado')}

=====================================
SECCIÓN DE ANTOJOS ALIMENTARIOS
=====================================
🍫 Alimentos dulces / postres:
{', '.join(st.session_state.get('antojos_dulces', [])) if st.session_state.get('antojos_dulces') else 'Ninguno seleccionado'}

🧂 Alimentos salados / snacks:
{', '.join(st.session_state.get('antojos_salados', [])) if st.session_state.get('antojos_salados') else 'Ninguno seleccionado'}

🌮 Comidas rápidas / callejeras:
{', '.join(st.session_state.get('antojos_comida_rapida', [])) if st.session_state.get('antojos_comida_rapida') else 'Ninguno seleccionado'}

🍹 Bebidas y postres líquidos:
{', '.join(st.session_state.get('antojos_bebidas', [])) if st.session_state.get('antojos_bebidas') else 'Ninguno seleccionado'}

🔥 Alimentos con condimentos estimulantes:
{', '.join(st.session_state.get('antojos_condimentos', [])) if st.session_state.get('antojos_condimentos') else 'Ninguno seleccionado'}

❓ Otros antojos especificados:
{st.session_state.get('otros_antojos', 'No especificado')}

=====================================
RESUMEN ESTADÍSTICO DE SELECCIONES:
=====================================
- Total Proteínas con grasa: {len(st.session_state.get('grupo1_huevos_embutidos', [])) + len(st.session_state.get('grupo1_carnes_grasas', [])) + len(st.session_state.get('grupo1_quesos_altos', [])) + len(st.session_state.get('grupo1_lacteos_enteros', [])) + len(st.session_state.get('grupo1_pescados_grasos', []))} opciones
- Total Proteínas magras: {len(st.session_state.get('grupo2_carnes_magras', [])) + len(st.session_state.get('grupo2_pescados_blancos', [])) + len(st.session_state.get('grupo2_quesos_magros', [])) + len(st.session_state.get('grupo2_lacteos_light', [])) + len(st.session_state.get('grupo2_otros', []))} opciones
- Total Grasas saludables: {len(st.session_state.get('grupo3_grasas_naturales', [])) + len(st.session_state.get('grupo3_frutos_secos', [])) + len(st.session_state.get('grupo3_mantequillas', []))} opciones
- Total Carbohidratos complejos: {len(st.session_state.get('grupo4_cereales', [])) + len(st.session_state.get('grupo4_tortillas_panes', [])) + len(st.session_state.get('grupo4_tuberculos', [])) + len(st.session_state.get('grupo4_leguminosas', []))} opciones
- Total Vegetales: {len(st.session_state.get('grupo5_vegetales', []))} opciones
- Total Frutas: {len(st.session_state.get('grupo6_frutas', []))} opciones
- Total Aceites de cocción: {len(st.session_state.get('aceites_coccion', []))} opciones
- Total Bebidas sin calorías: {len(st.session_state.get('bebidas_sin_calorias', []))} opciones
- Total Antojos identificados: {len(st.session_state.get('antojos_dulces', [])) + len(st.session_state.get('antojos_salados', [])) + len(st.session_state.get('antojos_comida_rapida', [])) + len(st.session_state.get('antojos_bebidas', [])) + len(st.session_state.get('antojos_condimentos', []))} opciones

TOTAL ALIMENTOS SELECCIONADOS: {len(st.session_state.get('grupo1_huevos_embutidos', [])) + len(st.session_state.get('grupo1_carnes_grasas', [])) + len(st.session_state.get('grupo1_quesos_altos', [])) + len(st.session_state.get('grupo1_lacteos_enteros', [])) + len(st.session_state.get('grupo1_pescados_grasos', [])) + len(st.session_state.get('grupo2_carnes_magras', [])) + len(st.session_state.get('grupo2_pescados_blancos', [])) + len(st.session_state.get('grupo2_quesos_magros', [])) + len(st.session_state.get('grupo2_lacteos_light', [])) + len(st.session_state.get('grupo2_otros', [])) + len(st.session_state.get('grupo3_grasas_naturales', [])) + len(st.session_state.get('grupo3_frutos_secos', [])) + len(st.session_state.get('grupo3_mantequillas', [])) + len(st.session_state.get('grupo4_cereales', [])) + len(st.session_state.get('grupo4_tortillas_panes', [])) + len(st.session_state.get('grupo4_tuberculos', [])) + len(st.session_state.get('grupo4_leguminosas', [])) + len(st.session_state.get('grupo5_vegetales', [])) + len(st.session_state.get('grupo6_frutas', []))}

=====================================
ANÁLISIS Y RECOMENDACIONES:
=====================================
Este cuestionario de selección alimentaria personalizada proporciona información detallada 
sobre las preferencias, tolerancias y antojos específicos del cliente, permitiendo el 
diseño de planes nutricionales altamente personalizados.

La información recopilada incluye:
- Selecciones específicas por grupos de alimentos
- Identificación de restricciones y alergias
- Mapeo de antojos para estrategias de manejo
- Preferencias de aceites y bebidas sin calorías

Recomendamos consulta nutricional especializada para desarrollar plan alimentario 
personalizado basado en estas selecciones específicas.

=====================================
© 2025 MUPAI - Muscle up GYM
Cuestionario de Selección Alimentaria Personalizada
=====================================
"""
    return resumen

# RESUMEN FINAL Y ENVÍO DE EMAIL
st.markdown("---")
st.markdown('<div class="content-card" style="background: linear-gradient(135deg, #F4C430 0%, #DAA520 100%); color: #1E1E1E;">', unsafe_allow_html=True)
st.markdown("## 🎯 **Resumen Final del Cuestionario de Selección Alimentaria Personalizada**")
st.markdown(f"*Fecha: {fecha_llenado} | Cliente: {nombre}*")

# Mostrar métricas finales
col1, col2, col3 = st.columns(3)
with col1:
    # Calcular totales de proteínas
    total_proteinas_grasas = len(st.session_state.get('grupo1_huevos_embutidos', [])) + len(st.session_state.get('grupo1_carnes_grasas', [])) + len(st.session_state.get('grupo1_quesos_altos', [])) + len(st.session_state.get('grupo1_lacteos_enteros', [])) + len(st.session_state.get('grupo1_pescados_grasos', []))
    total_proteinas_magras = len(st.session_state.get('grupo2_carnes_magras', [])) + len(st.session_state.get('grupo2_pescados_blancos', [])) + len(st.session_state.get('grupo2_quesos_magros', [])) + len(st.session_state.get('grupo2_lacteos_light', [])) + len(st.session_state.get('grupo2_otros', []))
    
    st.markdown(f"""
    ### 🥩 Proteínas
    - **Con grasa:** {total_proteinas_grasas} opciones
    - **Magras:** {total_proteinas_magras} opciones
    - **Restricciones:** {'Sí' if st.session_state.get('alergias_alimentarias') or st.session_state.get('intolerancias') else 'No'}
    """)

with col2:
    # Calcular totales de macronutrientes
    total_grasas = len(st.session_state.get('grupo3_grasas_naturales', [])) + len(st.session_state.get('grupo3_frutos_secos', [])) + len(st.session_state.get('grupo3_mantequillas', []))
    total_carbohidratos = len(st.session_state.get('grupo4_cereales', [])) + len(st.session_state.get('grupo4_tortillas_panes', [])) + len(st.session_state.get('grupo4_tuberculos', [])) + len(st.session_state.get('grupo4_leguminosas', []))
    total_vegetales = len(st.session_state.get('grupo5_vegetales', []))
    
    st.markdown(f"""
    ### 🥑 Macronutrientes  
    - **Grasas saludables:** {total_grasas} opciones
    - **Carbohidratos:** {total_carbohidratos} opciones
    - **Vegetales:** {total_vegetales} opciones
    """)

with col3:
    # Calcular totales adicionales
    total_frutas = len(st.session_state.get('grupo6_frutas', []))
    total_aceites = len(st.session_state.get('aceites_coccion', []))
    total_antojos = len(st.session_state.get('antojos_dulces', [])) + len(st.session_state.get('antojos_salados', [])) + len(st.session_state.get('antojos_comida_rapida', [])) + len(st.session_state.get('antojos_bebidas', [])) + len(st.session_state.get('antojos_condimentos', []))
    
    st.markdown(f"""
    ### 🍎 Adicionales
    - **Frutas:** {total_frutas} opciones
    - **Aceites cocción:** {total_aceites} opciones
    - **Antojos identificados:** {total_antojos} opciones
    """)

# Calcular total general
total_alimentos = total_proteinas_grasas + total_proteinas_magras + total_grasas + total_carbohidratos + total_vegetales + total_frutas

st.success(f"""
### ✅ Cuestionario de Selección Alimentaria Personalizada completado exitosamente

Tu perfil de selección alimentaria ha sido completado con **{total_alimentos} alimentos seleccionados** 
distribuidos en 6 grupos principales, más aceites de cocción, bebidas sin calorías y análisis de antojos.

**Esta información detallada permitirá diseñar planes de alimentación altamente personalizados** 
que se ajusten exactamente a tus gustos, tolerancias y preferencias individuales.

Se recomienda consulta con nutricionista especializado para desarrollar plan alimentario específico 
basado en estas selecciones detalladas.
""")

st.markdown('</div>', unsafe_allow_html=True)

# Función para verificar datos completos
def datos_completos_para_email():
    obligatorios = {
        "Nombre": st.session_state.get('nombre'),
        "Email": st.session_state.get('email_cliente'), 
        "Teléfono": st.session_state.get('telefono'),
        "Edad": st.session_state.get('edad')
    }
    faltantes = [campo for campo, valor in obligatorios.items() if not valor]
    return faltantes

# Botón para enviar email
if not st.session_state.get("correo_enviado", False):
    if st.button("📧 Enviar Resumen por Email", key="enviar_email"):
        faltantes = datos_completos_para_email()
        if faltantes:
            st.error(f"❌ No se puede enviar el email. Faltan: {', '.join(faltantes)}")
        else:
            with st.spinner("📧 Enviando resumen de patrones alimentarios por email..."):
                resumen_completo = crear_resumen_email()
                ok = enviar_email_resumen(
                    resumen_completo, 
                    st.session_state.get('nombre', ''), 
                    st.session_state.get('email_cliente', ''), 
                    st.session_state.get('fecha_llenado', ''), 
                    st.session_state.get('edad', ''), 
                    st.session_state.get('telefono', '')
                )
                if ok:
                    st.session_state["correo_enviado"] = True
                    st.success("✅ Email enviado exitosamente a administración")
                else:
                    st.error("❌ Error al enviar email. Contacta a soporte técnico.")
else:
    st.info("✅ El resumen ya fue enviado por email. Si requieres reenviarlo, usa el botón de 'Reenviar Email'.")

# Opción para reenviar manualmente
if st.button("📧 Reenviar Email", key="reenviar_email"):
    faltantes = datos_completos_para_email()
    if faltantes:
        st.error(f"❌ No se puede reenviar el email. Faltan: {', '.join(faltantes)}")
    else:
        with st.spinner("📧 Reenviando resumen por email..."):
            resumen_completo = crear_resumen_email()
            ok = enviar_email_resumen(
                resumen_completo, 
                st.session_state.get('nombre', ''), 
                st.session_state.get('email_cliente', ''), 
                st.session_state.get('fecha_llenado', ''), 
                st.session_state.get('edad', ''), 
                st.session_state.get('telefono', '')
            )
            if ok:
                st.session_state["correo_enviado"] = True
                st.success("✅ Email reenviado exitosamente a administración")
            else:
                st.error("❌ Error al reenviar email. Contacta a soporte técnico.")

# Limpieza de sesión y botón de nueva evaluación
if st.button("🔄 Nueva Evaluación", key="nueva"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Footer moderno
st.markdown("""
<div class="footer-mupai">
    <h4>MUPAI / Muscle up GYM Alimentary Pattern Assessment Intelligence</h4>
    <span>Digital Nutrition Science</span>
    <br>
    <span>© 2025 MUPAI - Muscle up GYM / MUPAI</span>
    <br>
    <a href="https://muscleupgym.fitness" target="_blank">muscleupgym.fitness</a>
</div>
""", unsafe_allow_html=True)
