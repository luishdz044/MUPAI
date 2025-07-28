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
    page_title="MUPAI - Evaluación de Patrones Alimentarios",
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
        <h1 class="header-title">TEST MUPAI: PATRONES ALIMENTARIOS</h1>
        <p class="header-subtitle">Tu evaluación personalizada de hábitos y preferencias alimentarias basada en ciencia</p>
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
            Ingresa la contraseña para acceder al sistema de evaluación de patrones alimentarios MUPAI
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
                    st.success("✅ Acceso autorizado. Bienvenido al sistema MUPAI de patrones alimentarios.")
                    st.rerun()
                else:
                    st.error("❌ Contraseña incorrecta. Acceso denegado.")
    
    # Mostrar información mientras no esté autenticado
    st.markdown("""
    <div class="content-card" style="margin-top: 3rem; text-align: center; background: #1A1A1A;">
        <h3 style="color: var(--mupai-yellow);">Sistema de Evaluación de Patrones Alimentarios</h3>
        <p style="color: #CCCCCC;">
            MUPAI utiliza metodologías científicas avanzadas para evaluar patrones alimentarios 
            personalizados, preferencias dietéticas y crear planes nutricionales adaptativos.
        </p>
        <p style="color: #999999; font-size: 0.9rem; margin-top: 1.5rem;">
            © 2025 MUPAI - Muscle up GYM 
            Digital Nutrition Science
            Alimentary Pattern Assessment Intelligence
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
        msg['Subject'] = f"Evaluación patrones alimentarios MUPAI - {nombre_cliente} ({fecha})"

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

    # INSTRUCCIONES INICIALES
    st.markdown("""
    <div class="content-card" style="background: linear-gradient(135deg, #F4C430 0%, #DAA520 100%); color: #1E1E1E; margin-bottom: 2rem;">
        <h2 style="color: #1E1E1E; text-align: center; margin-bottom: 1.5rem;">
            📋 INSTRUCCIONES DEL CUESTIONARIO
        </h2>
        <div style="text-align: left; font-size: 1.1rem; line-height: 1.6;">
            <p><strong>🎯 Objetivo:</strong> Este cuestionario nos ayudará a crear un plan nutricional completamente personalizado basado en tus preferencias, necesidades y estilo de vida.</p>
            
            <p><strong>📝 Instrucciones:</strong></p>
            <ul style="margin-left: 1.5rem;">
                <li>Responde todas las preguntas con honestidad y precisión</li>
                <li>Si no estás seguro de una respuesta, elige la opción más cercana a tu realidad</li>
                <li>No hay respuestas correctas o incorrectas, solo necesitamos conocerte mejor</li>
                <li>El cuestionario tiene 6 grupos principales más secciones adicionales</li>
                <li>Toma tu tiempo, la calidad de tus respuestas mejorará tu plan nutricional</li>
            </ul>
            
            <p><strong>⏱️ Tiempo estimado:</strong> 15-20 minutos</p>
            <p><strong>🔒 Privacidad:</strong> Toda tu información será tratada de forma confidencial</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # GRUPO 1: INFORMACIÓN BÁSICA NUTRICIONAL
    with st.expander("🥗 **GRUPO 1: INFORMACIÓN BÁSICA NUTRICIONAL**", expanded=True):
        progress.progress(10)
        progress_text.text("Grupo 1 de 6: Información básica nutricional")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🍽️ Hábitos alimentarios actuales")
        
        col1, col2 = st.columns(2)
        with col1:
            comidas_por_dia_actual = st.selectbox(
                "¿Cuántas comidas realizas habitualmente al día?",
                ["1 comida", "2 comidas", "3 comidas", "4 comidas", "5 comidas", "6 o más comidas"],
                help="Incluye todas las comidas principales y colaciones"
            )
            
            agua_diaria = st.selectbox(
                "¿Cuántos vasos de agua tomas al día aproximadamente?",
                ["1-2 vasos", "3-4 vasos", "5-6 vasos", "7-8 vasos", "9-10 vasos", "Más de 10 vasos"],
                help="Considera solo agua pura, no otras bebidas"
            )
            
            ejercicio_frecuencia = st.selectbox(
                "¿Con qué frecuencia realizas ejercicio?",
                ["No hago ejercicio", "1-2 veces por semana", "3-4 veces por semana", "5-6 veces por semana", "Todos los días"],
                help="Incluye cualquier tipo de actividad física planificada"
            )
        
        with col2:
            peso_objetivo = st.selectbox(
                "¿Cuál es tu objetivo principal de peso?",
                ["Mantener mi peso actual", "Perder peso", "Ganar peso", "Ganar masa muscular", "Mejorar composición corporal"],
                help="Selecciona tu objetivo más importante"
            )
            
            energia_nivel = st.selectbox(
                "¿Cómo describirías tu nivel de energía durante el día?",
                ["Muy bajo, siempre cansado", "Bajo, me canso fácil", "Normal, estable", "Alto, me siento activo", "Muy alto, lleno de energía"],
                help="Considera tu energía promedio en un día típico"
            )
            
            apetito_nivel = st.selectbox(
                "¿Cómo describirías tu apetito habitualmente?",
                ["Muy poco apetito", "Poco apetito", "Apetito normal", "Buen apetito", "Mucho apetito, siempre tengo hambre"],
                help="Piensa en tu sensación de hambre promedio"
            )

        # Guardar en session state
        st.session_state.comidas_por_dia_actual = comidas_por_dia_actual
        st.session_state.agua_diaria = agua_diaria
        st.session_state.ejercicio_frecuencia = ejercicio_frecuencia
        st.session_state.peso_objetivo = peso_objetivo
        st.session_state.energia_nivel = energia_nivel
        st.session_state.apetito_nivel = apetito_nivel
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 2: FUENTES DE PROTEÍNA
    with st.expander("🥩 **GRUPO 2: FUENTES DE PROTEÍNA**", expanded=True):
        progress.progress(20)
        progress_text.text("Grupo 2 de 6: Fuentes de proteína")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🍖 Proteínas que consumes regularmente")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🐄 Proteínas animales")
            proteinas_animales = st.multiselect(
                "Selecciona las proteínas animales que consumes:",
                ["Pollo", "Pavo", "Res", "Cerdo", "Pescado blanco", "Pescado azul", "Mariscos", 
                 "Huevos enteros", "Claras de huevo", "Lácteos (leche, yogurt)", "Quesos", "Embutidos"],
                help="Marca todas las que consumes habitualmente"
            )
            
            frecuencia_proteina_animal = st.selectbox(
                "¿Con qué frecuencia consumes proteína animal?",
                ["Nunca", "1-2 veces por semana", "3-4 veces por semana", "5-6 veces por semana", "Diariamente", "Varias veces al día"],
                help="Considera todas las proteínas animales en conjunto"
            )
        
        with col2:
            st.markdown("#### 🌱 Proteínas vegetales")
            proteinas_vegetales = st.multiselect(
                "Selecciona las proteínas vegetales que consumes:",
                ["Frijoles", "Lentejas", "Garbanzos", "Quinoa", "Tofu", "Tempeh", "Seitán", 
                 "Frutos secos", "Semillas", "Proteína en polvo vegetal", "Legumbres en general"],
                help="Marca todas las que consumes habitualmente"
            )
            
            frecuencia_proteina_vegetal = st.selectbox(
                "¿Con qué frecuencia consumes proteína vegetal?",
                ["Nunca", "1-2 veces por semana", "3-4 veces por semana", "5-6 veces por semana", "Diariamente", "Varias veces al día"],
                help="Considera todas las proteínas vegetales en conjunto"
            )

        st.markdown("### 🥤 Suplementos proteicos")
        suplementos_proteina = st.multiselect(
            "¿Utilizas algún suplemento de proteína?",
            ["Proteína whey", "Proteína caseína", "Proteína vegetal en polvo", "Proteína de huevo", 
             "Aminoácidos BCAA", "Creatina", "No uso suplementos proteicos"],
            help="Selecciona todos los que uses regularmente"
        )

        # Guardar en session state
        st.session_state.proteinas_animales = proteinas_animales
        st.session_state.frecuencia_proteina_animal = frecuencia_proteina_animal
        st.session_state.proteinas_vegetales = proteinas_vegetales
        st.session_state.frecuencia_proteina_vegetal = frecuencia_proteina_vegetal
        st.session_state.suplementos_proteina = suplementos_proteina
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 3: FUENTES DE GRASA SALUDABLE
    with st.expander("🥑 **GRUPO 3: FUENTES DE GRASA SALUDABLE**", expanded=True):
        progress.progress(30)
        progress_text.text("Grupo 3 de 6: Fuentes de grasa saludable")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🫒 Grasas que incluyes en tu alimentación")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🥑 Grasas vegetales")
            grasas_vegetales = st.multiselect(
                "Selecciona las grasas vegetales que consumes:",
                ["Aguacate", "Aceite de oliva", "Aceite de coco", "Aceite de canola", "Frutos secos (nueces, almendras)", 
                 "Semillas (chía, linaza, girasol)", "Aceitunas", "Mantequilla de frutos secos", "Tahini"],
                help="Marca todas las que consumes habitualmente"
            )
            
            frecuencia_grasas_vegetales = st.selectbox(
                "¿Con qué frecuencia consumes grasas vegetales?",
                ["Nunca", "1-2 veces por semana", "3-4 veces por semana", "5-6 veces por semana", "Diariamente"],
                help="Considera todas las grasas vegetales en conjunto"
            )
        
        with col2:
            st.markdown("#### 🐟 Grasas animales")
            grasas_animales = st.multiselect(
                "Selecciona las grasas animales que consumes:",
                ["Pescado graso (salmón, atún, sardinas)", "Mantequilla", "Yema de huevo", 
                 "Grasa de carnes", "Ghee", "Aceite de pescado (suplemento)"],
                help="Marca todas las que consumes habitualmente"
            )
            
            frecuencia_grasas_animales = st.selectbox(
                "¿Con qué frecuencia consumes grasas animales?",
                ["Nunca", "1-2 veces por semana", "3-4 veces por semana", "5-6 veces por semana", "Diariamente"],
                help="Considera todas las grasas animales en conjunto"
            )

        # Guardar en session state
        st.session_state.grasas_vegetales = grasas_vegetales
        st.session_state.frecuencia_grasas_vegetales = frecuencia_grasas_vegetales
        st.session_state.grasas_animales = grasas_animales
        st.session_state.frecuencia_grasas_animales = frecuencia_grasas_animales
        
        st.markdown('</div>', unsafe_allow_html=True)

    # PREGUNTA SOBRE MÉTODOS DE COCCIÓN (después del GRUPO 3, antes del GRUPO 4)
    with st.expander("👨‍🍳 **MÉTODOS DE COCCIÓN DISPONIBLES**", expanded=True):
        progress.progress(35)
        progress_text.text("Métodos de cocción: Evaluando tus recursos culinarios")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🔥 Métodos de cocción que tienes disponibles")
        
        metodos_disponibles = st.multiselect(
            "¿Qué métodos de cocción tienes disponibles en casa? (multiselección)",
            ["Hervido", "Al vapor", "A la plancha", "A la parrilla", "Salteado", "Frito", 
             "Horno convencional", "Microondas", "Olla lenta (slow cooker)", "Olla de presión", 
             "Air fryer", "Crudo", "Sofrito", "Guisado", "Wok", "Otro"],
            help="Selecciona todos los métodos que puedes usar en tu cocina"
        )
        
        if "Otro" in metodos_disponibles:
            otro_metodo = st.text_input(
                "Especifica otro método de cocción:",
                placeholder="Ej: Parrilla eléctrica, vaporera bambú...",
                help="Describe el método que no está en la lista"
            )
            st.session_state.otro_metodo_coccion = otro_metodo
        
        # Segunda pregunta: métodos más accesibles/prácticos
        if metodos_disponibles:
            metodos_practicos = st.multiselect(
                "¿Cuáles se te hacen más accesibles/prácticos para el día a día de tu plan? (multiselección)",
                metodos_disponibles,  # Solo mostrar los que marcó como disponibles
                help="De los métodos que tienes disponibles, ¿cuáles usas más frecuentemente?"
            )
            st.session_state.metodos_practicos = metodos_practicos
        else:
            st.info("Primero selecciona los métodos disponibles para poder elegir los más prácticos")
            metodos_practicos = []

        # Guardar en session state
        st.session_state.metodos_disponibles = metodos_disponibles
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 4: CARBOHIDRATOS Y ENERGÍA
    with st.expander("🍞 **GRUPO 4: CARBOHIDRATOS Y ENERGÍA**", expanded=True):
        progress.progress(45)
        progress_text.text("Grupo 4 de 6: Carbohidratos y energía")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🌾 Fuentes de carbohidratos que consumes")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🍞 Cereales y granos")
            cereales_granos = st.multiselect(
                "Selecciona los cereales y granos que consumes:",
                ["Arroz blanco", "Arroz integral", "Avena", "Quinoa", "Pan blanco", "Pan integral", 
                 "Pasta", "Cereales de desayuno", "Amaranto", "Cebada", "Trigo sarraceno"],
                help="Marca todos los que consumes habitualmente"
            )
            
            frecuencia_cereales = st.selectbox(
                "¿Con qué frecuencia consumes cereales y granos?",
                ["Nunca", "1-2 veces por semana", "3-4 veces por semana", "5-6 veces por semana", "Diariamente", "Varias veces al día"],
                help="Considera todos los cereales y granos en conjunto"
            )
        
        with col2:
            st.markdown("#### 🥔 Tubérculos y vegetales amiláceos")
            tuberculos = st.multiselect(
                "Selecciona los tubérculos que consumes:",
                ["Papa", "Camote/Boniato", "Yuca/Mandioca", "Plátano macho", "Maíz", 
                 "Calabaza", "Betabel", "Zanahoria"],
                help="Marca todos los que consumes habitualmente"
            )
            
            frecuencia_tuberculos = st.selectbox(
                "¿Con qué frecuencia consumes tubérculos?",
                ["Nunca", "1-2 veces por semana", "3-4 veces por semana", "5-6 veces por semana", "Diariamente"],
                help="Considera todos los tubérculos en conjunto"
            )

        st.markdown("### 🍎 Frutas y vegetales")
        col1, col2 = st.columns(2)
        with col1:
            frutas_consumo = st.selectbox(
                "¿Cuántas porciones de fruta consumes al día?",
                ["No como frutas", "1 porción", "2 porciones", "3 porciones", "4 o más porciones"],
                help="Una porción = 1 fruta mediana o 1 taza de fruta picada"
            )
        
        with col2:
            vegetales_consumo = st.selectbox(
                "¿Cuántas porciones de vegetales consumes al día?",
                ["No como vegetales", "1 porción", "2 porciones", "3 porciones", "4 o más porciones"],
                help="Una porción = 1 taza de vegetales crudos o 1/2 taza cocidos"
            )

        # Guardar en session state
        st.session_state.cereales_granos = cereales_granos
        st.session_state.frecuencia_cereales = frecuencia_cereales
        st.session_state.tuberculos = tuberculos
        st.session_state.frecuencia_tuberculos = frecuencia_tuberculos
        st.session_state.frutas_consumo = frutas_consumo
        st.session_state.vegetales_consumo = vegetales_consumo
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 5: HIDRATACIÓN Y BEBIDAS
    with st.expander("🥤 **GRUPO 5: HIDRATACIÓN Y BEBIDAS**", expanded=True):
        progress.progress(55)
        progress_text.text("Grupo 5 de 6: Hidratación y bebidas")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 💧 Hábitos de hidratación")
        
        col1, col2 = st.columns(2)
        with col1:
            agua_pura_consumo = st.selectbox(
                "¿Cuántos litros de agua pura tomas al día?",
                ["Menos de 1 litro", "1-1.5 litros", "1.5-2 litros", "2-2.5 litros", "2.5-3 litros", "Más de 3 litros"],
                help="Solo agua pura, sin saborizantes"
            )
            
            bebidas_con_cafeina = st.multiselect(
                "¿Qué bebidas con cafeína consumes?",
                ["Café negro", "Café con leche", "Té verde", "Té negro", "Bebidas energéticas", 
                 "Refrescos de cola", "Chocolate caliente", "No consumo cafeína"],
                help="Selecciona todas las que consumes habitualmente"
            )
        
        with col2:
            frecuencia_cafeina = st.selectbox(
                "¿Con qué frecuencia consumes bebidas con cafeína?",
                ["Nunca", "Ocasionalmente", "1 vez al día", "2-3 veces al día", "4 o más veces al día"],
                help="Considera todas las bebidas con cafeína juntas"
            )
            
            otras_bebidas = st.multiselect(
                "¿Qué otras bebidas consumes regularmente?",
                ["Jugos naturales", "Jugos procesados", "Refrescos/Sodas", "Bebidas deportivas", 
                 "Leche", "Leches vegetales", "Kombucha", "Agua con gas", "Infusiones sin cafeína"],
                help="Selecciona todas las bebidas que tomes habitualmente"
            )

        st.markdown("### 🍷 Consumo de alcohol")
        consumo_alcohol = st.selectbox(
            "¿Consumes bebidas alcohólicas?",
            ["No consumo alcohol", "Ocasionalmente (1-2 veces al mes)", "1-2 veces por semana", 
             "3-4 veces por semana", "5-6 veces por semana", "Diariamente"],
            help="Sé honesto sobre tu consumo real de alcohol"
        )
        
        if consumo_alcohol != "No consumo alcohol":
            tipos_alcohol = st.multiselect(
                "¿Qué tipos de bebidas alcohólicas prefieres?",
                ["Cerveza", "Vino tinto", "Vino blanco", "Destilados (tequila, whisky, etc.)", 
                 "Cócteles/Tragos", "Licores dulces"],
                help="Selecciona los tipos que consumes más frecuentemente"
            )
            st.session_state.tipos_alcohol = tipos_alcohol

        # Guardar en session state
        st.session_state.agua_pura_consumo = agua_pura_consumo
        st.session_state.bebidas_con_cafeina = bebidas_con_cafeina
        st.session_state.frecuencia_cafeina = frecuencia_cafeina
        st.session_state.otras_bebidas = otras_bebidas
        st.session_state.consumo_alcohol = consumo_alcohol
        
        st.markdown('</div>', unsafe_allow_html=True)

    # GRUPO 6: SUPLEMENTOS Y PRODUCTOS ESPECIALES
    with st.expander("💊 **GRUPO 6: SUPLEMENTOS Y PRODUCTOS ESPECIALES**", expanded=True):
        progress.progress(65)
        progress_text.text("Grupo 6 de 6: Suplementos y productos especiales")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🧪 Suplementos nutricionales")
        
        col1, col2 = st.columns(2)
        with col1:
            usa_suplementos = st.radio(
                "¿Actualmente tomas suplementos nutricionales?",
                ["No tomo suplementos", "Sí, tomo algunos", "Sí, tomo varios", "Sí, tomo muchos"],
                help="Incluye vitaminas, minerales, y otros suplementos"
            )
            
            if usa_suplementos != "No tomo suplementos":
                suplementos_actuales = st.multiselect(
                    "¿Qué suplementos tomas actualmente?",
                    ["Multivitamínico", "Vitamina D", "Vitamina C", "Vitaminas del complejo B", 
                     "Omega 3", "Calcio", "Magnesio", "Zinc", "Hierro", "Probióticos", 
                     "Proteína en polvo", "Creatina", "BCAA", "Glutamina", "Pre-entreno", 
                     "Quemadores de grasa", "Otros"],
                    help="Selecciona todos los que tomas regularmente"
                )
                st.session_state.suplementos_actuales = suplementos_actuales
        
        with col2:
            productos_especiales = st.multiselect(
                "¿Consumes productos dietéticos especiales?",
                ["Productos sin gluten", "Productos sin lactosa", "Productos veganos", 
                 "Productos keto", "Productos light/diet", "Edulcorantes artificiales", 
                 "Sal de mar/rosa", "Vinagres especiales", "Aceites premium", "Superfoods"],
                help="Productos que compras específicamente por sus características nutricionales"
            )
            
            frecuencia_productos_especiales = st.selectbox(
                "¿Con qué frecuencia consumes productos dietéticos especiales?",
                ["Nunca", "Ocasionalmente", "1-2 veces por semana", "3-4 veces por semana", "Diariamente"],
                help="Considera todos los productos especiales en conjunto"
            )

        # Guardar en session state
        st.session_state.usa_suplementos = usa_suplementos
        st.session_state.productos_especiales = productos_especiales
        st.session_state.frecuencia_productos_especiales = frecuencia_productos_especiales
        
        st.markdown('</div>', unsafe_allow_html=True)

    # APARTADO: ACEITES Y GRASAS DE COCINA
    with st.expander("🫒 **APARTADO: ACEITES Y GRASAS DE COCINA**", expanded=True):
        progress.progress(70)
        progress_text.text("Apartado especial: Aceites y grasas de cocina")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🧄 Aceites y grasas que usas para cocinar")
        
        col1, col2 = st.columns(2)
        with col1:
            aceites_cocina = st.multiselect(
                "¿Qué aceites usas para cocinar?",
                ["Aceite de oliva extra virgen", "Aceite de oliva regular", "Aceite de canola", 
                 "Aceite de girasol", "Aceite de coco", "Aceite de aguacate", "Aceite de sésamo", 
                 "Mantequilla", "Ghee", "Manteca de cerdo", "Aceite en spray", "No uso aceites"],
                help="Selecciona todos los aceites que usas para cocinar"
            )
            
            preferencia_coccion = st.selectbox(
                "¿Cuál es tu aceite preferido para cocinar a altas temperaturas?",
                ["Aceite de coco", "Aceite de aguacate", "Ghee", "Aceite de canola", 
                 "Aceite de girasol alto oleico", "Mantequilla", "No cocino a altas temperaturas"],
                help="Para freír, saltear o cocinar en el horno"
            )
        
        with col2:
            aceites_ensalada = st.multiselect(
                "¿Qué aceites usas para ensaladas o en crudo?",
                ["Aceite de oliva extra virgen", "Aceite de linaza", "Aceite de nuez", 
                 "Aceite de sésamo", "Aceite de aguacate", "Vinagre balsámico", 
                 "Aceite de coco virgen", "No uso aceites en crudo"],
                help="Aceites que usas sin cocinar, en ensaladas o aderezos"
            )
            
            cantidad_aceite_dia = st.selectbox(
                "¿Aproximadamente cuánto aceite usas al día?",
                ["No uso aceite", "1-2 cucharaditas", "1-2 cucharadas", "3-4 cucharadas", "Más de 4 cucharadas"],
                help="Considera todo el aceite que usas para cocinar y aderezar"
            )

        # Guardar en session state
        st.session_state.aceites_cocina = aceites_cocina
        st.session_state.preferencia_coccion = preferencia_coccion
        st.session_state.aceites_ensalada = aceites_ensalada
        st.session_state.cantidad_aceite_dia = cantidad_aceite_dia
        
        st.markdown('</div>', unsafe_allow_html=True)

    # APARTADO: ALERGIAS E INTOLERANCIAS
    with st.expander("⚠️ **APARTADO: ALERGIAS E INTOLERANCIAS**", expanded=True):
        progress.progress(75)
        progress_text.text("Apartado especial: Alergias e intolerancias")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🚨 Alergias alimentarias")
        
        tiene_alergias = st.radio(
            "¿Tienes alergias alimentarias diagnosticadas?",
            ["No tengo alergias", "Sí, tengo alergias leves", "Sí, tengo alergias severas"],
            help="Las alergias pueden causar reacciones graves, incluso peligrosas"
        )
        
        if tiene_alergias != "No tengo alergias":
            alergias_especificas = st.multiselect(
                "¿A qué alimentos eres alérgico?",
                ["Frutos secos (nueces, almendras, etc.)", "Maní/Cacahuate", "Mariscos", "Pescado", 
                 "Huevos", "Leche/Lácteos", "Soja", "Trigo/Gluten", "Semillas de sésamo", 
                 "Frutas específicas", "Otros"],
                help="Selecciona todos los alimentos que te causan reacciones alérgicas"
            )
            
            if "Otros" in alergias_especificas:
                otras_alergias = st.text_area(
                    "Especifica otras alergias:",
                    placeholder="Describe otros alimentos o sustancias que te causen alergia",
                    help="Sé específico para crear un plan seguro"
                )
                st.session_state.otras_alergias = otras_alergias
            
            st.session_state.alergias_especificas = alergias_especificas

        st.markdown("### 🤢 Intolerancias alimentarias")
        
        tiene_intolerancias = st.radio(
            "¿Tienes intolerancias alimentarias?",
            ["No tengo intolerancias", "Sí, tengo intolerancias leves", "Sí, tengo intolerancias severas"],
            help="Las intolerancias causan malestar digestivo pero no son peligrosas"
        )
        
        if tiene_intolerancias != "No tengo intolerancias":
            intolerancias_especificas = st.multiselect(
                "¿A qué alimentos eres intolerante?",
                ["Lactosa", "Gluten", "Fructosa", "FODMAP", "Histamina", "Cafeína", 
                 "Alcohol", "Edulcorantes artificiales", "Glutamato monosódico", "Otros"],
                help="Selecciona todos los alimentos que te causan malestar digestivo"
            )
            
            if "Otros" in intolerancias_especificas:
                otras_intolerancias = st.text_area(
                    "Especifica otras intolerancias:",
                    placeholder="Describe otros alimentos que te causen malestar",
                    help="Incluye síntomas si los conoces"
                )
                st.session_state.otras_intolerancias = otras_intolerancias
            
            st.session_state.intolerancias_especificas = intolerancias_especificas

        # Guardar en session state
        st.session_state.tiene_alergias = tiene_alergias
        st.session_state.tiene_intolerancias = tiene_intolerancias
        
        st.markdown('</div>', unsafe_allow_html=True)

    # APARTADO: PREFERENCIAS ALIMENTARIAS
    with st.expander("😋 **APARTADO: PREFERENCIAS ALIMENTARIAS**", expanded=True):
        progress.progress(80)
        progress_text.text("Apartado especial: Preferencias alimentarias")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Tus gustos y preferencias")
        
        col1, col2 = st.columns(2)
        with col1:
            sabores_favoritos = st.multiselect(
                "¿Qué sabores disfrutas más?",
                ["Dulce", "Salado", "Ácido/Agrio", "Amargo", "Picante", "Especiado", 
                 "Ahumado", "Umami", "Suave/Neutro"],
                help="Selecciona todos los sabores que realmente disfrutas"
            )
            
            texturas_favoritas = st.multiselect(
                "¿Qué texturas prefieres en los alimentos?",
                ["Crujiente", "Suave", "Cremosa", "Masticable", "Líquida", "Gelatinosa", 
                 "Fibrosa", "Aireada/Espumosa"],
                help="Piensa en las texturas que más te satisfacen"
            )
            
            temperaturas_preferidas = st.multiselect(
                "¿A qué temperatura prefieres los alimentos?",
                ["Muy caliente", "Caliente", "Tibia", "Temperatura ambiente", "Fría", "Helada"],
                help="Considera tanto bebidas como comidas"
            )
        
        with col2:
            comidas_comfort = st.text_area(
                "¿Cuáles son tus 3 comidas favoritas de todos los tiempos?",
                placeholder="Ej: Pizza margarita, tacos al pastor, helado de chocolate...",
                help="Esas comidas que siempre te hacen feliz"
            )
            
            alimentos_no_gustan = st.text_area(
                "¿Hay alimentos que definitivamente NO te gustan?",
                placeholder="Ej: Brócoli, hígado, pescado, comida muy picante...",
                help="Alimentos que evitas por gusto, no por alergia"
            )
            
            curiosidad_alimentaria = st.selectbox(
                "¿Qué tan abierto eres a probar alimentos nuevos?",
                ["Muy cerrado, solo como lo conocido", "Algo cerrado, rara vez pruebo cosas nuevas", 
                 "Neutro, a veces pruebo cosas nuevas", "Abierto, me gusta probar cosas nuevas", 
                 "Muy abierto, siempre busco nuevos sabores"],
                help="Esto nos ayuda a saber qué tan variado puede ser tu plan"
            )

        # Guardar en session state
        st.session_state.sabores_favoritos = sabores_favoritos
        st.session_state.texturas_favoritas = texturas_favoritas
        st.session_state.temperaturas_preferidas = temperaturas_preferidas
        st.session_state.comidas_comfort = comidas_comfort
        st.session_state.alimentos_no_gustan = alimentos_no_gustan
        st.session_state.curiosidad_alimentaria = curiosidad_alimentaria
        
        st.markdown('</div>', unsafe_allow_html=True)

    # APARTADO: ANTOJOS Y PATRONES EMOCIONALES
    with st.expander("🍫 **APARTADO: ANTOJOS Y PATRONES EMOCIONALES**", expanded=True):
        progress.progress(85)
        progress_text.text("Apartado especial: Antojos y patrones emocionales")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🧠 Antojos y alimentación emocional")
        
        col1, col2 = st.columns(2)
        with col1:
            frecuencia_antojos = st.selectbox(
                "¿Con qué frecuencia tienes antojos de comida?",
                ["Nunca o rara vez", "1-2 veces por semana", "3-4 veces por semana", 
                 "Diariamente", "Varias veces al día"],
                help="Antojos = deseos intensos de comer algo específico"
            )
            
            tipos_antojos = st.multiselect(
                "¿Qué tipo de alimentos se te antojan más?",
                ["Dulces (chocolate, postres)", "Salados (papas, snacks)", "Grasosos (pizza, hamburguesas)", 
                 "Carbohidratos (pan, pasta)", "Bebidas azucaradas", "Comida rápida", 
                 "Helados", "Frutas", "No tengo antojos específicos"],
                help="Selecciona los tipos de comida que más se te antojan"
            )
            
            horarios_antojos = st.multiselect(
                "¿A qué horas del día tienes más antojos?",
                ["Mañana", "Media mañana", "Mediodía", "Tarde", "Noche", "Madrugada", 
                 "No tengo horarios específicos"],
                help="Identifica si hay patrones en tus antojos"
            )
        
        with col2:
            triggers_emocionales = st.multiselect(
                "¿En qué situaciones comes por emociones?",
                ["Cuando estoy estresado", "Cuando estoy triste", "Cuando estoy ansioso", 
                 "Cuando estoy aburrido", "Cuando estoy feliz/celebrando", 
                 "Cuando estoy cansado", "Por costumbre/rutina", "No como por emociones"],
                help="Identifica tus triggers emocionales para comer"
            )
            
            control_antojos = st.selectbox(
                "¿Qué tan fácil te resulta resistir los antojos?",
                ["Muy fácil, casi siempre resisto", "Fácil, usualmente resisto", 
                 "Difícil, a veces cedo", "Muy difícil, casi siempre cedo", 
                 "Imposible, siempre cedo a los antojos"],
                help="Sé honesto sobre tu autocontrol actual"
            )
            
            estrategias_antojos = st.text_area(
                "¿Qué estrategias has usado para manejar antojos?",
                placeholder="Ej: Beber agua, distraerme, comer fruta, hacer ejercicio...",
                help="Comparte qué te ha funcionado o no"
            )

        # Guardar en session state
        st.session_state.frecuencia_antojos = frecuencia_antojos
        st.session_state.tipos_antojos = tipos_antojos
        st.session_state.horarios_antojos = horarios_antojos
        st.session_state.triggers_emocionales = triggers_emocionales
        st.session_state.control_antojos = control_antojos
        st.session_state.estrategias_antojos = estrategias_antojos
        
        st.markdown('</div>', unsafe_allow_html=True)

    # BLOQUE FINAL: INFORMACIÓN ADICIONAL Y CONTEXTO
    with st.expander("📝 **INFORMACIÓN ADICIONAL Y CONTEXTO**", expanded=True):
        progress.progress(90)
        progress_text.text("Información adicional: Completando tu perfil")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🏠 Contexto personal y familiar")
        
        col1, col2 = st.columns(2)
        with col1:
            situacion_familiar = st.selectbox(
                "¿Cuál es tu situación familiar?",
                ["Vivo solo", "Vivo en pareja", "Vivo con familia (padres/hermanos)", 
                 "Tengo hijos pequeños", "Tengo familia numerosa", "Vivo con roommates"],
                help="Esto afecta la planificación de comidas"
            )
            
            quien_cocina = st.selectbox(
                "¿Quién cocina principalmente en tu hogar?",
                ["Yo cocino todo", "Cocino principalmente yo", "Compartimos las tareas", 
                 "Cocina principalmente otra persona", "Otra persona cocina todo", "Comemos fuera/delivery"],
                help="Necesitamos saber quién preparará las comidas"
            )
            
            presupuesto_comida = st.selectbox(
                "¿Cómo describirías tu presupuesto para alimentación?",
                ["Muy limitado", "Limitado", "Moderado", "Holgado", "Sin limitaciones"],
                help="Esto nos ayuda a sugerir opciones adecuadas"
            )
        
        with col2:
            trabajo_horarios = st.selectbox(
                "¿Cómo son tus horarios de trabajo/estudio?",
                ["Horario fijo estándar (9-5)", "Horario fijo no estándar", "Turnos rotativos", 
                 "Horario flexible", "Trabajo desde casa", "Estudiante", "Sin horario fijo"],
                help="Los horarios afectan cuándo y cómo puedes comer"
            )
            
            eventos_sociales = st.selectbox(
                "¿Con qué frecuencia tienes eventos sociales que involucran comida?",
                ["Nunca o rara vez", "1-2 veces al mes", "1-2 veces por semana", 
                 "3-4 veces por semana", "Casi diariamente"],
                help="Cenas de trabajo, fiestas, reuniones familiares, etc."
            )
            
            viajes_frecuencia = st.selectbox(
                "¿Con qué frecuencia viajas o comes fuera de casa?",
                ["Nunca", "Ocasionalmente", "1-2 veces por mes", "Semanalmente", "Muy frecuentemente"],
                help="Viajes de trabajo, vacaciones, etc."
            )

        st.markdown("### 🎯 Objetivos y motivaciones específicas")
        
        objetivo_principal_detallado = st.selectbox(
            "¿Cuál es tu objetivo principal más específico?",
            ["Perder grasa corporal manteniendo músculo", "Ganar masa muscular", "Mejorar energía y bienestar", 
             "Controlar una condición médica", "Mejorar rendimiento deportivo", "Establecer hábitos saludables", 
             "Reducir inflamación", "Mejorar digestión", "Longevidad y antienvejecimiento"],
            help="Sé específico sobre lo que más quieres lograr"
        )
        
        razon_cambio = st.text_area(
            "¿Qué te motivó a buscar ayuda nutricional ahora?",
            placeholder="Ej: Me siento sin energía, quiero bajar de peso, tengo problemas digestivos...",
            help="Cuéntanos qué te trajo hasta aquí"
        )
        
        experiencias_previas = st.text_area(
            "¿Has seguido planes nutricionales antes? ¿Cómo fue tu experiencia?",
            placeholder="Ej: Probé keto pero no me funcionó, conté calorías pero era muy tedioso...",
            help="Esto nos ayuda a evitar estrategias que no te funcionaron"
        )

        # Guardar en session state
        st.session_state.situacion_familiar = situacion_familiar
        st.session_state.quien_cocina = quien_cocina
        st.session_state.presupuesto_comida = presupuesto_comida
        st.session_state.trabajo_horarios = trabajo_horarios
        st.session_state.eventos_sociales = eventos_sociales
        st.session_state.viajes_frecuencia = viajes_frecuencia
        st.session_state.objetivo_principal_detallado = objetivo_principal_detallado
        st.session_state.razon_cambio = razon_cambio
        st.session_state.experiencias_previas = experiencias_previas
        
        st.markdown('</div>', unsafe_allow_html=True)

    # RESULTADO FINAL: Análisis completo de patrones alimentarios
    with st.expander("📈 **RESULTADO FINAL: Tu Perfil Alimentario Completo**", expanded=True):
        progress.progress(100)
        progress_text.text("Análisis completo: Generando tu perfil alimentario personalizado")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Tu Perfil Alimentario Personalizado")
        
        # Crear resumen del perfil por grupos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Grupo 1: Información Básica")
            st.write(f"• **Comidas por día:** {st.session_state.get('comidas_por_dia_actual', 'No especificado')}")
            st.write(f"• **Objetivo principal:** {st.session_state.get('peso_objetivo', 'No especificado')}")
            st.write(f"• **Nivel de energía:** {st.session_state.get('energia_nivel', 'No especificado')}")
            st.write(f"• **Ejercicio:** {st.session_state.get('ejercicio_frecuencia', 'No especificado')}")
            
            st.markdown("#### 🥩 Grupo 2: Proteínas")
            if st.session_state.get('proteinas_animales'):
                proteinas_lista = st.session_state.get('proteinas_animales', [])
                st.write(f"• **Proteínas animales:** {', '.join(proteinas_lista[:3])}{'...' if len(proteinas_lista) > 3 else ''}")
            if st.session_state.get('proteinas_vegetales'):
                proteinas_veg_lista = st.session_state.get('proteinas_vegetales', [])
                st.write(f"• **Proteínas vegetales:** {', '.join(proteinas_veg_lista[:3])}{'...' if len(proteinas_veg_lista) > 3 else ''}")
            
            st.markdown("#### 🥑 Grupo 3: Grasas Saludables")
            if st.session_state.get('grasas_vegetales'):
                grasas_veg_lista = st.session_state.get('grasas_vegetales', [])
                st.write(f"• **Grasas vegetales:** {', '.join(grasas_veg_lista[:3])}{'...' if len(grasas_veg_lista) > 3 else ''}")
            if st.session_state.get('grasas_animales'):
                grasas_an_lista = st.session_state.get('grasas_animales', [])
                st.write(f"• **Grasas animales:** {', '.join(grasas_an_lista[:3])}{'...' if len(grasas_an_lista) > 3 else ''}")
        
        with col2:
            st.markdown("#### 🍞 Grupo 4: Carbohidratos")
            if st.session_state.get('cereales_granos'):
                cereales_lista = st.session_state.get('cereales_granos', [])
                st.write(f"• **Cereales:** {', '.join(cereales_lista[:3])}{'...' if len(cereales_lista) > 3 else ''}")
            st.write(f"• **Frutas:** {st.session_state.get('frutas_consumo', 'No especificado')}")
            st.write(f"• **Vegetales:** {st.session_state.get('vegetales_consumo', 'No especificado')}")
            
            st.markdown("#### 🥤 Grupo 5: Hidratación")
            st.write(f"• **Agua diaria:** {st.session_state.get('agua_pura_consumo', 'No especificado')}")
            st.write(f"• **Cafeína:** {st.session_state.get('frecuencia_cafeina', 'No especificado')}")
            st.write(f"• **Alcohol:** {st.session_state.get('consumo_alcohol', 'No especificado')}")
            
            st.markdown("#### 💊 Grupo 6: Suplementos")
            st.write(f"• **Usa suplementos:** {st.session_state.get('usa_suplementos', 'No especificado')}")
            st.write(f"• **Productos especiales:** {st.session_state.get('frecuencia_productos_especiales', 'No especificado')}")

        # Sección de métodos de cocción
        st.markdown("#### 👨‍🍳 Métodos de Cocción")
        if st.session_state.get('metodos_disponibles'):
            metodos_lista = st.session_state.get('metodos_disponibles', [])
            st.write(f"• **Disponibles:** {', '.join(metodos_lista[:5])}{'...' if len(metodos_lista) > 5 else ''}")
        if st.session_state.get('metodos_practicos'):
            metodos_prac_lista = st.session_state.get('metodos_practicos', [])
            st.write(f"• **Más prácticos:** {', '.join(metodos_prac_lista[:3])}{'...' if len(metodos_prac_lista) > 3 else ''}")

        # Restricciones importantes
        if (st.session_state.get('tiene_alergias') and st.session_state.get('tiene_alergias') != "No tengo alergias") or (st.session_state.get('tiene_intolerancias') and st.session_state.get('tiene_intolerancias') != "No tengo intolerancias"):
            st.markdown("#### ⚠️ Restricciones Importantes")
            if st.session_state.get('tiene_alergias') and st.session_state.get('tiene_alergias') != "No tengo alergias":
                st.warning(f"**Alergias:** {st.session_state.get('tiene_alergias')}")
                if st.session_state.get('alergias_especificas'):
                    alergias_lista = st.session_state.get('alergias_especificas', [])
                    st.write(f"• **Específicas:** {', '.join(alergias_lista)}")
            
            if st.session_state.get('tiene_intolerancias') and st.session_state.get('tiene_intolerancias') != "No tengo intolerancias":
                st.info(f"**Intolerancias:** {st.session_state.get('tiene_intolerancias')}")
                if st.session_state.get('intolerancias_especificas'):
                    intol_lista = st.session_state.get('intolerancias_especificas', [])
                    st.write(f"• **Específicas:** {', '.join(intol_lista)}")

        # Preferencias y antojos
        st.markdown("### 😋 Patrones de Preferencias y Antojos")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.get('sabores_favoritos'):
                sabores_lista = st.session_state.get('sabores_favoritos', [])
                st.write(f"• **Sabores favoritos:** {', '.join(sabores_lista)}")
            if st.session_state.get('comidas_comfort'):
                comidas_text = st.session_state.get('comidas_comfort', '')
                st.write(f"• **Comidas favoritas:** {comidas_text[:100]}{'...' if len(comidas_text) > 100 else ''}")
            st.write(f"• **Curiosidad alimentaria:** {st.session_state.get('curiosidad_alimentaria', 'No especificado')}")
        
        with col2:
            st.write(f"• **Frecuencia antojos:** {st.session_state.get('frecuencia_antojos', 'No especificado')}")
            if st.session_state.get('tipos_antojos') and "No tengo antojos específicos" not in st.session_state.get('tipos_antojos', []):
                antojos_lista = st.session_state.get('tipos_antojos', [])
                st.write(f"• **Tipos de antojos:** {', '.join(antojos_lista[:3])}{'...' if len(antojos_lista) > 3 else ''}")
            st.write(f"• **Control antojos:** {st.session_state.get('control_antojos', 'No especificado')}")

        # Contexto personal
        st.markdown("### 🏠 Contexto Personal")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"• **Situación familiar:** {st.session_state.get('situacion_familiar', 'No especificado')}")
            st.write(f"• **Quién cocina:** {st.session_state.get('quien_cocina', 'No especificado')}")
            st.write(f"• **Presupuesto:** {st.session_state.get('presupuesto_comida', 'No especificado')}")
        
        with col2:
            st.write(f"• **Horarios trabajo:** {st.session_state.get('trabajo_horarios', 'No especificado')}")
            st.write(f"• **Eventos sociales:** {st.session_state.get('eventos_sociales', 'No especificado')}")
            st.write(f"• **Objetivo específico:** {st.session_state.get('objetivo_principal_detallado', 'No especificado')}")

        # Recomendaciones personalizadas
        st.markdown("### 💡 Recomendaciones Personalizadas Iniciales")
        
        # Análisis básico basado en las respuestas
        recomendaciones = []
        
        if st.session_state.get('agua_pura_consumo') in ["Menos de 1 litro", "1-1.5 litros"]:
            recomendaciones.append("💧 **Hidratación:** Incrementar el consumo de agua pura gradualmente hasta alcanzar 2-2.5 litros diarios.")
        
        if st.session_state.get('vegetales_consumo') in ["No como vegetales", "1 porción"]:
            recomendaciones.append("🥬 **Vegetales:** Incorporar más vegetales variados, comenzando con los que más te gusten.")
        
        if (st.session_state.get('frecuencia_antojos') in ["Diariamente", "Varias veces al día"]) and (st.session_state.get('control_antojos') in ["Muy difícil, casi siempre cedo", "Imposible, siempre cedo a los antojos"]):
            recomendaciones.append("🧠 **Antojos:** Desarrollar estrategias específicas para manejar antojos, incluyendo alternativas saludables.")
        
        if st.session_state.get('ejercicio_frecuencia') == "No hago ejercicio":
            recomendaciones.append("🏃 **Actividad:** Incorporar actividad física gradual que complemente el plan nutricional.")
        
        if st.session_state.get('metodos_disponibles') and len(st.session_state.get('metodos_disponibles', [])) >= 5:
            recomendaciones.append("👨‍🍳 **Cocina:** Aprovechar la variedad de métodos de cocción disponibles para crear más opciones saludables.")
        
        if not recomendaciones:
            recomendaciones.append("✅ **Perfil balanceado:** Tu perfil muestra buenos hábitos base. Enfocaremos en optimización y personalización.")
        
        for i, rec in enumerate(recomendaciones, 1):
            st.write(f"{i}. {rec}")

        st.success(f"""
        ### ✅ Análisis de patrones alimentarios completado exitosamente
        
        **Tu perfil nutricional personalizado está listo** y incluye información detallada sobre:
        - 6 grupos alimentarios principales
        - Métodos de cocción disponibles y preferidos  
        - Restricciones, alergias e intolerancias
        - Patrones de preferencias y antojos
        - Contexto personal y familiar
        
        **Este análisis integral permitirá crear un plan nutricional completamente adaptado** 
        a tu estilo de vida, preferencias y necesidades específicas.
        
        La información será enviada a nuestro equipo de nutrición para desarrollar tu plan personalizado.
        """)

        st.markdown('</div>', unsafe_allow_html=True)

    # RESULTADO FINAL: Análisis de patrones alimentarios
    with st.expander("📈 **RESULTADO FINAL: Tu Perfil Alimentario Personalizado**", expanded=True):
        progress.progress(100)
        progress_text.text("Análisis completo: Generando tu perfil alimentario personalizado")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Tu Perfil Alimentario Personalizado")
        
        # Crear resumen del perfil
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Perfil Personal")
            st.write(f"• **Nombre:** {nombre}")
            st.write(f"• **Edad:** {edad} años")
            st.write(f"• **Sexo:** {sexo}")
            st.write(f"• **Origen cultural:** {origen_cultural if origen_cultural else 'No especificado'}")
            
            st.markdown("#### 🥗 Preferencias Principales")
            if sabores_preferidos:
                st.write(f"• **Sabores favoritos:** {', '.join(sabores_preferidos)}")
            if texturas_preferidas:
                st.write(f"• **Texturas preferidas:** {', '.join(texturas_preferidas)}")
            if patron_dietetico != "Ninguno en particular":
                st.write(f"• **Patrón dietético:** {patron_dietetico}")
                if motivacion_patron:
                    st.write(f"• **Motivación:** {motivacion_patron}")
        
        with col2:
            st.markdown("#### ⏰ Patrones Temporales")
            st.write(f"• **Comidas por día:** {comidas_por_dia}")
            st.write(f"• **Desayuno:** {horario_desayuno}")
            st.write(f"• **Almuerzo:** {horario_almuerzo}")
            st.write(f"• **Cena:** {horario_cena}")
            st.write(f"• **Frecuencia de snacks:** {snacks_frecuencia}")
            
            st.markdown("#### 👨‍🍳 Habilidades Culinarias")
            st.write(f"• **Nivel de cocina:** {nivel_cocina}")
            st.write(f"• **Tiempo disponible:** {tiempo_cocinar_dia}")
            st.write(f"• **Frecuencia cocina casa:** {frecuencia_cocina_casa}")

        # Análisis de restricciones
        if tiene_alergias != "No":
            st.markdown("#### ⚠️ Restricciones Importantes")
            st.warning(f"**Alergias/Intolerancias:** {tiene_alergias}")
            if alergias_especificas:
                st.write(f"• **Detalles:** {alergias_especificas}")

        # Recomendaciones personalizadas basadas en las respuestas
        st.markdown("### 💡 Recomendaciones Personalizadas")
        
        # Análisis del nivel de cocina para recomendaciones
        if nivel_cocina.startswith("Principiante"):
            recomendacion_cocina = "Enfócate en recetas simples de 3-5 ingredientes. Considera meal prep básico los fines de semana."
        elif nivel_cocina.startswith("Básico"):
            recomendacion_cocina = "Puedes explorar técnicas nuevas gradualmente. Ideal para batch cooking y preparaciones versátiles."
        elif nivel_cocina.startswith("Intermedio"):
            recomendacion_cocina = "Tienes base sólida para experimentar con sabores internacionales y técnicas más avanzadas."
        else:
            recomendacion_cocina = "Tu nivel avanzado te permite crear platos complejos. Considera explorar cocina molecular o técnicas especializadas."

        # Análisis del tiempo disponible
        if tiempo_cocinar_dia == "Menos de 15 minutos":
            recomendacion_tiempo = "Prioriza meal prep, alimentos pre-cortados y técnicas de cocción rápida como salteados."
        elif tiempo_cocinar_dia == "15-30 minutos":
            recomendacion_tiempo = "Tiempo ideal para platos balanceados. Una olla/sartén puede ser tu mejor estrategia."
        else:
            recomendacion_tiempo = "Tienes flexibilidad para explorar técnicas que requieren más tiempo como guisos, horneados o fermentaciones."

        # Mostrar recomendaciones
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"""
            **💻 Recomendación por nivel de cocina:**
            {recomendacion_cocina}
            """)
        with col2:
            st.info(f"""
            **⏱️ Recomendación por tiempo disponible:**
            {recomendacion_tiempo}
            """)

        # Objetivos y próximos pasos
        st.markdown("### 🎯 Próximos Pasos Recomendados")
        
        objetivos_texto = ""
        if objetivo_principal == "Perder peso":
            objetivos_texto = "Enfoque en preparaciones bajas en calorías pero satisfactorias, control de porciones y planificación de comidas."
        elif objetivo_principal == "Ganar peso/músculo":
            objetivos_texto = "Prioriza alimentos densos en nutrientes, aumenta frecuencia de comidas y incluye snacks nutritivos."
        elif objetivo_principal == "Mejorar energía y bienestar":
            objetivos_texto = "Enfócate en alimentos integrales, hidratación adecuada y horarios regulares de comida."
        else:
            objetivos_texto = "Plan balanceado enfocado en variedad nutricional y sostenibilidad a largo plazo."

        st.success(f"""
        ### ✅ Análisis completado exitosamente
        
        **Tu objetivo principal:** {objetivo_principal}
        
        **Estrategia recomendada:** {objetivos_texto}
        
        **Nivel de personalización:** Alto - basado en {len([x for x in [sabores_preferidos, texturas_preferidas, patron_dietetico, nivel_cocina] if x])} factores clave analizados.
        """)

        st.markdown('</div>', unsafe_allow_html=True)

# Construir resumen completo para email
def crear_resumen_email():
    resumen = f"""
=====================================
CUESTIONARIO PATRONES ALIMENTARIOS MUPAI
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
GRUPO 1: INFORMACIÓN BÁSICA NUTRICIONAL
=====================================
- Comidas por día actual: {st.session_state.get('comidas_por_dia_actual', 'No especificado')}
- Agua diaria: {st.session_state.get('agua_diaria', 'No especificado')}
- Frecuencia ejercicio: {st.session_state.get('ejercicio_frecuencia', 'No especificado')}
- Objetivo de peso: {st.session_state.get('peso_objetivo', 'No especificado')}
- Nivel de energía: {st.session_state.get('energia_nivel', 'No especificado')}
- Nivel de apetito: {st.session_state.get('apetito_nivel', 'No especificado')}

=====================================
GRUPO 2: FUENTES DE PROTEÍNA
=====================================
- Proteínas animales: {', '.join(st.session_state.get('proteinas_animales', [])) if st.session_state.get('proteinas_animales') else 'No especificado'}
- Frecuencia proteína animal: {st.session_state.get('frecuencia_proteina_animal', 'No especificado')}
- Proteínas vegetales: {', '.join(st.session_state.get('proteinas_vegetales', [])) if st.session_state.get('proteinas_vegetales') else 'No especificado'}
- Frecuencia proteína vegetal: {st.session_state.get('frecuencia_proteina_vegetal', 'No especificado')}
- Suplementos de proteína: {', '.join(st.session_state.get('suplementos_proteina', [])) if st.session_state.get('suplementos_proteina') else 'No especificado'}

=====================================
GRUPO 3: FUENTES DE GRASA SALUDABLE
=====================================
- Grasas vegetales: {', '.join(st.session_state.get('grasas_vegetales', [])) if st.session_state.get('grasas_vegetales') else 'No especificado'}
- Frecuencia grasas vegetales: {st.session_state.get('frecuencia_grasas_vegetales', 'No especificado')}
- Grasas animales: {', '.join(st.session_state.get('grasas_animales', [])) if st.session_state.get('grasas_animales') else 'No especificado'}
- Frecuencia grasas animales: {st.session_state.get('frecuencia_grasas_animales', 'No especificado')}

=====================================
MÉTODOS DE COCCIÓN (DESPUÉS GRUPO 3)
=====================================
- Métodos disponibles: {', '.join(st.session_state.get('metodos_disponibles', [])) if st.session_state.get('metodos_disponibles') else 'No especificado'}
- Métodos más prácticos: {', '.join(st.session_state.get('metodos_practicos', [])) if st.session_state.get('metodos_practicos') else 'No especificado'}
- Otro método especificado: {st.session_state.get('otro_metodo_coccion', 'No especificado')}

=====================================
GRUPO 4: CARBOHIDRATOS Y ENERGÍA
=====================================
- Cereales y granos: {', '.join(st.session_state.get('cereales_granos', [])) if st.session_state.get('cereales_granos') else 'No especificado'}
- Frecuencia cereales: {st.session_state.get('frecuencia_cereales', 'No especificado')}
- Tubérculos: {', '.join(st.session_state.get('tuberculos', [])) if st.session_state.get('tuberculos') else 'No especificado'}
- Frecuencia tubérculos: {st.session_state.get('frecuencia_tuberculos', 'No especificado')}
- Consumo de frutas: {st.session_state.get('frutas_consumo', 'No especificado')}
- Consumo de vegetales: {st.session_state.get('vegetales_consumo', 'No especificado')}

=====================================
GRUPO 5: HIDRATACIÓN Y BEBIDAS
=====================================
- Agua pura consumo: {st.session_state.get('agua_pura_consumo', 'No especificado')}
- Bebidas con cafeína: {', '.join(st.session_state.get('bebidas_con_cafeina', [])) if st.session_state.get('bebidas_con_cafeina') else 'No especificado'}
- Frecuencia cafeína: {st.session_state.get('frecuencia_cafeina', 'No especificado')}
- Otras bebidas: {', '.join(st.session_state.get('otras_bebidas', [])) if st.session_state.get('otras_bebidas') else 'No especificado'}
- Consumo de alcohol: {st.session_state.get('consumo_alcohol', 'No especificado')}
- Tipos de alcohol: {', '.join(st.session_state.get('tipos_alcohol', [])) if st.session_state.get('tipos_alcohol') else 'No especificado'}

=====================================
GRUPO 6: SUPLEMENTOS Y PRODUCTOS ESPECIALES
=====================================
- Usa suplementos: {st.session_state.get('usa_suplementos', 'No especificado')}
- Suplementos actuales: {', '.join(st.session_state.get('suplementos_actuales', [])) if st.session_state.get('suplementos_actuales') else 'No especificado'}
- Productos especiales: {', '.join(st.session_state.get('productos_especiales', [])) if st.session_state.get('productos_especiales') else 'No especificado'}
- Frecuencia productos especiales: {st.session_state.get('frecuencia_productos_especiales', 'No especificado')}

=====================================
APARTADO: ACEITES Y GRASAS DE COCINA
=====================================
- Aceites para cocinar: {', '.join(st.session_state.get('aceites_cocina', [])) if st.session_state.get('aceites_cocina') else 'No especificado'}
- Preferencia altas temperaturas: {st.session_state.get('preferencia_coccion', 'No especificado')}
- Aceites para ensaladas: {', '.join(st.session_state.get('aceites_ensalada', [])) if st.session_state.get('aceites_ensalada') else 'No especificado'}
- Cantidad aceite por día: {st.session_state.get('cantidad_aceite_dia', 'No especificado')}

=====================================
APARTADO: ALERGIAS E INTOLERANCIAS
=====================================
- Tiene alergias: {st.session_state.get('tiene_alergias', 'No especificado')}
- Alergias específicas: {', '.join(st.session_state.get('alergias_especificas', [])) if st.session_state.get('alergias_especificas') else 'No especificado'}
- Otras alergias: {st.session_state.get('otras_alergias', 'No especificado')}
- Tiene intolerancias: {st.session_state.get('tiene_intolerancias', 'No especificado')}
- Intolerancias específicas: {', '.join(st.session_state.get('intolerancias_especificas', [])) if st.session_state.get('intolerancias_especificas') else 'No especificado'}
- Otras intolerancias: {st.session_state.get('otras_intolerancias', 'No especificado')}

=====================================
APARTADO: PREFERENCIAS ALIMENTARIAS
=====================================
- Sabores favoritos: {', '.join(st.session_state.get('sabores_favoritos', [])) if st.session_state.get('sabores_favoritos') else 'No especificado'}
- Texturas favoritas: {', '.join(st.session_state.get('texturas_favoritas', [])) if st.session_state.get('texturas_favoritas') else 'No especificado'}
- Temperaturas preferidas: {', '.join(st.session_state.get('temperaturas_preferidas', [])) if st.session_state.get('temperaturas_preferidas') else 'No especificado'}
- Comidas comfort: {st.session_state.get('comidas_comfort', 'No especificado')}
- Alimentos que no le gustan: {st.session_state.get('alimentos_no_gustan', 'No especificado')}
- Curiosidad alimentaria: {st.session_state.get('curiosidad_alimentaria', 'No especificado')}

=====================================
APARTADO: ANTOJOS Y PATRONES EMOCIONALES
=====================================
- Frecuencia de antojos: {st.session_state.get('frecuencia_antojos', 'No especificado')}
- Tipos de antojos: {', '.join(st.session_state.get('tipos_antojos', [])) if st.session_state.get('tipos_antojos') else 'No especificado'}
- Horarios de antojos: {', '.join(st.session_state.get('horarios_antojos', [])) if st.session_state.get('horarios_antojos') else 'No especificado'}
- Triggers emocionales: {', '.join(st.session_state.get('triggers_emocionales', [])) if st.session_state.get('triggers_emocionales') else 'No especificado'}
- Control de antojos: {st.session_state.get('control_antojos', 'No especificado')}
- Estrategias para antojos: {st.session_state.get('estrategias_antojos', 'No especificado')}

=====================================
INFORMACIÓN ADICIONAL Y CONTEXTO
=====================================
- Situación familiar: {st.session_state.get('situacion_familiar', 'No especificado')}
- Quién cocina: {st.session_state.get('quien_cocina', 'No especificado')}
- Presupuesto comida: {st.session_state.get('presupuesto_comida', 'No especificado')}
- Horarios de trabajo: {st.session_state.get('trabajo_horarios', 'No especificado')}
- Eventos sociales: {st.session_state.get('eventos_sociales', 'No especificado')}
- Frecuencia de viajes: {st.session_state.get('viajes_frecuencia', 'No especificado')}
- Objetivo principal detallado: {st.session_state.get('objetivo_principal_detallado', 'No especificado')}
- Razón del cambio: {st.session_state.get('razon_cambio', 'No especificado')}
- Experiencias previas: {st.session_state.get('experiencias_previas', 'No especificado')}

=====================================
RESUMEN DE ANÁLISIS IDENTIFICADO:
=====================================
Este cuestionario completo de patrones alimentarios proporciona una base integral 
para el desarrollo de recomendaciones nutricionales altamente personalizadas basadas en:

1. 6 grupos alimentarios principales evaluados
2. Métodos de cocción disponibles y preferidos
3. Restricciones específicas (alergias e intolerancias)  
4. Patrones de preferencias detallados
5. Análisis de antojos y alimentación emocional
6. Contexto personal, familiar y social completo

RECOMENDACIONES PARA SEGUIMIENTO:
- Desarrollar plan nutricional personalizado basado en estos patrones
- Considerar restricciones y alergias como prioridad absoluta
- Aprovechar métodos de cocción preferidos y disponibles
- Integrar estrategias para manejo de antojos identificados
- Adaptar recomendaciones al contexto personal y familiar específico

=====================================
© 2025 MUPAI - Muscle up GYM
Alimentary Pattern Assessment Intelligence
=====================================
"""
    return resumen

# RESUMEN FINAL Y ENVÍO DE EMAIL
st.markdown("---")
st.markdown('<div class="content-card" style="background: linear-gradient(135deg, #F4C430 0%, #DAA520 100%); color: #1E1E1E;">', unsafe_allow_html=True)
st.markdown("## 🎯 **Resumen Final de tu Evaluación de Patrones Alimentarios**")
st.markdown(f"*Fecha: {fecha_llenado} | Cliente: {nombre}*")

# Mostrar métricas finales
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    ### 🥗 Preferencias
    - **Sabores principales:** {len(st.session_state.get('sabores_preferidos', []))} identificados
    - **Patrón dietético:** {st.session_state.get('patron_dietetico', 'Estándar')}
    - **Restricciones:** {'Sí' if st.session_state.get('tiene_alergias', 'No') != 'No' else 'No'}
    """)

with col2:
    st.markdown(f"""
    ### ⏰ Patrones Temporales  
    - **Comidas/día:** {st.session_state.get('comidas_por_dia', 'No especificado')}
    - **Horarios:** {'Regulares' if not st.session_state.get('horarios_irregulares') else 'Irregulares'}
    - **Snacks:** {st.session_state.get('snacks_frecuencia', 'No especificado')}
    """)

with col3:
    st.markdown(f"""
    ### 👨‍🍳 Habilidades
    - **Nivel cocina:** {st.session_state.get('nivel_cocina', 'No especificado')}
    - **Tiempo disponible:** {st.session_state.get('tiempo_cocinar_dia', 'No especificado')}
    - **Objetivo:** {st.session_state.get('objetivo_principal', 'No especificado')}
    """)

st.success(f"""
### ✅ Evaluación de patrones alimentarios completada exitosamente

Tu perfil alimentario ha sido analizado considerando todos los factores evaluados: preferencias, 
restricciones, habilidades culinarias, patrones temporales y contexto cultural. 

**Este análisis proporciona la base para desarrollar recomendaciones nutricionales personalizadas** 
que se ajusten a tu estilo de vida y preferencias individuales.

Se recomienda consulta con nutricionista especializado para desarrollar plan específico basado en estos patrones.
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
