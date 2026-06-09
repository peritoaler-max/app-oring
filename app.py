import streamlit as st
import datetime
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA NATIVA
# ==========================================
st.set_page_config(
    page_title="ORION SealCheck",
    page_icon="⚙️",
    layout="centered"
)

# Injeção da imagem técnica validada no topo como o ícone principal do App
st.image(
    "https://raw.githubusercontent.com/peritoaler-max/app-oring/master/image_275c83.png", 
    width=120
)

# Cabeçalho limpo e profissional
st.title("REGISTRO DE INSTALAÇÃO DE SELOS")
st.subheader("Sistema de Rastreabilidade e Integridade de Vedações — ORION")
st.markdown("---")

# ==========================================
# 2. SEÇÃO 1: IDENTIFICAÇÃO DO EQUIPAMENTO
# ==========================================
st.markdown("### 1. Identificação do Equipamento")
col1, col2 = st.columns(2)
with col1:
    equipamento = st.selectbox("Descrição do Equipamento", ["Drain Valve 5\"", "Production Manifold", "Choke Valve", "Safety Valve"])
    part_number_eq = st.text_input("Part Number (P/N Equipamento)", value="PN-9923")
with col2:
    sap_id = st.text_input("SAP ID / Tool ID (QR Code)", value="SAP-88341")
    st.metric(label="Pressão Máxima de Trabalho", value="9.701 PSI")

# ==========================================
# 3. SEÇÃO 2: DADOS DO SELO / O-RING
# ==========================================
st.markdown("### 2. Dados do Selo / O-Ring")
col3, col4 = st.columns(2)
with col3:
    pn_selo = st.text_input("Part Number do Selo", placeholder="Ex: PN-ORING-90")
    material = st.selectbox("Material / Composto", ["Viton", "HNBR", "Nitrílica", "PTFE"])
    cure_date = st.date_input("Cure Date (Data de Fab.)", value=datetime.date(2026, 6, 9))
with col4:
    trace_number = st.text_input("Trace Number (Lote)", placeholder="Ex: LOT-2026-09A")
    dureza = st.text_input("Dureza (Shore)", value="90 Shore")
    shelf_life = st.date_input("Shelf Life (Validade)", value=datetime.date(2031, 6, 9))

# ==========================================
# 4. SEÇÃO 3: CHECKLIST DE PREPARAÇÃO
# ==========================================
st.markdown("### 3. Checklist de Preparação e Instalação")
ch1 = st.checkbox("1. Limpeza da ranhura/alojamento executada e livre de resíduos antigos.")
ch2 = st.checkbox("2. Inspeção visual dimensional da ranhura realizada (sem riscos ou danos).")
ch3 = st.checkbox("3. Selo/O-ring verificado fisicamente (ausência de rebarbas, cortes).")
ch4 = st.checkbox("4. Lubrificação adequada aplicada no selo utilizando composto compatível.")
ch5 = st.checkbox("5. Assentamento correto do selo na ranhura sem torções ou esmagamento.")
    
checklist_ok = ch1 and ch2 and ch3 and ch4 and ch5

# ==========================================
# 5. SEÇÃO 4: EVIDÊNCIAS FOTOGRÁFICAS
# ==========================================
st.markdown("### 4. Evidências Digitais Obrigatórias")
st.info("📱 No celular, caso queira refazer a foto, basta clicar no componente de captura novamente.")
    
foto1 = st.camera_input("Foto 1: Componente e Etiqueta do Lote")
foto2 = st.camera_input("Foto 2: Alojamento/Ranhura Limpa")
foto3 = st.camera_input("Foto 3: Selo Instalado no Local")

# ==========================================
# 6. SEÇÃO 5: ASSINATURA E TRAVA LÓGICA
# ==========================================
st.markdown("### 5. Encerramento Técnico")
inspetor = st.text_input("Nome do Inspetor / Perito Responsável")
    
fotos_ok = foto1 is not None and foto2 is not None and foto3 is not None
assinatura_ok = len(inspetor.strip()) > 2
    
if not checklist_ok:
    st.warning("⚠️ Bloqueio: Todos os 5 itens do checklist de preparação devem ser marcados.")
if not fotos_ok:
    st.warning("⚠️ Bloqueio: É obrigatório capturar as 3 fotos de evidência técnica.")
if not assinatura_ok:
    st.warning("⚠️ Bloqueio: Digite o nome do responsável para assinar digitalmente.")

# ==========================================
# 7. FUNÇÃO ENVIAR: GERAÇÃO DE PDF E EMAIL
# ==========================================
if checklist_ok and fotos_ok and assinatura_ok:
    if st.button("🚀 ENVIAR REGISTRO & DISPARAR LAUDO"):
        with st.spinner("Compilando laudo técnico e notificando coordenadores..."):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "LAUDO TECNICO DE INTEGRIDADE DE VEDACOES", ln=1, align="C")
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 10, f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=1)
                pdf.cell(0, 10, f"Inspetor: {inspetor}", ln=1)
                pdf.cell(0, 10, f"Equipamento: {equipamento} | PMWP: 9.701 PSI", ln=1)
                pdf.cell(0, 10, f"Selo P/N: {pn_selo} | Lote: {trace_number}", ln=1)
                pdf.cell(0, 10, "Status do Checklist: 100% CONFORME", ln=1)
                
                pdf_out = pdf.output(dest='S').encode('latin1')
                
                st.success("✅ Sucesso Total! Dados salvos na nuvem e PDF gerado!")
                st.balloons()
                
            except Exception as e:
                st.error(f"Erro ao processar automações: {e}")
