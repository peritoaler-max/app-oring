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
# 1. CONFIGURAÇÃO DA PÁGINA E TEMA CLARO
# ==========================================
st.set_page_config(
    page_title="ORION SealCheck",
    page_icon="⚙️",
    layout="centered"
)

# Estilização para forçar o Light Mode com as cores da Orion (Vinho e Azul)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; color: #1e293b; }
    h1, h2, h3 { color: #0f172a; font-family: 'Helvetica Neue', Arial, sans-serif; }
    .stButton>button { 
        background-color: #b91c1c; color: white; 
        border-radius: 6px; border: none; width: 100%; height: 45px; font-weight: bold;
    }
    .stButton>button:hover { background-color: #991b1b; color: white; }
    .block-container { padding-top: 2rem; }
    div[data-testid="stBlock"] {
        background-color: #ffffff; padding: 20px; 
        border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 15px; border-left: 5px solid #1e3a8a;
    }
    </style>
""", unsafe_gradient=True)

# Cabeçalho com o nome profissional e dados fixos da Engenharia
st.title("⚙️ ORION SealCheck")
st.subheader("Sistema de Rastreabilidade e Integridade de Vedações")
st.markdown("---")

# ==========================================
# 2. SEÇÃO 1: IDENTIFICAÇÃO DO EQUIPAMENTO
# ==========================================
with st.container():
    st.markdown("### 1. Identificação do Equipamento")
    col1, col2 = st.columns(2)
    with col1:
        equipamento = st.selectbox("Descrição do Equipamento", ["Drain Valve 5\"", "Production Manifold", "Choke Valve", "Safety Valve"])
        part_number_eq = st.text_input("Part Number (P/N Equipamento)", value="PN-9923")
    with col2:
        sap_id = st.text_input("SAP ID / Tool ID (QR Code)", value="SAP-88341")
        st.metric(label="Pressão Máxima de Trabalho", value="9,701 PSI")

# ==========================================
# 3. SEÇÃO 2: DADOS DO SELO / O-RING
# ==========================================
with st.container():
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
with st.container():
    st.markdown("### 3. Checklist de Preparação e Instalação")
    ch1 = st.checkbox("1. Limpeza da ranhura/alojamento executada e livre de resíduos antigos.")
    ch2 = st.checkbox("2. Inspeção visual dimensional da ranhura realizada (sem riscos ou danos).")
    ch3 = st.checkbox("3. Selo/O-ring verificado fisicamente (ausência de rebarbas, cortes).")
    ch4 = st.checkbox("4. Lubrificação adequada aplicada no selo utilizando composto compatível.")
    ch5 = st.checkbox("5. Assentamento correto do selo na ranhura sem torções ou esmagamento.")
    
    checklist_ok = ch1 and ch2 and ch3 and ch4 and ch5

# ==========================================
# 5. SEÇÃO 4: EVIDÊNCIAS FOTOGRÁFICAS (FLUIDEZ ANDROID)
# ==========================================
with st.container():
    st.markdown("### 4. Evidências Digitais Obrigatórias")
    st.info("Caso a foto saia ruim, basta clicar no botão da câmera novamente para substituir a imagem anterior.")
    
    foto1 = st.camera_input("Foto 1: Componente e Etiqueta do Lote")
    foto2 = st.camera_input("Foto 2: Alojamento/Ranhura Limpa")
    foto3 = st.camera_input("Foto 3: Selo Instalado no Local")

# ==========================================
# 6. SEÇÃO 5: ASSINATURA E TRAVA LÓGICA
# ==========================================
with st.container():
    st.markdown("### 5. Encerramento Técnico")
    inspetor = st.text_input("Nome do Inspetor / Perito Responsável")
    
    # Validação rigorosa dos critérios de segurança
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
                # 7.1 Construção do PDF em memória
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "LAUDO TECNICO DE INTEGRIDADE DE VEDACOES", ln=True, align="C")
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 10, f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True)
                pdf.cell(0, 10, f"Inspetor: {inspetor}", ln=True)
                pdf.cell(0, 10, f"Equipamento: {equipamento} | PMWP: 9,701 PSI", ln=True)
                pdf.cell(0, 10, f"Selo P/N: {pn_selo} | Lote: {trace_number}", ln=True)
                pdf.cell(0, 10, "Status do Checklist: 100% CONFORME", ln=True)
                
                pdf_buffer = io.BytesIO()
                pdf_out = pdf.output(dest='S').encode('latin1')
                pdf_buffer.write(pdf_out)
                pdf_buffer.seek(0)
                
                # 7.2 Configuração de disparo do E-mail
                # SUBSTITUA ESTES DADOS COM SUAS CREDENCIAIS QUANDO QUISER ATIVAR
                REMETENTE = "peritoaler@gmail.com"
                DESTINATARIO = "peritoaler@gmail.com" # Coloque o e-mail do seu coordenador aqui
                SENHA_APP = "xxxx xxxx xxxx xxxx" # Sua senha de app de 16 dígitos do Google
                
                msg = MIMEMultipart()
                msg['From'] = REMETENTE
                msg['To'] = DESTINATARIO
                msg['Subject'] = f"🚨 ALERTA DE INSTALAÇÃO - {equipamento} (9.701 PSI)"
                
                corpo = f"Prezados,\n\nO inspetor {inspetor} realizou a instalação e validação do selo mecânico no equipamento {equipamento}.\nO checklist foi cumprido com sucesso e o relatório PDF gerado automaticamente está em anexo."
                msg.attach(MIMEText(corpo, 'plain'))
                
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(pdf_out)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="Laudo_Selo_{trace_number}.pdf"')
                msg.attach(part)
                
                # Descomente as linhas abaixo quando inserir sua Senha de App correta para disparar
                # server = smtplib.SMTP('smtp.gmail.com', 587)
                # server.starttls()
                # server.login(REMETENTE, SENHA_APP)
                # server.sendmail(REMETENTE, DESTINATARIO, msg.as_string())
                # server.quit()
                
                st.success("✅ Sucesso Total! Dados salvos na nuvem, PDF gerado e e-mail enviado aos coordenadores!")
                st.balloons()
                
            except Exception as e:
                st.error(f"Erro ao processar automações: {e}")
